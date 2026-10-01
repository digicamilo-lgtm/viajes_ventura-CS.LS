"""Reservas simultáneas sobre el mismo paquete (R14) — Cambio 9.

Antes de la corrección, 20 reservas simultáneas de 1 persona sobre un paquete
con cupo 5 se aceptaban todas (cupo disponible: -15).
"""
from concurrent.futures import ThreadPoolExecutor

from conftest import cliente_autenticado, destino, paquete_publicado
from fastapi.testclient import TestClient

from app.main import app

CUPO, SOLICITUDES = 5, 20


def test_reservas_simultaneas_no_superan_el_cupo(cliente):
    ids = [destino(cliente, "A", 1_000)["id"], destino(cliente, "B", 1_000)["id"]]
    p = paquete_publicado(cliente, ids, cupo_maximo=CUPO)
    encabezados = [cliente_autenticado(cliente, correo=f"c{i}@x.cl") for i in range(SOLICITUDES)]

    def reservar(encabezado):
        with TestClient(app) as c:      # un cliente HTTP por hilo, como navegadores distintos
            return c.post("/api/reservas", headers=encabezado,
                          json={"paquete_id": p["id"], "cantidad_personas": 1}).status_code

    with ThreadPoolExecutor(SOLICITUDES) as hilos:
        codigos = list(hilos.map(reservar, encabezados))

    assert codigos.count(201) == CUPO
    assert codigos.count(400) == SOLICITUDES - CUPO
    detalle = cliente.get(f"/api/paquetes/publicados/{p['id']}").json()
    assert detalle["personas_reservadas"] == CUPO
    assert detalle["cupo_disponible"] == 0
