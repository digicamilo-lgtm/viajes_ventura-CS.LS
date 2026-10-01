from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.dependencias import obtener_hoy
from app.database import conectar
from app.dominio import Administrador
from app.main import app
from app.repositorios import AdministradorRepositorio
from app.seguridad import contrasenas, crear_token, hashear

HOY = date(2026, 10, 1)
ADMIN_CORREO, ADMIN_CONTRASENA = "paulina@viajesaventura.cl", "clave-admin-de-pruebas"


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cliente HTTP sin sesión, sobre una base de datos temporal y con la fecha del día fija.

    Crea además una cuenta de administrador; su encabezado queda en `c.encabezado_admin`
    para que los helpers de catálogo lo usen.
    """
    monkeypatch.setenv("VIAJES_DB", str(tmp_path / "prueba.db"))
    monkeypatch.setenv("JWT_SECRET", "clave-de-pruebas-no-usar-en-produccion")
    monkeypatch.setattr(contrasenas, "_COSTO", 4)     # bcrypt rápido en pruebas; en producción, 12
    app.dependency_overrides[obtener_hoy] = lambda: HOY
    with TestClient(app) as c:      # el "with" ejecuta el arranque, que crea el esquema
        conexion = conectar()
        admin = AdministradorRepositorio(conexion).guardar(
            Administrador("Paulina Ovalle", ADMIN_CORREO, hashear(ADMIN_CONTRASENA)))
        conexion.close()
        c.encabezado_admin = encabezado(crear_token(admin.id, Administrador.ROL))
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin(cliente):
    """Cliente HTTP con la sesión del administrador ya iniciada."""
    c = TestClient(app, headers=cliente.encabezado_admin)
    c.encabezado_admin = cliente.encabezado_admin
    return c


@pytest.fixture
def bd(cliente):
    """Conexión directa a la base de datos de la prueba, para preparar datos de otros dominios."""
    conexion = conectar()
    yield conexion
    conexion.close()


def destino(c: TestClient, nombre: str, costo: int, **extra) -> dict:
    datos = {"nombre": nombre, "zona": "Zona", "descripcion": "", "duracion_dias": 2, "costo_base": costo}
    respuesta = c.post("/api/destinos", json={**datos, **extra}, headers=c.encabezado_admin)
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def paquete(c: TestClient, destino_ids: list[int], **extra) -> dict:
    datos = {"nombre": "Norte Grande en 5 días", "fecha_salida": "2026-12-10",
             "fecha_regreso": "2026-12-15", "cupo_maximo": 12, "margen": 0.20, "destino_ids": destino_ids}
    respuesta = c.post("/api/paquetes", json={**datos, **extra}, headers=c.encabezado_admin)
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def paquete_publicado(c: TestClient, destino_ids: list[int], **extra) -> dict:
    p = paquete(c, destino_ids, **extra)
    respuesta = c.post(f"/api/paquetes/{p['id']}/publicar", headers=c.encabezado_admin)
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()


def cliente_registrado(c: TestClient, nombre: str = "Carolina Reyes", correo: str = "carolina@example.com",
                       contrasena: str = "clave-segura-1", **extra) -> dict:
    datos = {"nombre": nombre, "rut": "11111111-1", "correo": correo, "telefono": "+56 9 1111 1111",
             "contrasena": contrasena}
    respuesta = c.post("/api/clientes", json={**datos, **extra})
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def token(c: TestClient, correo: str = "carolina@example.com", contrasena: str = "clave-segura-1") -> str:
    respuesta = c.post("/api/clientes/sesiones", json={"correo": correo, "contrasena": contrasena})
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()["token"]


def encabezado(token_: str) -> dict:
    return {"Authorization": f"Bearer {token_}"}


def cliente_autenticado(c: TestClient, **extra) -> dict:
    """Registra un cliente y devuelve el encabezado Authorization listo para usar."""
    cliente_registrado(c, **extra)
    correo = extra.get("correo", "carolina@example.com")
    contrasena = extra.get("contrasena", "clave-segura-1")
    return encabezado(token(c, correo, contrasena))
