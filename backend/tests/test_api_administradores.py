"""Autenticación de administradores y autorización del catálogo (S1, RNF-03) — Cambio 9."""
import bcrypt
import pytest
from conftest import (ADMIN_CONTRASENA, ADMIN_CORREO, cliente_autenticado, destino, encabezado, paquete,
                      paquete_publicado)

from app import crear_administrador
from app.database import conectar
from app.repositorios import AdministradorRepositorio


def test_iniciar_sesion_de_administrador(cliente):
    respuesta = cliente.post("/api/administradores/sesiones",
                             json={"correo": ADMIN_CORREO, "contrasena": ADMIN_CONTRASENA})
    assert respuesta.status_code == 200
    perfil = cliente.get("/api/administradores/yo", headers=encabezado(respuesta.json()["token"]))
    assert perfil.json()["correo"] == ADMIN_CORREO


@pytest.mark.parametrize("ruta", ["/api/clientes/sesiones", "/api/administradores/sesiones"])
def test_login_con_correo_inexistente_igual_ejecuta_bcrypt(cliente, monkeypatch, ruta):
    """Mismo trabajo (y tiempo) con o sin correo registrado: no se puede saber cuál existe."""
    llamadas = []
    original = bcrypt.checkpw
    monkeypatch.setattr(bcrypt, "checkpw", lambda *a: llamadas.append(1) or original(*a))
    respuesta = cliente.post(ruta, json={"correo": "nadie@x.cl", "contrasena": "x"})
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Correo o contraseña incorrectos."
    assert llamadas == [1]


@pytest.mark.parametrize("metodo, ruta", [
    ("get", "/api/destinos"), ("post", "/api/destinos"), ("put", "/api/destinos/1"),
    ("delete", "/api/destinos/1"), ("get", "/api/paquetes"), ("get", "/api/paquetes/1"),
    ("post", "/api/paquetes"), ("put", "/api/paquetes/1"), ("post", "/api/paquetes/1/publicar"),
    ("delete", "/api/paquetes/1"),
])
def test_catalogo_exige_administrador(cliente, metodo, ruta):
    """Sin sesión: 401. Con sesión de cliente: 403 (S1, RNF-03)."""
    assert getattr(cliente, metodo)(ruta).status_code == 401
    assert getattr(cliente, metodo)(ruta, headers=cliente_autenticado(cliente)).status_code == 403


def test_token_de_cliente_no_sirve_como_administrador_con_el_mismo_id(cliente):
    """El cliente 1 y el administrador 1 comparten id; el rol del token los distingue."""
    encabezado_cliente = cliente_autenticado(cliente)
    assert cliente.get("/api/clientes/yo", headers=encabezado_cliente).json()["id"] == 1
    assert cliente.get("/api/administradores/yo", headers=encabezado_cliente).status_code == 403
    assert cliente.post("/api/destinos", headers=encabezado_cliente, json={
        "nombre": "X", "zona": "Z", "duracion_dias": 1, "costo_base": 1}).status_code == 403


def test_administrador_no_puede_reservar(cliente):                     # R11: reservar es de clientes
    ids = [destino(cliente, "A", 1_000)["id"], destino(cliente, "B", 1_000)["id"]]
    p = paquete_publicado(cliente, ids)
    respuesta = cliente.post("/api/reservas", headers=cliente.encabezado_admin,
                             json={"paquete_id": p["id"], "cantidad_personas": 1})
    assert respuesta.status_code == 403


def test_vista_publica_de_paquetes_no_muestra_borradores(cliente):     # S2
    ids = [destino(cliente, "A", 1_000)["id"], destino(cliente, "B", 1_000)["id"]]
    borrador = paquete(cliente, ids, nombre="Borrador")
    publicado = paquete_publicado(cliente, ids, nombre="Publicado")
    assert [p["nombre"] for p in cliente.get("/api/paquetes/publicados").json()] == ["Publicado"]
    assert cliente.get(f"/api/paquetes/publicados/{publicado['id']}").status_code == 200
    assert cliente.get(f"/api/paquetes/publicados/{borrador['id']}").status_code == 404


# --- python -m app.crear_administrador --------------------------------------
def _contrasenas(monkeypatch, *valores):
    respuestas = iter(valores)
    monkeypatch.setattr(crear_administrador.getpass, "getpass", lambda _: next(respuestas))


def test_crear_administrador_por_consola(cliente, monkeypatch):
    _contrasenas(monkeypatch, "clave-muy-segura-123", "clave-muy-segura-123")
    assert crear_administrador.main(["--nombre", "Ignacio Salas", "--correo", "ignacio@x.cl"]) == 0
    conexion = conectar()
    creado = AdministradorRepositorio(conexion).buscar_por_correo("ignacio@x.cl")
    conexion.close()
    assert creado is not None
    assert creado.hash_contrasena.startswith("$2b$")


@pytest.mark.parametrize("contrasenas, correo", [
    (("corta", "corta"), "nuevo@x.cl"),                                   # menos de 12 caracteres
    (("clave-muy-segura-123", "otra-clave-distinta"), "nuevo@x.cl"),      # no coinciden
    (("clave-muy-segura-123", "clave-muy-segura-123"), ADMIN_CORREO),     # correo ya registrado
])
def test_crear_administrador_rechaza_datos_invalidos(cliente, monkeypatch, contrasenas, correo):
    _contrasenas(monkeypatch, *contrasenas)
    assert crear_administrador.main(["--nombre", "X", "--correo", correo]) == 1
