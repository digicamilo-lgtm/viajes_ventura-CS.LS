import sqlite3
from datetime import date

from app.dominio import Reserva
from app.repositorios.base import Repositorio


class ReservaRepositorio(Repositorio[Reserva]):
    """Una reserva no cambia su total ni sus integrantes (R13); solo puede marcarse como cancelada."""

    def guardar(self, reserva: Reserva) -> Reserva:
        valores = (reserva.cliente_id, reserva.paquete_id, reserva.fecha_emision.isoformat(),
                   reserva.cantidad_personas, reserva.total, int(reserva.cancelada))
        with self._conexion:
            cursor = self._conexion.execute(
                "INSERT INTO reservas (cliente_id, paquete_id, fecha_emision, cantidad_personas, total, cancelada)"
                " VALUES (?, ?, ?, ?, ?, ?)", valores)
            reserva_id = cursor.lastrowid
        return self.buscar_por_id(reserva_id)

    def marcar_cancelada(self, reserva_id: int) -> None:
        with self._conexion:
            self._conexion.execute("UPDATE reservas SET cancelada = 1 WHERE id = ?", (reserva_id,))

    def buscar_por_id(self, reserva_id: int) -> Reserva | None:
        fila = self._conexion.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
        return self._a_reserva(fila) if fila else None

    def listar(self) -> list[Reserva]:
        filas = self._conexion.execute("SELECT * FROM reservas ORDER BY fecha_emision DESC")
        return [self._a_reserva(f) for f in filas.fetchall()]

    def listar_por_cliente(self, cliente_id: int) -> list[Reserva]:
        """FR-15: historial propio del cliente."""
        filas = self._conexion.execute(
            "SELECT * FROM reservas WHERE cliente_id = ? ORDER BY fecha_emision DESC", (cliente_id,))
        return [self._a_reserva(f) for f in filas.fetchall()]

    @staticmethod
    def _a_reserva(fila: sqlite3.Row) -> Reserva:
        return Reserva(cliente_id=fila["cliente_id"], paquete_id=fila["paquete_id"],
                       fecha_emision=date.fromisoformat(fila["fecha_emision"]),
                       cantidad_personas=fila["cantidad_personas"], total=fila["total"], id=fila["id"],
                       cancelada=bool(fila["cancelada"]))
