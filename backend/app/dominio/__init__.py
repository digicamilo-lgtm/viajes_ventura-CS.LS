"""Modelo de dominio (diagrama de clases, Figura 5 del Informe Técnico)."""
from app.dominio.cliente import Cliente
from app.dominio.destino import Destino
from app.dominio.errores import NoAutenticadoError, NoEncontradoError, ReglaNegocioError
from app.dominio.paquete import EstadoPaquete, Paquete
from app.dominio.reserva import Reserva

__all__ = ["Cliente", "Destino", "EstadoPaquete", "NoAutenticadoError", "NoEncontradoError",
           "Paquete", "ReglaNegocioError", "Reserva"]
