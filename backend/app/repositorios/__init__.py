"""Capa de persistencia (diagrama de clases, Figura 6 del Informe Técnico)."""
from app.repositorios.base import Repositorio
from app.repositorios.destino_repositorio import DestinoRepositorio
from app.repositorios.paquete_repositorio import PaqueteRepositorio

__all__ = ["DestinoRepositorio", "PaqueteRepositorio", "Repositorio"]
