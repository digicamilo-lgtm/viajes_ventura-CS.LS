import sqlite3

from app.dominio import Administrador
from app.repositorios.base import Repositorio


class AdministradorRepositorio(Repositorio[Administrador]):

    def guardar(self, administrador: Administrador) -> Administrador:
        valores = (administrador.nombre, administrador.correo, administrador.hash_contrasena)
        with self._conexion:
            if administrador.id is None:
                cursor = self._conexion.execute(
                    "INSERT INTO administradores (nombre, correo, hash_contrasena) VALUES (?, ?, ?)", valores)
                administrador_id = cursor.lastrowid
            else:
                self._conexion.execute(
                    "UPDATE administradores SET nombre = ?, correo = ?, hash_contrasena = ? WHERE id = ?",
                    (*valores, administrador.id))
                administrador_id = administrador.id
        return self.buscar_por_id(administrador_id)

    def buscar_por_id(self, administrador_id: int) -> Administrador | None:
        fila = self._conexion.execute("SELECT * FROM administradores WHERE id = ?", (administrador_id,)).fetchone()
        return self._a_administrador(fila) if fila else None

    def buscar_por_correo(self, correo: str) -> Administrador | None:
        fila = self._conexion.execute(
            "SELECT * FROM administradores WHERE correo = ? COLLATE NOCASE", (correo.strip(),)).fetchone()
        return self._a_administrador(fila) if fila else None

    def listar(self) -> list[Administrador]:
        filas = self._conexion.execute("SELECT * FROM administradores ORDER BY nombre")
        return [self._a_administrador(f) for f in filas.fetchall()]

    @staticmethod
    def _a_administrador(fila: sqlite3.Row) -> Administrador:
        return Administrador(nombre=fila["nombre"], correo=fila["correo"],
                             hash_contrasena=fila["hash_contrasena"], id=fila["id"])
