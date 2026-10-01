import sqlite3
from collections.abc import Iterator
from datetime import date

from app.database import conectar


def obtener_conexion() -> Iterator[sqlite3.Connection]:
    """Una conexión por solicitud, cerrada siempre al terminar."""
    conexion = conectar()
    try:
        yield conexion
    finally:
        conexion.close()


def obtener_hoy() -> date:
    """Fecha del día contra la que se comparan las salidas (R15). Se reemplaza en las pruebas."""
    return date.today()
