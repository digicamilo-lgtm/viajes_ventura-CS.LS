import sqlite3
from datetime import date

from app.dominio import EstadoPaquete, Paquete
from app.repositorios.base import Repositorio
from app.repositorios.destino_repositorio import DestinoRepositorio


class PaqueteRepositorio(Repositorio[Paquete]):

    def __init__(self, conexion: sqlite3.Connection):
        super().__init__(conexion)
        self._destinos = DestinoRepositorio(conexion)

    def guardar(self, paquete: Paquete) -> Paquete:
        valores = (paquete.nombre, paquete.fecha_salida.isoformat(), paquete.fecha_regreso.isoformat(),
                   paquete.cupo_maximo, paquete.margen, paquete.precio_por_persona, paquete.estado.value)
        # Paquete y destinos se escriben en una sola transacción.
        with self._conexion:
            if paquete.id is None:
                cursor = self._conexion.execute(
                    "INSERT INTO paquetes (nombre, fecha_salida, fecha_regreso, cupo_maximo, margen,"
                    " precio_por_persona, estado) VALUES (?, ?, ?, ?, ?, ?, ?)", valores)
                paquete_id = cursor.lastrowid
            else:
                paquete_id = paquete.id
                self._conexion.execute(
                    "UPDATE paquetes SET nombre = ?, fecha_salida = ?, fecha_regreso = ?, cupo_maximo = ?,"
                    " margen = ?, precio_por_persona = ?, estado = ? WHERE id = ?", (*valores, paquete_id))
                self._conexion.execute("DELETE FROM paquete_destinos WHERE paquete_id = ?", (paquete_id,))
            self._conexion.executemany(
                "INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (?, ?)",
                [(paquete_id, d.id) for d in paquete.destinos])
        return self.buscar_por_id(paquete_id)

    def buscar_por_id(self, paquete_id: int) -> Paquete | None:
        fila = self._conexion.execute("SELECT * FROM paquetes WHERE id = ?", (paquete_id,)).fetchone()
        return self._a_paquete(fila) if fila else None

    def listar(self) -> list[Paquete]:
        filas = self._conexion.execute("SELECT * FROM paquetes ORDER BY fecha_salida, nombre")
        return [self._a_paquete(f) for f in filas.fetchall()]

    def listar_publicados(self, hoy: date) -> list[Paquete]:
        """Paquetes que un cliente puede ver: publicados y con salida vigente (CU-01, S2, S3)."""
        filas = self._conexion.execute(
            "SELECT * FROM paquetes WHERE estado = ? AND fecha_salida >= ? ORDER BY fecha_salida, nombre",
            (EstadoPaquete.PUBLICADO.value, hoy.isoformat()))
        return [self._a_paquete(f) for f in filas.fetchall()]

    def personas_reservadas(self, paquete_id: int) -> int:
        """Suma de personas de las reservas del paquete; base del cupo disponible (R14)."""
        fila = self._conexion.execute(
            "SELECT COALESCE(SUM(cantidad_personas), 0) FROM reservas WHERE paquete_id = ? AND cancelada = 0",
            (paquete_id,)).fetchone()
        return fila[0]

    def eliminar(self, paquete_id: int) -> None:
        with self._conexion:
            self._conexion.execute("DELETE FROM paquetes WHERE id = ?", (paquete_id,))

    def _a_paquete(self, fila: sqlite3.Row) -> Paquete:
        ids = [f["destino_id"] for f in self._conexion.execute(
            "SELECT destino_id FROM paquete_destinos WHERE paquete_id = ? ORDER BY rowid", (fila["id"],))]
        return Paquete(
            nombre=fila["nombre"],
            fecha_salida=date.fromisoformat(fila["fecha_salida"]),
            fecha_regreso=date.fromisoformat(fila["fecha_regreso"]),
            cupo_maximo=fila["cupo_maximo"],
            margen=fila["margen"],
            destinos=self._destinos.buscar_varios(ids),
            estado=EstadoPaquete(fila["estado"]),
            precio_por_persona=fila["precio_por_persona"],
            id=fila["id"],
        )
