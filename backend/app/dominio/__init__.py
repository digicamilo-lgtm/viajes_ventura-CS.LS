"""Modelo de dominio (diagrama de clases, Figura 5 del Informe Técnico)."""
from app.dominio.destino import Destino
from app.dominio.errores import NoEncontradoError, ReglaNegocioError
from app.dominio.paquete import EstadoPaquete, Paquete

__all__ = ["Destino", "EstadoPaquete", "NoEncontradoError", "Paquete", "ReglaNegocioError"]
