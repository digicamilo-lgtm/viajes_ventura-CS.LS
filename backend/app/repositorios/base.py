import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
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

    @contextmanager
    def transaccion_exclusiva(self) -> Iterator[None]:
        """Bloquea la escritura en la base de datos mientras se valida y se escribe.

        Sirve cuando una decisión depende de datos que otra solicitud podría
        cambiar entre la lectura y la escritura (por ejemplo, el cupo de un
        paquete, R14). BEGIN IMMEDIATE toma el bloqueo al iniciar, así que dos
        solicitudes simultáneas se atienden en serie.
        """
        self._conexion.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            if self._conexion.in_transaction:
                self._conexion.rollback()
            raise
        else:
            if self._conexion.in_transaction:
                self._conexion.commit()
