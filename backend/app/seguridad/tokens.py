"""Emisión y verificación de tokens de sesión (R11, sección 7.1 del Informe Técnico).

JWT firmado con HS256 y expiración de 30 minutos; la clave se lee de la
variable de entorno JWT_SECRET, nunca escrita literal en el código.
"""
import os
from datetime import datetime, timedelta, timezone

import jwt

ALGORITMO = "HS256"
EXPIRACION = timedelta(minutes=30)


def _clave_secreta() -> str:
    clave = os.environ.get("JWT_SECRET")
    if not clave:
        raise RuntimeError("Falta configurar la variable de entorno JWT_SECRET.")
    return clave


def crear_token(cliente_id: int) -> str:
    ahora = datetime.now(timezone.utc)
    payload = {"sub": str(cliente_id), "iat": ahora, "exp": ahora + EXPIRACION}
    return jwt.encode(payload, _clave_secreta(), algorithm=ALGORITMO)


def decodificar_token(token: str) -> int:
    """Devuelve el id del cliente autenticado. Lanza jwt.InvalidTokenError si no es válido o expiró."""
    payload = jwt.decode(token, _clave_secreta(), algorithms=[ALGORITMO])
    return int(payload["sub"])
