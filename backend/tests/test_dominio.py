"""Pruebas unitarias del modelo de dominio, sin base de datos."""
from datetime import date

import pytest

from app.dominio import Cliente, Destino, EstadoPaquete, Paquete, ReglaNegocioError, Reserva

SALIDA, REGRESO = date(2026, 12, 10), date(2026, 12, 15)


def destinos_caso():
    surire = Destino("Salar de Surire", "Región de Arica y Parinacota", "", 3, 310_000, id=1)
    elqui = Destino("Valle del Elqui", "Región de Coquimbo", "", 2, 120_000, id=2)
    return surire, elqui


def norte_grande(**cambios):
    datos = dict(nombre="Norte Grande en 5 días", fecha_salida=SALIDA, fecha_regreso=REGRESO,
                 cupo_maximo=12, margen=0.20, destinos=list(destinos_caso()))
    datos.update(cambios)
    return Paquete.crear(**datos)


# --- Destino -------------------------------------------------------------
@pytest.mark.parametrize("campo, valor", [
    ("costo_base", 0), ("costo_base", -5), ("duracion_dias", 0), ("costo_base", 10.5), ("nombre", "   "),
])
def test_destino_rechaza_datos_invalidos(campo, valor):            # R1, R2
    datos = dict(nombre="Isla Damas", zona="Coquimbo", descripcion="", duracion_dias=1, costo_base=38_000)
    datos[campo] = valor
    with pytest.raises(ReglaNegocioError):
        Destino(**datos)


def test_destino_actualizar_invalido_no_deja_cambios_a_medias():
    surire, _ = destinos_caso()
    with pytest.raises(ReglaNegocioError):
        surire.actualizar({"zona": "Otra zona", "costo_base": 0})
    assert surire.zona == "Región de Arica y Parinacota"
    assert surire.costo_base == 310_000


def test_destino_no_permite_cambiar_disponibilidad_por_actualizar():
    surire, _ = destinos_caso()
    with pytest.raises(ReglaNegocioError):
        surire.actualizar({"disponible": False})
    surire.marcar_no_disponible()                                    # R8
    assert surire.disponible is False


# --- Paquete: creación y precio -----------------------------------------
def test_precio_es_suma_de_costos_mas_margen():                     # R6, FR-06
    assert norte_grande().precio_por_persona == 516_000              # (310.000 + 120.000) × 1,20


def test_precio_redondea_a_pesos_enteros():                          # S6
    cajon = Destino("Cajón del Maipo", "RM", "", 1, 45_000, id=3)
    damas = Destino("Isla Damas", "Coquimbo", "", 1, 38_001, id=4)
    paquete = norte_grande(destinos=[cajon, damas], margen=0.15)
    assert paquete.precio_por_persona == 95_451                      # 83.001 × 1,15 = 95.451,15


def test_precio_no_pierde_un_peso_por_error_de_float():              # S6
    cajon = Destino("Cajón del Maipo", "RM", "", 1, 45_000, id=3)
    damas = Destino("Isla Damas", "Coquimbo", "", 1, 38_000, id=4)
    # En float, 83.000 × 1,15 = 95449.99999999999; truncarlo cobraría 95.449.
    assert norte_grande(destinos=[cajon, damas], margen=0.15).precio_por_persona == 95_450


@pytest.mark.parametrize("cambios, mensaje", [
    ({"destinos": [destinos_caso()[0]]}, "entre 2 y 5"),                               # R3
    ({"destinos": [Destino(f"D{i}", "Z", "", 1, 1_000, id=i) for i in range(10, 16)]}, "entre 2 y 5"),
    ({"destinos": [destinos_caso()[0], destinos_caso()[0]]}, "repetir"),              # R3
    ({"fecha_regreso": SALIDA}, "posterior"),                                          # R5
    ({"cupo_maximo": 0}, "cupo"),                                                      # R5
    ({"margen": -0.1}, "negativo"),                                                    # R6
    ({"margen": float("nan")}, "negativo"),
])
def test_paquete_rechaza_reglas_incumplidas(cambios, mensaje):
    with pytest.raises(ReglaNegocioError, match=mensaje):
        norte_grande(**cambios)


