"""Flujo de punta a punta con los 4 dominios integrados (Cambio 8: integración, Sprint 2).

Recorre el caso completo con los datos del caso de estudio, a través de la API
y sobre SQLite real, como lo harían los socios y los clientes de Viajes Aventura:
el administrador arma y publica el catálogo, dos clientes se registran y
reservan, y se verifica que las fallas de la temporada pasada (sobreventa,
precio cambiado después de vender, historial ajeno, destino borrado) ya no ocurren.
"""
from conftest import ADMIN_CONTRASENA, ADMIN_CORREO, encabezado


def test_flujo_completo_viajes_aventura(cliente):
    http = cliente

    # 1. El administrador inicia sesión (S1, CU-03).
    respuesta = http.post("/api/administradores/sesiones",
                          json={"correo": ADMIN_CORREO, "contrasena": ADMIN_CONTRASENA})
    assert respuesta.status_code == 200
    admin = encabezado(respuesta.json()["token"])

    # 2. Registra destinos del caso (FR-01) y lista el catálogo (FR-04).
    def registrar_destino(nombre, zona, dias, costo):
        r = http.post("/api/destinos", headers=admin, json={
            "nombre": nombre, "zona": zona, "duracion_dias": dias, "costo_base": costo})
        assert r.status_code == 201, r.text
        return r.json()["id"]

    surire = registrar_destino("Salar de Surire", "Región de Arica y Parinacota", 3, 310_000)
    elqui = registrar_destino("Valle del Elqui", "Región de Coquimbo", 2, 120_000)
    damas = registrar_destino("Isla Damas", "Región de Coquimbo", 1, 38_000)
    assert len(http.get("/api/destinos", headers=admin).json()) == 3

    # 3. Arma "Norte Grande en 5 días": el sistema calcula el precio (FR-05, FR-06) y lo publica (FR-07).
    r = http.post("/api/paquetes", headers=admin, json={
        "nombre": "Norte Grande en 5 días", "fecha_salida": "2026-12-10", "fecha_regreso": "2026-12-15",
        "cupo_maximo": 12, "margen": 0.20, "destino_ids": [surire, elqui]})
    assert r.status_code == 201
    norte = r.json()
    assert norte["precio_por_persona"] == 516_000
    assert norte["estado"] == "BORRADOR"
    assert http.get("/api/paquetes/publicados").json() == []           # un borrador no se ofrece (S2)
    assert http.post(f"/api/paquetes/{norte['id']}/publicar", headers=admin).json()["estado"] == "PUBLICADO"

    # 4. Una visitante ve el paquete con su cupo (FR-08), se registra (FR-09) e inicia sesión (FR-10).
    publicados = http.get("/api/paquetes/publicados").json()
    assert [(p["nombre"], p["cupo_disponible"]) for p in publicados] == [("Norte Grande en 5 días", 12)]
    assert http.post("/api/reservas", json={"paquete_id": norte["id"], "cantidad_personas": 2}).status_code == 401

    def registrar_cliente(nombre, rut, correo):
        r = http.post("/api/clientes", json={"nombre": nombre, "rut": rut, "correo": correo,
                                             "telefono": "+56 9 1234 5678", "contrasena": "clave-segura-1"})
        assert r.status_code == 201, r.text
        r = http.post("/api/clientes/sesiones", json={"correo": correo, "contrasena": "clave-segura-1"})
        return encabezado(r.json()["token"])

    carolina = registrar_cliente("Carolina Reyes", "11.111.111-1", "carolina@example.com")
    andres = registrar_cliente("Andrés Pinto", "12.345.678-5", "andres@example.com")

    # 5. Reservan (FR-11, FR-12): el total es precio × personas y se descuenta del cupo (R13, R14).
    r = http.post("/api/reservas", headers=carolina, json={"paquete_id": norte["id"], "cantidad_personas": 2})
    assert r.status_code == 201
    assert r.json()["total"] == 1_032_000
    assert http.post("/api/reservas", headers=andres,
                     json={"paquete_id": norte["id"], "cantidad_personas": 9}).status_code == 201
    assert http.get(f"/api/paquetes/publicados/{norte['id']}").json()["cupo_disponible"] == 1

    # 6. La sobreventa de la temporada pasada ya no es posible (FR-13).
    r = http.post("/api/reservas", headers=andres, json={"paquete_id": norte["id"], "cantidad_personas": 2})
    assert r.status_code == 400
    assert "cupo" in r.json()["detail"]

    # 7. Un cliente no puede tocar el catálogo (S1, RNF-03).
    assert http.delete(f"/api/destinos/{surire}", headers=carolina).status_code == 403

    # 8. El administrador sube el costo de un destino: lo ya publicado y vendido no cambia (R7, R13).
    http.put(f"/api/destinos/{surire}", headers=admin, json={"costo_base": 400_000})
    assert http.get(f"/api/paquetes/publicados/{norte['id']}").json()["precio_por_persona"] == 516_000
    assert [r["total"] for r in http.get("/api/reservas", headers=carolina).json()] == [1_032_000]

    # 9. Cada cliente ve solo su historial (FR-15, R11), y los listados no exponen RUT ni teléfono (R17).
    assert [r["cantidad_personas"] for r in http.get("/api/reservas", headers=andres).json()] == [9]
    for respuesta in (http.get("/api/reservas", headers=carolina), http.get("/api/paquetes/publicados")):
        assert "11111111" not in respuesta.text
        assert "+56 9" not in respuesta.text

    # 10. Dar de baja un destino vendido lo deja no disponible, sin borrarlo (R8, FR-03).
    assert http.delete(f"/api/destinos/{surire}", headers=admin).json()["resultado"] == "no_disponible"
    assert http.delete(f"/api/destinos/{damas}", headers=admin).json()["resultado"] == "eliminado"
    r = http.post("/api/paquetes", headers=admin, json={
        "nombre": "Otro", "fecha_salida": "2027-01-10", "fecha_regreso": "2027-01-12",
        "cupo_maximo": 5, "destino_ids": [surire, elqui]})
    assert r.status_code == 400                                          # no entra en paquetes nuevos
    assert [d["nombre"] for d in http.get(f"/api/paquetes/{norte['id']}", headers=admin).json()["destinos"]] \
        == ["Salar de Surire", "Valle del Elqui"]                        # lo vendido conserva su contenido
