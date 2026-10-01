from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.dependencias import obtener_hoy
from app.database import conectar
from app.main import app

HOY = date(2026, 10, 1)


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cliente HTTP sobre una base de datos temporal y con la fecha del día fija."""
    monkeypatch.setenv("VIAJES_DB", str(tmp_path / "prueba.db"))
    app.dependency_overrides[obtener_hoy] = lambda: HOY
    with TestClient(app) as c:      # el "with" ejecuta el arranque, que crea el esquema
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def bd(cliente):
    """Conexión directa a la base de datos de la prueba, para preparar datos de otros dominios."""
    conexion = conectar()
    yield conexion
    conexion.close()


def destino(c: TestClient, nombre: str, costo: int, **extra) -> dict:
    datos = {"nombre": nombre, "zona": "Zona", "descripcion": "", "duracion_dias": 2, "costo_base": costo}
    respuesta = c.post("/api/destinos", json={**datos, **extra})
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def paquete(c: TestClient, destino_ids: list[int], **extra) -> dict:
    datos = {"nombre": "Norte Grande en 5 días", "fecha_salida": "2026-12-10",
             "fecha_regreso": "2026-12-15", "cupo_maximo": 12, "margen": 0.20, "destino_ids": destino_ids}
    respuesta = c.post("/api/paquetes", json={**datos, **extra})
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()
