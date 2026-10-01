"""Pruebas de la API de destinos (HU-01) sobre SQLite real."""
from conftest import destino, paquete


def test_registrar_y_listar(cliente):                               # FR-01, FR-04
    creado = destino(cliente, "Valle del Elqui", 120_000)
    assert creado["disponible"] is True
    assert [d["nombre"] for d in cliente.get("/api/destinos").json()] == ["Valle del Elqui"]


def test_nombre_unico_sin_distinguir_mayusculas(cliente):           # R1
    destino(cliente, "Valle del Elqui", 120_000)
    respuesta = cliente.post("/api/destinos", json={"nombre": "  valle DEL elqui ", "zona": "Z",
                                                     "duracion_dias": 2, "costo_base": 1})
    assert respuesta.status_code == 400
    assert "Ya existe" in respuesta.json()["detail"]


def test_costo_base_debe_ser_positivo(cliente):                     # R2
    respuesta = cliente.post("/api/destinos", json={"nombre": "X", "zona": "Z",
                                                     "duracion_dias": 2, "costo_base": 0})
    assert respuesta.status_code == 400


def test_error_de_validacion_no_repite_el_valor_recibido(cliente):
    respuesta = cliente.post("/api/destinos", json={"nombre": "X", "zona": "Z",
                                                     "duracion_dias": "dato-secreto", "costo_base": 1})
    assert respuesta.status_code == 422
    assert "dato-secreto" not in respuesta.text
    assert respuesta.json()["errores"][0]["campo"] == "duracion_dias"


def test_modificar_destino(cliente):                                # FR-02
    d = destino(cliente, "Isla Damas", 38_000)
    respuesta = cliente.put(f"/api/destinos/{d['id']}", json={"costo_base": 40_000})
    assert respuesta.status_code == 200
    assert respuesta.json()["costo_base"] == 40_000 and respuesta.json()["nombre"] == "Isla Damas"


def test_modificar_a_un_nombre_existente_falla(cliente):
    destino(cliente, "Isla Damas", 38_000)
    otro = destino(cliente, "Cajón del Maipo", 45_000)
    respuesta = cliente.put(f"/api/destinos/{otro['id']}", json={"nombre": "isla damas"})
    assert respuesta.status_code == 400


def test_baja_de_destino_sin_paquetes_lo_elimina(cliente):          # FR-03, R8
    d = destino(cliente, "Isla Damas", 38_000)
    respuesta = cliente.delete(f"/api/destinos/{d['id']}")
    assert respuesta.json()["resultado"] == "eliminado"
    assert cliente.get(f"/api/destinos/{d['id']}").status_code == 404


def test_baja_de_destino_en_paquete_lo_marca_no_disponible(cliente):  # FR-03, R8
    a = destino(cliente, "Salar de Surire", 310_000)
    b = destino(cliente, "Valle del Elqui", 120_000)
    paquete(cliente, [a["id"], b["id"]])

    respuesta = cliente.delete(f"/api/destinos/{a['id']}")

    assert respuesta.json()["resultado"] == "no_disponible"
    assert cliente.get(f"/api/destinos/{a['id']}").json()["disponible"] is False
    disponibles = cliente.get("/api/destinos", params={"solo_disponibles": True}).json()
    assert [d["nombre"] for d in disponibles] == ["Valle del Elqui"]


def test_destino_inexistente(cliente):
    assert cliente.get("/api/destinos/999").status_code == 404
    assert cliente.put("/api/destinos/999", json={"zona": "Z"}).status_code == 404
    assert cliente.delete("/api/destinos/999").status_code == 404


def test_texto_con_sql_se_guarda_literal(cliente):                  # consultas parametrizadas
    nombre = "x'); DROP TABLE destinos; --"
    destino(cliente, nombre, 1_000)
    assert cliente.get("/api/destinos").json()[0]["nombre"] == nombre
