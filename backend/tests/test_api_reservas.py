"""Pruebas de la API de reservas (HU-04) sobre SQLite real."""
from conftest import cliente_autenticado, destino, paquete, paquete_publicado


def _dos_destinos(c):
    a = destino(c, "Salar de Surire", 310_000)
    b = destino(c, "Valle del Elqui", 120_000)
    return a["id"], b["id"]


def test_reservar_requiere_autenticacion(cliente):                  # R11
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))
    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 2})
    assert respuesta.status_code == 401


def test_reservar_calcula_el_total_y_registra_fecha_de_emision(cliente):  # R12, R13
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))                       # precio_por_persona = 516.000
    encabezados = cliente_autenticado(cliente)

    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 2},
                             headers=encabezados)

    assert respuesta.status_code == 201, respuesta.text
    reserva = respuesta.json()
    assert reserva["total"] == 1_032_000
    assert reserva["cantidad_personas"] == 2
    assert reserva["fecha_emision"] == "2026-10-01"                 # HOY fijo en conftest


def test_no_se_puede_reservar_un_paquete_en_borrador(cliente):      # FR-12
    ids = _dos_destinos(cliente)
    p = paquete(cliente, list(ids))                                 # no publicado
    encabezados = cliente_autenticado(cliente)

    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 1},
                             headers=encabezados)

    assert respuesta.status_code == 400
    assert "publicado" in respuesta.json()["detail"]


def test_rechaza_reserva_que_supera_el_cupo_disponible(cliente):    # R14
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids), cupo_maximo=3)
    encabezados = cliente_autenticado(cliente)
    cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 3}, headers=encabezados)

    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 1},
                             headers=encabezados)

    assert respuesta.status_code == 400
    assert "cupo" in respuesta.json()["detail"]


def test_rechaza_reserva_sobre_paquete_vencido(cliente):            # R15
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids), fecha_salida="2026-09-01", fecha_regreso="2026-09-05")
    encabezados = cliente_autenticado(cliente)

    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 1},
                             headers=encabezados)

    assert respuesta.status_code == 400
    assert "ya pasó" in respuesta.json()["detail"]


def test_rechaza_menos_de_una_persona(cliente):                     # R16
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))
    encabezados = cliente_autenticado(cliente)

    respuesta = cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 0},
                             headers=encabezados)

    assert respuesta.status_code == 422                             # lo rechaza Pydantic (ge=1)


def test_reservar_paquete_inexistente(cliente):
    encabezados = cliente_autenticado(cliente)
    respuesta = cliente.post("/api/reservas", json={"paquete_id": 999, "cantidad_personas": 1},
                             headers=encabezados)
    assert respuesta.status_code == 404


def test_mis_reservas_solo_muestra_las_propias(cliente):            # FR-15, R11
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))

    encabezados_carolina = cliente_autenticado(cliente, nombre="Carolina Reyes", correo="carolina@example.com")
    cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 1},
                headers=encabezados_carolina)

    encabezados_andres = cliente_autenticado(cliente, nombre="Andrés Pinto", correo="andres@example.com")
    respuesta_andres = cliente.get("/api/reservas", headers=encabezados_andres)
    respuesta_carolina = cliente.get("/api/reservas", headers=encabezados_carolina)

    assert respuesta_andres.json() == []
    assert len(respuesta_carolina.json()) == 1
