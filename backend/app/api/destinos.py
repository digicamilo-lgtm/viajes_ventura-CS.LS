"""CRUD de destinos — HU-01 (FR-01 a FR-04)."""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.api.dependencias import obtener_administrador_actual, obtener_conexion
from app.api.esquemas import DestinoActualizacion, DestinoEntrada, DestinoSalida, ResultadoBaja
from app.dominio import Destino, NoEncontradoError, ReglaNegocioError
from app.repositorios import DestinoRepositorio

# CU-06 a CU-09: todo el catálogo de destinos es del administrador (S1, RNF-03).
router = APIRouter(prefix="/api/destinos", tags=["Destinos"],
                   dependencies=[Depends(obtener_administrador_actual)])


def repositorio(conexion: sqlite3.Connection = Depends(obtener_conexion)) -> DestinoRepositorio:
    return DestinoRepositorio(conexion)


def _buscar(repo: DestinoRepositorio, id: int) -> Destino:
    destino = repo.buscar_por_id(id)
    if destino is None:
        raise NoEncontradoError("Destino no encontrado.")
    return destino


@router.get("", response_model=list[DestinoSalida])
def listar_destinos(solo_disponibles: bool = False, repo: DestinoRepositorio = Depends(repositorio)):
    """FR-04: lista el catálogo; cada destino indica si está disponible."""
    return [DestinoSalida.desde(d) for d in repo.listar(solo_disponibles)]


@router.get("/{id}", response_model=DestinoSalida)
def obtener_destino(id: int, repo: DestinoRepositorio = Depends(repositorio)):
    return DestinoSalida.desde(_buscar(repo, id))


@router.post("", response_model=DestinoSalida, status_code=status.HTTP_201_CREATED)
def registrar_destino(datos: DestinoEntrada, repo: DestinoRepositorio = Depends(repositorio)):
    """FR-01: registra un destino con nombre único (R1) y costo base mayor que cero (R2)."""
    destino = Destino(**datos.model_dump())
    if repo.existe_nombre(destino.nombre):
        raise ReglaNegocioError("Ya existe un destino con ese nombre en el catálogo.")
    return DestinoSalida.desde(repo.guardar(destino))


@router.put("/{id}", response_model=DestinoSalida)
def modificar_destino(id: int, datos: DestinoActualizacion, repo: DestinoRepositorio = Depends(repositorio)):
    """FR-02: modifica los campos enviados. Los paquetes ya publicados conservan su precio (R7)."""
    destino = _buscar(repo, id)
    destino.actualizar(datos.model_dump(exclude_unset=True))
    if repo.existe_nombre(destino.nombre, excluir_id=id):
        raise ReglaNegocioError("Ya existe un destino con ese nombre en el catálogo.")
    return DestinoSalida.desde(repo.guardar(destino))


@router.delete("/{id}", response_model=ResultadoBaja)
def dar_de_baja_destino(id: int, repo: DestinoRepositorio = Depends(repositorio)):
    """FR-03 / R8: elimina el destino si no está en ningún paquete; si lo está, lo marca no disponible."""
    destino = _buscar(repo, id)
    if repo.esta_en_algun_paquete(id):
        destino.marcar_no_disponible()
        repo.guardar(destino)
        return ResultadoBaja(id=id, resultado="no_disponible",
                             mensaje="El destino forma parte de paquetes: se marcó como no disponible.")
    repo.eliminar(id)
    return ResultadoBaja(id=id, resultado="eliminado", mensaje="Destino eliminado del catálogo.")
