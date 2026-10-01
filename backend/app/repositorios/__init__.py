"""Capa de persistencia (diagrama de clases, Figura 6 del Informe Técnico)."""
from app.repositorios.administrador_repositorio import AdministradorRepositorio
from app.repositorios.base import Repositorio
from app.repositorios.cliente_repositorio import ClienteRepositorio
from app.repositorios.destino_repositorio import DestinoRepositorio
from app.repositorios.paquete_repositorio import PaqueteRepositorio
from app.repositorios.reserva_repositorio import ReservaRepositorio

__all__ = ["AdministradorRepositorio", "ClienteRepositorio", "DestinoRepositorio", "PaqueteRepositorio",
           "Repositorio", "ReservaRepositorio"]
