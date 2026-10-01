"""Pruebas de la API de paquetes (HU-02) sobre SQLite real."""
import pytest
from conftest import destino, paquete


@pytest.fixture
def surire_elqui(cliente):
    return destino(cliente, "Salar de Surire", 310_000), destino(cliente, "Valle del Elqui", 120_000)


def ids(*destinos):
    return [d["id"] for d in destinos]


def test_crear_paquete_calcula_el_precio(cliente, surire_elqui):    # FR-05, FR-06
    creado = paquete(cliente, ids(*surire_elqui))
    assert creado["estado"] == "BORRADOR"
    assert creado["precio_por_persona"] == 516_000
    assert creado["cupo_disponible"] == 12
    assert [d["nombre"] for d in creado["destinos"]] == ["Salar de Surire", "Valle del Elqui"]


@pytest.mark.parametrize("cambios, codigo", [
    ({"destino_ids": "uno"}, 422),
    ({"fecha_regreso": "2026-12-01"}, 400),            # R5
    ({"cupo_maximo": 0}, 400),                         # R5
    ({"margen": -0.2}, 400),                           # R6
])
def test_crear_paquete_invalido(cliente, surire_elqui, cambios, codigo):
    datos = {"nombre": "P", "fecha_salida": "2026-12-10", "fecha_regreso": "2026-12-15",
             "cupo_maximo": 12, "destino_ids": ids(*surire_elqui), **cambios}
    assert cliente.post("/api/paquetes", json=datos).status_code == codigo


def test_crear_paquete_con_un_solo_destino_o_repetido(cliente, surire_elqui):  # R3
    surire, _ = surire_elqui
    base = {"nombre": "P", "fecha_salida": "2026-12-10", "fecha_regreso": "2026-12-15", "cupo_maximo": 5}
    assert cliente.post("/api/paquetes", json={**base, "destino_ids": [surire["id"]]}).status_code == 400
    respuesta = cliente.post("/api/paquetes", json={**base, "destino_ids": [surire["id"], surire["id"]]})
    assert respuesta.status_code == 400 and "repetir" in respuesta.json()["detail"]


def test_crear_paquete_con_destino_inexistente(cliente, surire_elqui):
    respuesta = cliente.post("/api/paquetes", json={
        "nombre": "P", "fecha_salida": "2026-12-10", "fecha_regreso": "2026-12-15",
        "cupo_maximo": 5, "destino_ids": [surire_elqui[0]["id"], 999]})
    assert respuesta.status_code == 404 and "999" in respuesta.json()["detail"]


def test_destino_no_disponible_no_entra_en_paquetes_nuevos(cliente, surire_elqui):  # R8
    surire, elqui = surire_elqui
    paquete(cliente, ids(surire, elqui))
    cliente.delete(f"/api/destinos/{surire['id']}")             # queda no disponible
    otro = destino(cliente, "Isla Damas", 38_000)
    respuesta = cliente.post("/api/paquetes", json={
        "nombre": "Nuevo", "fecha_salida": "2026-12-10", "fecha_regreso": "2026-12-15",
        "cupo_maximo": 5, "destino_ids": ids(surire, otro)})
    assert respuesta.status_code == 400 and "no disponibles" in respuesta.json()["detail"]


def test_precio_publicado_no_cambia_si_cambia_el_costo(cliente, surire_elqui):  # R7, FR-07
    surire, elqui = surire_elqui
    publicado = paquete(cliente, ids(surire, elqui))
    borrador = paquete(cliente, ids(surire, elqui), nombre="Borrador")
    assert cliente.post(f"/api/paquetes/{publicado['id']}/publicar").json()["estado"] == "PUBLICADO"

    cliente.put(f"/api/destinos/{surire['id']}", json={"costo_base": 400_000})

    assert cliente.get(f"/api/paquetes/{publicado['id']}").json()["precio_por_persona"] == 516_000
    assert cliente.get(f"/api/paquetes/{borrador['id']}").json()["precio_por_persona"] == 624_000


def test_publicados_excluye_borradores_y_vencidos(cliente, surire_elqui):  # CU-01, S2, S3
    vigente = paquete(cliente, ids(*surire_elqui), nombre="Vigente")
    vencido = paquete(cliente, ids(*surire_elqui), nombre="Vencido",
                      fecha_salida="2026-09-01", fecha_regreso="2026-09-05")
    paquete(cliente, ids(*surire_elqui), nombre="Borrador")
    for p in (vigente, vencido):
        cliente.post(f"/api/paquetes/{p['id']}/publicar")

    publicados = cliente.get("/api/paquetes/publicados").json()

    assert [p["nombre"] for p in publicados] == ["Vigente"]
    assert cliente.get(f"/api/paquetes/{vencido['id']}").json()["vencido"] is True
    assert len(cliente.get("/api/paquetes").json()) == 3


def test_cupo_disponible_descuenta_reservas(cliente, bd, surire_elqui):  # R14, FR-08
    p = paquete(cliente, ids(*surire_elqui))
    cliente.post(f"/api/paquetes/{p['id']}/publicar")
    # Las reservas son del dominio de Logan; aquí se insertan directo para probar el cupo.
    with bd:
        bd.execute("INSERT INTO clientes (nombre, rut, correo, telefono, hash_contrasena)"
                   " VALUES ('C', '1-9', 'c@x.cl', '9', 'h')")
        bd.executemany("INSERT INTO reservas (cliente_id, paquete_id, fecha_emision, cantidad_personas, total)"
                       " VALUES (1, ?, '2026-10-01', ?, 1)", [(p["id"], 3), (p["id"], 2)])

    detalle = cliente.get(f"/api/paquetes/{p['id']}").json()
    assert detalle["personas_reservadas"] == 5 and detalle["cupo_disponible"] == 7


def test_modificar_paquete_en_borrador(cliente, surire_elqui):
    p = paquete(cliente, ids(*surire_elqui))
    otro = destino(cliente, "Isla Damas", 38_000)
    respuesta = cliente.put(f"/api/paquetes/{p['id']}",
                            json={"margen": 0, "destino_ids": ids(surire_elqui[0], otro)})
    assert respuesta.status_code == 200
    assert respuesta.json()["precio_por_persona"] == 348_000


def test_paquete_publicado_no_se_modifica_ni_elimina(cliente, surire_elqui):  # R7, S3
    p = paquete(cliente, ids(*surire_elqui))
    cliente.post(f"/api/paquetes/{p['id']}/publicar")
    assert cliente.put(f"/api/paquetes/{p['id']}", json={"cupo_maximo": 50}).status_code == 400
    assert cliente.delete(f"/api/paquetes/{p['id']}").status_code == 400
    assert cliente.post(f"/api/paquetes/{p['id']}/publicar").status_code == 400


def test_eliminar_borrador(cliente, surire_elqui):
    p = paquete(cliente, ids(*surire_elqui))
    assert cliente.delete(f"/api/paquetes/{p['id']}").status_code == 204
    assert cliente.get(f"/api/paquetes/{p['id']}").status_code == 404
    # Sin paquetes que lo usen, el destino vuelve a poder eliminarse (R8).
    assert cliente.delete(f"/api/destinos/{surire_elqui[0]['id']}").json()["resultado"] == "eliminado"
