"""Pruebas de la API de destinos (HU-01) sobre SQLite real."""
from conftest import destino, paquete


def test_registrar_y_listar(admin):                               # FR-01, FR-04
    creado = destino(admin, "Valle del Elqui", 120_000)
    assert creado["disponible"] is True
    assert [d["nombre"] for d in admin.get("/api/destinos").json()] == ["Valle del Elqui"]


def test_nombre_unico_sin_distinguir_mayusculas(admin):           # R1
    destino(admin, "Valle del Elqui", 120_000)
    respuesta = admin.post("/api/destinos", json={"nombre": "  valle DEL elqui ", "zona": "Z",
                                                   "duracion_dias": 2, "costo_base": 1})
    assert respuesta.status_code == 400
    assert "Ya existe" in respuesta.json()["detail"]


def test_costo_base_debe_ser_positivo(admin):                     # R2
    respuesta = admin.post("/api/destinos", json={"nombre": "X", "zona": "Z",
                                                   "duracion_dias": 2, "costo_base": 0})
    assert respuesta.status_code == 400


def test_error_de_validacion_no_repite_el_valor_recibido(admin):
    respuesta = admin.post("/api/destinos", json={"nombre": "X", "zona": "Z",
                                                   "duracion_dias": "dato-secreto", "costo_base": 1})
    assert respuesta.status_code == 422
    assert "dato-secreto" not in respuesta.text
    assert respuesta.json()["errores"][0]["campo"] == "duracion_dias"


def test_modificar_destino(admin):                                # FR-02
    d = destino(admin, "Isla Damas", 38_000)
    respuesta = admin.put(f"/api/destinos/{d['id']}", json={"costo_base": 40_000})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["costo_base"] == 40_000
    assert datos["nombre"] == "Isla Damas"


def test_modificar_a_un_nombre_existente_falla(admin):
    destino(admin, "Isla Damas", 38_000)
    otro = destino(admin, "Cajón del Maipo", 45_000)
    respuesta = admin.put(f"/api/destinos/{otro['id']}", json={"nombre": "isla damas"})
    assert respuesta.status_code == 400


def test_baja_de_destino_sin_paquetes_lo_elimina(admin):          # FR-03, R8
    d = destino(admin, "Isla Damas", 38_000)
    respuesta = admin.delete(f"/api/destinos/{d['id']}")
    assert respuesta.json()["resultado"] == "eliminado"
    assert admin.get(f"/api/destinos/{d['id']}").status_code == 404


def test_baja_de_destino_en_paquete_lo_marca_no_disponible(admin):  # FR-03, R8
    a = destino(admin, "Salar de Surire", 310_000)
    b = destino(admin, "Valle del Elqui", 120_000)
    paquete(admin, [a["id"], b["id"]])

    respuesta = admin.delete(f"/api/destinos/{a['id']}")

    assert respuesta.json()["resultado"] == "no_disponible"
    assert admin.get(f"/api/destinos/{a['id']}").json()["disponible"] is False
    disponibles = admin.get("/api/destinos", params={"solo_disponibles": True}).json()
    assert [d["nombre"] for d in disponibles] == ["Valle del Elqui"]


def test_destino_inexistente(admin):
    assert admin.get("/api/destinos/999").status_code == 404
    assert admin.put("/api/destinos/999", json={"zona": "Z"}).status_code == 404
    assert admin.delete("/api/destinos/999").status_code == 404


def test_texto_con_sql_se_guarda_literal(admin):                  # consultas parametrizadas
    nombre = "x'); DROP TABLE destinos; --"
    destino(admin, nombre, 1_000)
    assert admin.get("/api/destinos").json()[0]["nombre"] == nombre
