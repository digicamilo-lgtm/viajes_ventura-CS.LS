"""Reservar un paquete y consultar historial propio — HU-04 (FR-11 a FR-15)."""
import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, status

from app.api.dependencias import obtener_cliente_actual, obtener_conexion, obtener_hoy
from app.api.esquemas import ReservaEntrada, ReservaSalida
from app.dominio import Cliente, NoEncontradoError, Reserva
from app.repositorios import PaqueteRepositorio, ReservaRepositorio

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


class Repos:
    def __init__(self, conexion: sqlite3.Connection = Depends(obtener_conexion)):
        self.reservas = ReservaRepositorio(conexion)
        self.paquetes = PaqueteRepositorio(conexion)


@router.post("", response_model=ReservaSalida, status_code=status.HTTP_201_CREATED)
def reservar_paquete(datos: ReservaEntrada, cliente: Cliente = Depends(obtener_cliente_actual),
                     repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """FR-12 a FR-14: valida que el paquete esté publicado y vigente y que haya cupo, calcula el
    total y registra la reserva. Requiere autenticación (R11)."""
    paquete = repos.paquetes.buscar_por_id(datos.paquete_id)
    if paquete is None:
        raise NoEncontradoError("Paquete no encontrado.")
    personas_reservadas = repos.paquetes.personas_reservadas(paquete.id)
    reserva = Reserva.crear(cliente_id=cliente.id, paquete=paquete, cantidad_personas=datos.cantidad_personas,
                            personas_reservadas=personas_reservadas, hoy=hoy)
    return ReservaSalida.desde(repos.reservas.guardar(reserva))


@router.get("", response_model=list[ReservaSalida])
def mis_reservas(cliente: Cliente = Depends(obtener_cliente_actual), repos: Repos = Depends()):
    """FR-15: historial propio; el cliente_id sale del token, nunca de un parámetro (R11)."""
    return [ReservaSalida.desde(r) for r in repos.reservas.listar_por_cliente(cliente.id)]
