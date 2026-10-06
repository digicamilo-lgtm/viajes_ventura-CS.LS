"""Reservar, modificar, cancelar y consultar el historial propio — HU-04 (FR-11 a FR-15, S4)."""
import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, status

from app.api.dependencias import obtener_cliente_actual, obtener_conexion, obtener_hoy
from app.api.esquemas import ReservaEntrada, ReservaModificacion, ReservaSalida
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
    # Leer el cupo y registrar la reserva en una sola transacción exclusiva: si no, dos reservas
    # simultáneas ven el mismo cupo libre y ambas se aceptan (sobreventa, R14).
    with repos.reservas.transaccion_exclusiva():
        paquete = repos.paquetes.buscar_por_id(datos.paquete_id)
        if paquete is None:
            raise NoEncontradoError("Paquete no encontrado.")
        personas_reservadas = repos.paquetes.personas_reservadas(paquete.id)
        reserva = Reserva.crear(cliente_id=cliente.id, paquete=paquete, cantidad_personas=datos.cantidad_personas,
                                personas_reservadas=personas_reservadas, hoy=hoy)
        guardada = repos.reservas.guardar(reserva)
    return ReservaSalida.desde(guardada)


@router.get("", response_model=list[ReservaSalida])
def mis_reservas(cliente: Cliente = Depends(obtener_cliente_actual), repos: Repos = Depends()):
    """FR-15: historial propio; el cliente_id sale del token, nunca de un parámetro (R11)."""
    return [ReservaSalida.desde(r) for r in repos.reservas.listar_por_cliente(cliente.id)]


def _reserva_propia(repos: Repos, reserva_id: int, cliente: Cliente) -> Reserva:
    """Una reserva ajena responde como inexistente, para no revelar qué reservas hay (R11)."""
    reserva = repos.reservas.buscar_por_id(reserva_id)
    if reserva is None or reserva.cliente_id != cliente.id:
        raise NoEncontradoError("Reserva no encontrada.")
    return reserva


@router.delete("/{reserva_id}", response_model=ReservaSalida)
def cancelar_reserva(reserva_id: int, cliente: Cliente = Depends(obtener_cliente_actual),
                     repos: Repos = Depends(), hoy: date = Depends(obtener_hoy)):
    """Cancela una reserva propia hasta el día de salida del paquete (S4). Libera su cupo."""
    with repos.reservas.transaccion_exclusiva():
        reserva = _reserva_propia(repos, reserva_id, cliente)
        paquete = repos.paquetes.buscar_por_id(reserva.paquete_id)
        reserva.cancelar(paquete, hoy)
        repos.reservas.marcar_cancelada(reserva.id)
    return ReservaSalida.desde(repos.reservas.buscar_por_id(reserva_id))


@router.put("/{reserva_id}", response_model=ReservaSalida)
def modificar_reserva(reserva_id: int, datos: ReservaModificacion,
                      cliente: Cliente = Depends(obtener_cliente_actual), repos: Repos = Depends(),
                      hoy: date = Depends(obtener_hoy)):
    """Cambia la cantidad de personas (S4): la reserva actual queda cancelada y se crea una nueva al
    precio vigente, dentro de la misma transacción y con el cupo recalculado."""
    with repos.reservas.transaccion_exclusiva():
        actual = _reserva_propia(repos, reserva_id, cliente)
        paquete = repos.paquetes.buscar_por_id(actual.paquete_id)
        personas_reservadas = repos.paquetes.personas_reservadas(paquete.id)
        nueva = actual.reemplazar_por(paquete, nueva_cantidad_personas=datos.cantidad_personas,
                                      personas_reservadas=personas_reservadas, hoy=hoy)
        repos.reservas.marcar_cancelada(actual.id)
        guardada = repos.reservas.guardar(nueva)
    return ReservaSalida.desde(guardada)
