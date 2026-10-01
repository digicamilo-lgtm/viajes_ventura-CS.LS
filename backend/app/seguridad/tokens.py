"""Emisión y verificación de tokens de sesión (R11, sección 7.1 del Informe Técnico).

JWT firmado con HS256 y expiración de 30 minutos; la clave se lee de la
variable de entorno JWT_SECRET, nunca escrita literal en el código. El token
lleva el rol del usuario: sin él, el cliente 1 y el administrador 1 tendrían
el mismo token.
"""
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

ALGORITMO = "HS256"
EXPIRACION = timedelta(minutes=30)
LARGO_MINIMO_CLAVE = 32      # bytes; HS256 usa una clave de 256 bits (RFC 7518, sección 3.2)
ROLES = {"cliente", "administrador"}


@dataclass(frozen=True)
class Sesion:
    usuario_id: int
    rol: str


def _clave_secreta() -> str:
    clave = os.environ.get("JWT_SECRET")
    if not clave:
        raise RuntimeError("Falta configurar la variable de entorno JWT_SECRET.")
    if len(clave.encode("utf-8")) < LARGO_MINIMO_CLAVE:
        raise RuntimeError(f"JWT_SECRET debe tener al menos {LARGO_MINIMO_CLAVE} bytes.")
    return clave


def crear_token(usuario_id: int, rol: str) -> str:
    if rol not in ROLES:
        raise ValueError(f"Rol desconocido: {rol}")
    ahora = datetime.now(timezone.utc)
    payload = {"sub": str(usuario_id), "rol": rol, "iat": ahora, "exp": ahora + EXPIRACION}
    return jwt.encode(payload, _clave_secreta(), algorithm=ALGORITMO)


def decodificar_token(token: str) -> Sesion:
    """Devuelve la sesión del token. Lanza jwt.InvalidTokenError si no es válido, expiró o no trae rol."""
    payload = jwt.decode(token, _clave_secreta(), algorithms=[ALGORITMO],
                         options={"require": ["exp", "sub", "rol"]})
    if payload["rol"] not in ROLES:
        raise jwt.InvalidTokenError("Rol desconocido.")
    try:
        return Sesion(usuario_id=int(payload["sub"]), rol=payload["rol"])
    except ValueError as exc:
        raise jwt.InvalidTokenError("Identificador inválido.") from exc
