"""CRUD de paquetes — HU-02 (FR-05 a FR-08)."""
import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, Response, status

from app.api.dependencias import obtener_conexion, obtener_hoy
from app.api.esquemas import PaqueteActualizacion, PaqueteEntrada, PaqueteSalida
from app.dominio import Destino, NoEncontradoError, Paquete
from app.repositorios import DestinoRepositorio, PaqueteRepositorio

router = APIRouter(prefix="/api/paquetes", tags=["Paquetes"])


class Repos:
    def __init__(self, conexion: sqlite3.Connection = Depends(obtener_conexion)):
        self.paquetes = PaqueteRepositorio(conexion)
        self.destinos = DestinoRepositorio(conexion)

    def buscar(self, id: int) -> Paquete:
        paquete = self.paquetes.buscar_por_id(id)
        if paquete is None:
            raise NoEncontradoError("Paquete no encontrado.")
        return paquete

    def resolver_destinos(self, ids: list[int]) -> list[Destino]:
        destinos = self.destinos.buscar_varios(ids)
        faltantes = sorted(set(ids) - {d.id for d in destinos})
        if faltantes:
            raise NoEncontradoError(f"Destinos no encontrados: {', '.join(map(str, faltantes))}.")
        return destinos

    def salida(self, paquete: Paquete, hoy: date) -> PaqueteSalida:
        return PaqueteSalida.desde(paquete, self.paquetes.personas_reservadas(paquete.id), hoy)


@router.get("", response_model=list[PaqueteSalida])
def listar_paquetes(repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """Todos los paquetes, en borrador y publicados (vista del administrador)."""
    return [repos.salida(p, hoy) for p in repos.paquetes.listar()]


@router.get("/publicados", response_model=list[PaqueteSalida])
def listar_publicados(repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """CU-01 / FR-08: paquetes publicados con salida vigente, con su precio y cupo disponible."""
    return [repos.salida(p, hoy) for p in repos.paquetes.listar_publicados(hoy)]


@router.get("/{id}", response_model=PaqueteSalida)
def obtener_paquete(id: int, repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    return repos.salida(repos.buscar(id), hoy)


@router.post("", response_model=PaqueteSalida, status_code=status.HTTP_201_CREATED)
def crear_paquete(datos: PaqueteEntrada, repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """FR-05 / FR-06: arma el paquete en borrador; el precio lo calcula el sistema."""
    paquete = Paquete.crear(
        nombre=datos.nombre, fecha_salida=datos.fecha_salida, fecha_regreso=datos.fecha_regreso,
        cupo_maximo=datos.cupo_maximo, margen=datos.margen,
        destinos=repos.resolver_destinos(datos.destino_ids))
    return repos.salida(repos.paquetes.guardar(paquete), hoy)


@router.put("/{id}", response_model=PaqueteSalida)
def modificar_paquete(id: int, datos: PaqueteActualizacion, repos: Repos = Depends(),
                      hoy: date = Depends(obtener_hoy)):
    """Modifica un paquete en borrador; uno publicado conserva sus datos y su precio (R7)."""
    paquete = repos.buscar(id)
    cambios = datos.model_dump(exclude_unset=True)
    ids = cambios.pop("destino_ids", None)
    paquete.modificar(cambios, repos.resolver_destinos(ids) if ids is not None else None)
    return repos.salida(repos.paquetes.guardar(paquete), hoy)


@router.post("/{id}/publicar", response_model=PaqueteSalida)
def publicar_paquete(id: int, repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """FR-07: fija el precio con los costos vigentes y deja el paquete disponible para reservas."""
    paquete = repos.buscar(id)
    paquete.publicar()
    return repos.salida(repos.paquetes.guardar(paquete), hoy)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paquete(id: int, repos: Repos = Depends()):
    """Elimina un paquete en borrador. Los publicados se conservan por el historial de reservas (S3)."""
    repos.buscar(id).verificar_editable()
    repos.paquetes.eliminar(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