def test_paquete_nuevo_no_admite_destinos_no_disponibles():         # R8
    surire, elqui = destinos_caso()
    elqui.marcar_no_disponible()
    with pytest.raises(ReglaNegocioError, match="no disponibles"):
        norte_grande(destinos=[surire, elqui])


# --- Paquete: publicación (R7) ------------------------------------------
def test_publicar_fija_el_precio_ante_cambios_de_costo():           # R7, FR-07
    surire, elqui = destinos_caso()
    borrador = norte_grande(destinos=[surire, elqui])
    publicado = norte_grande(destinos=[surire, elqui])
    publicado.publicar()

    surire.actualizar({"costo_base": 400_000})

    assert publicado.estado is EstadoPaquete.PUBLICADO
    assert publicado.precio_por_persona == 516_000       # conserva el precio publicado
    assert borrador.precio_por_persona == 624_000        # el borrador sigue los costos vigentes


def test_paquete_publicado_no_se_modifica_ni_se_publica_dos_veces():
    paquete = norte_grande()
    paquete.publicar()
    with pytest.raises(ReglaNegocioError):
        paquete.publicar()
    with pytest.raises(ReglaNegocioError):
        paquete.modificar({"cupo_maximo": 20})


def test_modificar_valida_todo_antes_de_asignar():
    paquete = norte_grande()
    with pytest.raises(ReglaNegocioError):
        paquete.modificar({"nombre": "Otro", "cupo_maximo": -1})
    assert paquete.nombre == "Norte Grande en 5 días"


# --- Paquete: cupo y vencimiento -----------------------------------------
def test_cupo_disponible_descuenta_personas_reservadas():           # R14, FR-08
    assert norte_grande().cupo_disponible(personas_reservadas=5) == 7


@pytest.mark.parametrize("hoy, vencido", [
    (date(2026, 12, 9), False), (date(2026, 12, 10), False), (date(2026, 12, 11), True),
])
def test_esta_vencido_compara_con_la_fecha_del_dia(hoy, vencido):   # R15
    assert norte_grande().esta_vencido(hoy) is vencido


# --- Cliente ---------------------------------------------------------------
def test_cliente_normaliza_el_correo():                             # R9
    c = Cliente("Carolina Reyes", "11111111-1", "  Carolina@Example.COM ", "+56911111111", "hash-x")
    assert c.correo == "carolina@example.com"


@pytest.mark.parametrize("campo, valor", [
    ("nombre", "   "), ("rut", ""), ("correo", "no-es-un-correo"), ("telefono", ""),
])
def test_cliente_rechaza_datos_invalidos(campo, valor):              # R9
    datos = dict(nombre="Carolina Reyes", rut="11111111-1", correo="carolina@example.com",
                 telefono="+56911111111", hash_contrasena="hash-x")
    datos[campo] = valor
    with pytest.raises(ReglaNegocioError):
        Cliente(**datos)


def test_cliente_nunca_guarda_la_contrasena_en_texto_plano():        # R10
    # El dominio solo exige que llegue ya hasheada; hashear la contraseña es responsabilidad
    # de app.seguridad (ver test_seguridad.py), nunca del objeto Cliente.
    c = Cliente("Carolina Reyes", "11111111-1", "carolina@example.com", "+56911111111", "$2b$12$...")
    assert c.hash_contrasena != "clave-en-texto-plano"


# --- Reserva ---------------------------------------------------------------
def publicado(**cambios):
    """Un paquete publicado con id (como lo devolvería el repositorio tras guardarlo)."""
    datos = dict(nombre="Norte Grande en 5 días", fecha_salida=SALIDA, fecha_regreso=REGRESO,
                 cupo_maximo=12, margen=0.20, destinos=list(destinos_caso()))
    datos.update(cambios)
    p = Paquete(id=100, **datos)
    p.publicar()
    return p


def test_reserva_calcula_el_total_al_momento_de_reservar():          # R12, R13
    paquete = publicado()
    reserva = Reserva.crear(cliente_id=1, paquete=paquete, cantidad_personas=2,
                            personas_reservadas=0, hoy=date(2026, 11, 1))
    assert reserva.total == 1_032_000             # 516.000 × 2
    assert reserva.fecha_emision == date(2026, 11, 1)


