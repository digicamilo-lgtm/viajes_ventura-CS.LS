import sqlite3
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Repositorio(ABC, Generic[T]):
    """Contrato común de persistencia (Figura 6 del Informe Técnico).

    Toda consulta de las subclases usa parámetros (?) y nunca concatena datos de
    entrada en el SQL (prevención de inyección SQL, sección 7.3).
    """

    def __init__(self, conexion: sqlite3.Connection):
        self._conexion = conexion

    @abstractmethod
    def guardar(self, entidad: T) -> T:
        """Inserta la entidad si no tiene id, o la actualiza; devuelve la entidad persistida."""

    @abstractmethod
    def buscar_por_id(self, id: int) -> T | None:
        ...

    @abstractmethod
    def listar(self) -> list[T]:
        ...
