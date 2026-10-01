"""Manejo de errores sin filtrar información interna (sección 7.3) — Cambio 9."""
from fastapi.testclient import TestClient

from app.main import app
from app.repositorios import PaqueteRepositorio


def test_error_no_controlado_no_expone_la_traza(cliente, monkeypatch):
    def fallar(*_):
        raise RuntimeError("detalle interno: C:\\servidor\\viajes.db SELECT * FROM clientes")

    monkeypatch.setattr(PaqueteRepositorio, "listar_publicados", fallar)
    # raise_server_exceptions=False: responder como lo haría el servidor real, sin relanzar en la prueba.
    respuesta = TestClient(app, raise_server_exceptions=False).get("/api/paquetes/publicados")

    assert respuesta.status_code == 500
    assert respuesta.json() == {"detail": "Error interno del servidor."}
    for filtrado in ("Traceback", "viajes.db", "SELECT", "RuntimeError"):
        assert filtrado not in respuesta.text
