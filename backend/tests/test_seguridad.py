"""Pruebas de hash de contraseñas y tokens de sesión (sección 7.1 del Informe Técnico)."""
import jwt
import pytest

from app.dominio import ReglaNegocioError
from app.seguridad import Sesion, crear_token, decodificar_token, hashear, simular_verificacion, verificar


def test_hashear_nunca_devuelve_la_contrasena_en_texto_plano():    # R10
    hash_resultante = hashear("clave-segura-1")
    assert hash_resultante != "clave-segura-1"
    assert verificar("clave-segura-1", hash_resultante) is True
    assert verificar("otra-clave", hash_resultante) is False


def test_hashear_dos_veces_la_misma_contrasena_da_hashes_distintos():  # sal aleatoria
    primer_hash = hashear("clave-segura-1")
    segundo_hash = hashear("clave-segura-1")
    assert primer_hash != segundo_hash


def test_hashear_rechaza_contrasena_demasiado_larga():
    with pytest.raises(ReglaNegocioError):
        hashear("x" * 100)


def test_token_viaja_y_vuelve_con_el_mismo_id(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "clave-de-pruebas-de-al-menos-32-bytes")
    token = crear_token(7, "cliente")
    assert decodificar_token(token) == Sesion(usuario_id=7, rol="cliente")


def test_token_firmado_con_otra_clave_se_rechaza(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "clave-de-pruebas-de-al-menos-32-bytes")
    token = crear_token(7, "cliente")
    monkeypatch.setenv("JWT_SECRET", "otra-clave-distinta-de-al-menos-32-bytes")
    with pytest.raises(jwt.InvalidTokenError):
        decodificar_token(token)


def test_token_requiere_la_variable_de_entorno(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.raises(RuntimeError):
        crear_token(1, "cliente")


# --- Cambio 9: revisión de seguridad del sistema integrado (sección 7.3) ----
CLAVE = "clave-de-pruebas-de-al-menos-32-bytes"


def test_token_sin_rol_se_rechaza(monkeypatch):
    """Sin rol, el token del cliente 1 serviría también como token del administrador 1."""
    monkeypatch.setenv("JWT_SECRET", CLAVE)
    token = jwt.encode({"sub": "1", "exp": 9_999_999_999}, CLAVE, algorithm="HS256")
    with pytest.raises(jwt.InvalidTokenError):
        decodificar_token(token)


def test_token_con_rol_inventado_se_rechaza(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", CLAVE)
    token = jwt.encode({"sub": "1", "rol": "superusuario", "exp": 9_999_999_999}, CLAVE, algorithm="HS256")
    with pytest.raises(jwt.InvalidTokenError):
        decodificar_token(token)


def test_token_sin_firma_se_rechaza(monkeypatch):
    """Un token con algoritmo "none" no se acepta: el algoritmo está fijado en HS256."""
    monkeypatch.setenv("JWT_SECRET", CLAVE)
    token = jwt.encode({"sub": "1", "rol": "administrador", "exp": 9_999_999_999}, None, algorithm="none")
    with pytest.raises(jwt.InvalidTokenError):
        decodificar_token(token)


def test_clave_jwt_corta_se_rechaza(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "corta")
    with pytest.raises(RuntimeError, match="32 bytes"):
        crear_token(1, "cliente")


def test_simular_verificacion_ejecuta_bcrypt(monkeypatch):
    """Un correo inexistente gasta el mismo trabajo de bcrypt que uno existente (sección 7.1)."""
    import bcrypt
    llamadas = []
    original = bcrypt.checkpw
    monkeypatch.setattr(bcrypt, "checkpw", lambda *a: llamadas.append(1) or original(*a))
    simular_verificacion("cualquier-clave")
    assert llamadas == [1]
