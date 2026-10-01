import sqlite3
from collections.abc import Iterator
from datetime import date

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import conectar
from app.dominio import Cliente, NoAutenticadoError
from app.repositorios import ClienteRepositorio
from app.seguridad import decodificar_token

_esquema_bearer = HTTPBearer(auto_error=False)


def obtener_conexion() -> Iterator[sqlite3.Connection]:
    """Una conexión por solicitud, cerrada siempre al terminar."""
    conexion = conectar()
    try:
        yield conexion
    finally:
        conexion.close()


def obtener_hoy() -> date:
    """Fecha del día contra la que se comparan las salidas (R15). Se reemplaza en las pruebas."""
    return date.today()


def obtener_cliente_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_esquema_bearer),
    conexion: sqlite3.Connection = Depends(obtener_conexion),
) -> Cliente:
    """R11: exige un token de sesión válido. El cliente_id sale del token, nunca de un parámetro
    que el cliente pueda manipular (RNF-03)."""
    if credenciales is None:
        raise NoAutenticadoError("Se requiere autenticación.")
    try:
        cliente_id = decodificar_token(credenciales.credentials)
    except jwt.InvalidTokenError:
        raise NoAutenticadoError("Sesión inválida o expirada.")
    cliente = ClienteRepositorio(conexion).buscar_por_id(cliente_id)
    if cliente is None:
        raise NoAutenticadoError("Sesión inválida o expirada.")
    return cliente