def test_reserva_no_cambia_si_el_precio_del_paquete_cambia_despues():  # R13, R7
    paquete = publicado()
    reserva = Reserva.crear(cliente_id=1, paquete=paquete, cantidad_personas=1,
                            personas_reservadas=0, hoy=date(2026, 11, 1))
    paquete.destinos[0].actualizar({"costo_base": 999_999})
    assert reserva.total == 516_000               # no vuelve a calcularse


def test_reserva_rechaza_paquete_no_publicado():                     # FR-12
    borrador = norte_grande()
    hoy = date(2026, 11, 1)
    with pytest.raises(ReglaNegocioError, match="publicado"):
        Reserva.crear(cliente_id=1, paquete=borrador, cantidad_personas=1,
                      personas_reservadas=0, hoy=hoy)


def test_reserva_rechaza_paquete_vencido():                          # R15
    paquete = publicado()
    hoy = date(2026, 12, 11)
    with pytest.raises(ReglaNegocioError, match="ya pasó"):
        Reserva.crear(cliente_id=1, paquete=paquete, cantidad_personas=1,
                      personas_reservadas=0, hoy=hoy)


def test_reserva_rechaza_si_supera_el_cupo_disponible():             # R14
    paquete = publicado(cupo_maximo=5)
    hoy = date(2026, 11, 1)
    with pytest.raises(ReglaNegocioError, match="cupo"):
        Reserva.crear(cliente_id=1, paquete=paquete, cantidad_personas=3,
                      personas_reservadas=3, hoy=hoy)


@pytest.mark.parametrize("personas", [0, -1])
def test_reserva_rechaza_menos_de_una_persona(personas):             # R16
    paquete = publicado()
    hoy = date(2026, 11, 1)
    with pytest.raises(ReglaNegocioError, match="al menos uno"):
        Reserva.crear(cliente_id=1, paquete=paquete, cantidad_personas=personas,
                      personas_reservadas=0, hoy=hoy)


# --- Usuario, Cliente y Administrador (herencia y polimorfismo, Figura 5) -------
from app.dominio import Administrador, Usuario  # noqa: E402


def test_usuario_es_abstracto():
    with pytest.raises(TypeError):
        Usuario("X", "x@x.cl", "hash")


def test_solo_el_administrador_puede_gestionar_el_catalogo():          # polimorfismo, S1
    usuarios = [Cliente("Carolina Reyes", "11111111-1", "c@x.cl", "+569", "hash"),
                Administrador("Paulina Ovalle", "p@x.cl", "hash")]
    assert [u.puede_gestionar_catalogo() for u in usuarios] == [False, True]
    assert all(isinstance(u, Usuario) for u in usuarios)


def test_verificar_contrasena_se_hereda_de_usuario():
    from app.seguridad import hashear
    admin = Administrador("Paulina Ovalle", "p@x.cl", hashear("clave-segura-1"))
    assert admin.verificar_contrasena("clave-segura-1") is True
    assert admin.verificar_contrasena("otra") is False


def test_datos_publicos_no_incluyen_rut_ni_telefono():               # R17
    c = Cliente("Carolina Reyes", "11111111-1", "c@x.cl", "+56911111111", "hash", id=3)
    assert c.datos_publicos() == {"id": 3, "nombre": "Carolina Reyes", "correo": "c@x.cl"}


@pytest.mark.parametrize("rut, normalizado", [
    ("11111111-1", "11111111-1"), ("11.111.111-1", "11111111-1"), ("111111111", "11111111-1"),
    ("12.345.678-5", "12345678-5"), ("10.000.013-k", "10000013-K"), ("1-9", "1-9"),
])
def test_rut_valido_se_normaliza(rut, normalizado):
    assert Cliente("C", rut, "c@x.cl", "+569", "hash").rut == normalizado


@pytest.mark.parametrize("rut", ["11111111-2", "12345678-K", "abc", "", "123456789-0", "1-"])
def test_rut_invalido_se_rechaza_sin_repetirlo(rut):                  # R17: el error no expone el dato
    with pytest.raises(ReglaNegocioError) as error:
        Cliente("C", rut, "c@x.cl", "+569", "hash")
    assert rut == "" or rut not in str(error.value)
