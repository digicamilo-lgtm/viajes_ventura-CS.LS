"""Registro, autenticación y perfil de clientes — HU-03 (FR-09 a FR-11)."""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.api.dependencias import obtener_cliente_actual, obtener_conexion
from app.api.esquemas import ClienteEntrada, ClientePerfil, CredencialesEntrada, TokenSalida
from app.dominio import Cliente, NoAutenticadoError, ReglaNegocioError
from app.repositorios import ClienteRepositorio
from app.seguridad import crear_token, hashear, verificar

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])


def repositorio(conexion: sqlite3.Connection = Depends(obtener_conexion)) -> ClienteRepositorio:
    return ClienteRepositorio(conexion)


@router.post("", response_model=ClientePerfil, status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: ClienteEntrada, repo: ClienteRepositorio = Depends(repositorio)):
    """FR-09: registra un cliente con correo único (R9) y contraseña hasheada, nunca en texto plano (R10)."""
    if repo.existe_correo(datos.correo):
        raise ReglaNegocioError("Ya existe un cliente registrado con ese correo.")
    cliente = Cliente(nombre=datos.nombre, rut=datos.rut, correo=datos.correo,
                      telefono=datos.telefono, hash_contrasena=hashear(datos.contrasena))
    return ClientePerfil.desde(repo.guardar(cliente))


@router.post("/sesiones", response_model=TokenSalida)
def iniciar_sesion(datos: CredencialesEntrada, repo: ClienteRepositorio = Depends(repositorio)):
    """FR-10: autentica por correo y contraseña; mismo mensaje genérico ante cualquier error (sección 7.1)."""
    cliente = repo.buscar_por_correo(datos.correo)
    if cliente is None or not verificar(datos.contrasena, cliente.hash_contrasena):
        raise NoAutenticadoError("Correo o contraseña incorrectos.")
    return TokenSalida(token=crear_token(cliente.id))


@router.get("/yo", response_model=ClientePerfil)
def mi_perfil(cliente: Cliente = Depends(obtener_cliente_actual)):
    """R11 / R17: el propio cliente ve sus datos completos; en ningún otro lugar se exponen RUT/teléfono."""
    return ClientePerfil.desde(cliente)
