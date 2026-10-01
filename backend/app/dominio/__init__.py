"""Modelo de dominio (diagrama de clases, Figura 5 del Informe Técnico)."""
from app.dominio.cliente import Cliente
from app.dominio.destino import Destino
from app.dominio.errores import NoAutenticadoError, NoAutorizadoError, NoEncontradoError, ReglaNegocioError
from app.dominio.paquete import EstadoPaquete, Paquete
from app.dominio.reserva import Reserva
from app.dominio.usuario import Administrador, Usuario

__all__ = ["Administrador", "Cliente", "Destino", "EstadoPaquete", "NoAutenticadoError", "NoAutorizadoError",
           "NoEncontradoError", "Paquete", "ReglaNegocioError", "Reserva", "Usuario"]
