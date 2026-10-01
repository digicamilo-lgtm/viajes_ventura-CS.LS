"""Pruebas de la API de clientes (HU-03) sobre SQLite real."""
from conftest import cliente_autenticado, cliente_registrado, encabezado, token


def test_registrar_no_expone_la_contrasena(cliente):                # R9, R10
    creado = cliente_registrado(cliente)
    assert "contrasena" not in creado and "hash_contrasena" not in creado
    assert creado["rut"] == "11111111-1" and creado["telefono"] == "+56 9 1111 1111"


def test_correo_unico_sin_distinguir_mayusculas(cliente):           # R9
    cliente_registrado(cliente, correo="carolina@example.com")
    respuesta = cliente.post("/api/clientes", json={
        "nombre": "Otra Persona", "rut": "22222222-2", "correo": "CAROLINA@example.com",
        "telefono": "+56922222222", "contrasena": "otra-clave-1"})
    assert respuesta.status_code == 400
    assert "Ya existe" in respuesta.json()["detail"]


def test_correo_invalido_es_rechazado(cliente):
    respuesta = cliente.post("/api/clientes", json={
        "nombre": "X", "rut": "11111111-1", "correo": "no-es-un-correo",
        "telefono": "+56911111111", "contrasena": "clave-segura-1"})
    assert respuesta.status_code == 400


def test_iniciar_sesion_con_credenciales_correctas(cliente):        # FR-10
    cliente_registrado(cliente, correo="carolina@example.com", contrasena="clave-segura-1")
    t = token(cliente, "carolina@example.com", "clave-segura-1")
    assert isinstance(t, str) and len(t) > 10


def test_iniciar_sesion_con_contrasena_incorrecta_falla_generico(cliente):
    cliente_registrado(cliente, correo="carolina@example.com", contrasena="clave-segura-1")
    respuesta = cliente.post("/api/clientes/sesiones",
                             json={"correo": "carolina@example.com", "contrasena": "clave-equivocada"})
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Correo o contraseña incorrectos."


def test_iniciar_sesion_con_correo_inexistente_da_el_mismo_mensaje(cliente):  # sección 7.1
    respuesta = cliente.post("/api/clientes/sesiones",
                             json={"correo": "nadie@example.com", "contrasena": "lo-que-sea"})
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Correo o contraseña incorrectos."


def test_mi_perfil_requiere_autenticacion(cliente):                 # R11
    assert cliente.get("/api/clientes/yo").status_code == 401


def test_mi_perfil_devuelve_los_datos_completos(cliente):           # R17
    encabezados = cliente_autenticado(cliente)
    respuesta = cliente.get("/api/clientes/yo", headers=encabezados)
    assert respuesta.status_code == 200
    assert respuesta.json()["rut"] == "11111111-1"


def test_token_invalido_es_rechazado(cliente):
    respuesta = cliente.get("/api/clientes/yo", headers=encabezado("esto-no-es-un-token"))
    assert respuesta.status_code == 401
