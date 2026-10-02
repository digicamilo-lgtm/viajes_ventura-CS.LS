"""Autenticación de administradores (S1, CU-03, RNF-03).

No hay registro público de administradores: se crean desde la consola con
`python -m app.crear_administrador`, para que nadie pueda darse ese rol a sí mismo.
"""
import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencias import obtener_administrador_actual, obtener_conexion
from app.api.esquemas import AdministradorSalida, CredencialesEntrada, TokenSalida
from app.dominio import Administrador, NoAutenticadoError, Usuario
from app.repositorios import AdministradorRepositorio
from app.seguridad import crear_token, simular_verificacion

router = APIRouter(prefix="/api/administradores", tags=["Administradores"])


@router.post("/sesiones", response_model=TokenSalida)
def iniciar_sesion(datos: CredencialesEntrada,
                   conexion: Annotated[sqlite3.Connection, Depends(obtener_conexion)]):
    """Mismo mensaje genérico y mismo tiempo de respuesta ante cualquier error (sección 7.1)."""
    administrador = AdministradorRepositorio(conexion).buscar_por_correo(datos.correo)
    if administrador is None:
        simular_verificacion(datos.contrasena)
        raise NoAutenticadoError("Correo o contraseña incorrectos.")
    if not administrador.verificar_contrasena(datos.contrasena):
        raise NoAutenticadoError("Correo o contraseña incorrectos.")
    return TokenSalida(token=crear_token(administrador.id, Administrador.ROL))


@router.get("/yo", response_model=AdministradorSalida)
def mi_perfil(administrador: Annotated[Usuario, Depends(obtener_administrador_actual)]):
    return AdministradorSalida.desde(administrador)
