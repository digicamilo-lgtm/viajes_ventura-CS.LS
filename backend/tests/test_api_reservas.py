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


def _reservar(c, paquete_id: int, personas: int, encabezados: dict) -> dict:
    respuesta = c.post("/api/reservas", json={"paquete_id": paquete_id, "cantidad_personas": personas},
                       headers=encabezados)
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def test_cancelar_marca_la_reserva_y_libera_el_cupo(cliente):       # S4, R14
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))                       # cupo 12
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 12, encabezados)
    assert cliente.post("/api/reservas", json={"paquete_id": p["id"], "cantidad_personas": 1},
                        headers=encabezados).status_code == 400     # cupo lleno

    respuesta = cliente.delete(f"/api/reservas/{reserva['id']}", headers=encabezados)

    assert respuesta.status_code == 200, respuesta.text
    assert respuesta.json()["cancelada"] is True
    assert _reservar(cliente, p["id"], 12, encabezados)["cancelada"] is False  # cupo liberado


def test_cancelar_solo_la_reserva_propia(cliente):                  # R11
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 2, encabezados)
    otros = cliente_autenticado(cliente, correo="otra@example.com", nombre="Otra Persona")

    respuesta = cliente.delete(f"/api/reservas/{reserva['id']}", headers=otros)

    assert respuesta.status_code == 404
    assert cliente.get("/api/reservas", headers=encabezados).json()[0]["cancelada"] is False


def test_no_se_cancela_dos_veces(cliente):                          # S4
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 2, encabezados)
    cliente.delete(f"/api/reservas/{reserva['id']}", headers=encabezados)

    respuesta = cliente.delete(f"/api/reservas/{reserva['id']}", headers=encabezados)

    assert respuesta.status_code == 400
    assert "ya está cancelada" in respuesta.json()["detail"]


def test_no_se_cancela_un_paquete_que_ya_partio(cliente):           # S4
    from datetime import date
    from app.api.dependencias import obtener_hoy
    from app.main import app
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids), fecha_salida="2026-10-02", fecha_regreso="2026-10-05")
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 2, encabezados)
    app.dependency_overrides[obtener_hoy] = lambda: date(2026, 10, 3)

    respuesta = cliente.delete(f"/api/reservas/{reserva['id']}", headers=encabezados)

    assert respuesta.status_code == 400
    assert "ya partió" in respuesta.json()["detail"]


def test_modificar_reemplaza_la_reserva_con_el_precio_vigente(cliente):  # S4, R13
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))                       # precio por persona 516.000
    encabezados = cliente_autenticado(cliente)
    original = _reservar(cliente, p["id"], 2, encabezados)

    respuesta = cliente.put(f"/api/reservas/{original['id']}", json={"cantidad_personas": 3},
                            headers=encabezados)

    assert respuesta.status_code == 200, respuesta.text
    nueva = respuesta.json()
    assert nueva["id"] != original["id"]
    assert nueva["cantidad_personas"] == 3
    assert nueva["total"] == 1_548_000
    historial = {r["id"]: r for r in cliente.get("/api/reservas", headers=encabezados).json()}
    assert historial[original["id"]]["cancelada"] is True
    assert historial[nueva["id"]]["cancelada"] is False


def test_modificar_respeta_el_cupo_sin_contar_la_reserva_propia(cliente):  # R14
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))                       # cupo 12
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 2, encabezados)

    excede = cliente.put(f"/api/reservas/{reserva['id']}", json={"cantidad_personas": 13}, headers=encabezados)
    assert excede.status_code == 400

    completa = cliente.put(f"/api/reservas/{reserva['id']}", json={"cantidad_personas": 12}, headers=encabezados)
    assert completa.status_code == 200, completa.text                # el cupo entero es posible


def test_modificar_reserva_ajena_responde_404(cliente):             # R11
    ids = _dos_destinos(cliente)
    p = paquete_publicado(cliente, list(ids))
    encabezados = cliente_autenticado(cliente)
    reserva = _reservar(cliente, p["id"], 2, encabezados)
    otros = cliente_autenticado(cliente, correo="otra@example.com", nombre="Otra Persona")

    respuesta = cliente.put(f"/api/reservas/{reserva['id']}", json={"cantidad_personas": 1}, headers=otros)

    assert respuesta.status_code == 404
