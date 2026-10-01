import sqlite3

from app.dominio import Destino
from app.repositorios.base import Repositorio


class DestinoRepositorio(Repositorio[Destino]):

    def guardar(self, destino: Destino) -> Destino:
        valores = (destino.nombre, destino.zona, destino.descripcion, destino.duracion_dias,
                   destino.costo_base, int(destino.disponible))
        with self._conexion:
            if destino.id is None:
                cursor = self._conexion.execute(
                    "INSERT INTO destinos (nombre, zona, descripcion, duracion_dias, costo_base, disponible)"
                    " VALUES (?, ?, ?, ?, ?, ?)", valores)
                id = cursor.lastrowid
            else:
                self._conexion.execute(
                    "UPDATE destinos SET nombre = ?, zona = ?, descripcion = ?, duracion_dias = ?,"
                    " costo_base = ?, disponible = ? WHERE id = ?", (*valores, destino.id))
                id = destino.id
        return self.buscar_por_id(id)

    def buscar_por_id(self, id: int) -> Destino | None:
        fila = self._conexion.execute("SELECT * FROM destinos WHERE id = ?", (id,)).fetchone()
        return self._a_destino(fila) if fila else None

    def buscar_varios(self, ids: list[int]) -> list[Destino]:
        """Devuelve los destinos en el mismo orden de ids; omite los que no existen."""
        encontrados = {d.id: d for d in (self.buscar_por_id(i) for i in set(ids)) if d}
        return [encontrados[i] for i in ids if i in encontrados]

    def listar(self, solo_disponibles: bool = False) -> list[Destino]:
        sql = "SELECT * FROM destinos"
        if solo_disponibles:
            sql += " WHERE disponible = 1"
        return [self._a_destino(f) for f in self._conexion.execute(sql + " ORDER BY nombre")]

    def existe_nombre(self, nombre: str, excluir_id: int | None = None) -> bool:
        """R1: el nombre no se repite (sin distinguir mayúsculas)."""
        fila = self._conexion.execute(
            "SELECT 1 FROM destinos WHERE nombre = ? COLLATE NOCASE AND id IS NOT ?",
            (nombre.strip(), excluir_id)).fetchone()
        return fila is not None

    def esta_en_algun_paquete(self, id: int) -> bool:
        """R8: decide entre eliminar el destino o marcarlo no disponible."""
        fila = self._conexion.execute(
            "SELECT 1 FROM paquete_destinos WHERE destino_id = ? LIMIT 1", (id,)).fetchone()
        return fila is not None

    def eliminar(self, id: int) -> None:
        with self._conexion:
            self._conexion.execute("DELETE FROM destinos WHERE id = ?", (id,))

    @staticmethod
    def _a_destino(fila: sqlite3.Row) -> Destino:
        return Destino(nombre=fila["nombre"], zona=fila["zona"], descripcion=fila["descripcion"],
                       duracion_dias=fila["duracion_dias"], costo_base=fila["costo_base"],
                       disponible=bool(fila["disponible"]), id=fila["id"])
