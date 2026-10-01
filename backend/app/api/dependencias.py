import sqlite3
from collections.abc import Iterator
from datetime import date

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import conectar
from app.dominio import Cliente, NoAutenticadoError, NoAutorizadoError, Usuario
from app.repositorios import AdministradorRepositorio, ClienteRepositorio
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


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_esquema_bearer),
    conexion: sqlite3.Connection = Depends(obtener_conexion),
) -> Usuario:
    """Exige un token de sesión válido y devuelve el Cliente o el Administrador que lo emitió.

    El id y el rol salen del token firmado, nunca de un parámetro que el usuario pueda
    manipular (R11, RNF-03).
    """
    if credenciales is None:
        raise NoAutenticadoError("Se requiere autenticación.")
    try:
        sesion = decodificar_token(credenciales.credentials)
    except jwt.InvalidTokenError:
        raise NoAutenticadoError("Sesión inválida o expirada.")
    repositorio = ClienteRepositorio(conexion) if sesion.rol == Cliente.ROL else AdministradorRepositorio(conexion)
    usuario = repositorio.buscar_por_id(sesion.usuario_id)
    if usuario is None:
        raise NoAutenticadoError("Sesión inválida o expirada.")
    return usuario


def obtener_cliente_actual(usuario: Usuario = Depends(obtener_usuario_actual)) -> Cliente:
    """R11: reservar y consultar reservas es exclusivo de un cliente autenticado."""
    if not isinstance(usuario, Cliente):
        raise NoAutorizadoError("Esta operación es solo para clientes.")
    return usuario


def obtener_administrador_actual(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
    """S1 / RNF-03: solo quien puede gestionar el catálogo modifica destinos y paquetes.

    Se le pregunta al usuario (polimorfismo) en vez de revisar su tipo concreto.
    """
    if not usuario.puede_gestionar_catalogo():
        raise NoAutorizadoError("Esta operación es solo para administradores.")
    return usuario
