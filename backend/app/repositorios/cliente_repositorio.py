import sqlite3

from app.dominio import Cliente
from app.repositorios.base import Repositorio


class ClienteRepositorio(Repositorio[Cliente]):

    def guardar(self, cliente: Cliente) -> Cliente:
        valores = (cliente.nombre, cliente.rut, cliente.correo, cliente.telefono, cliente.hash_contrasena)
        with self._conexion:
            if cliente.id is None:
                cursor = self._conexion.execute(
                    "INSERT INTO clientes (nombre, rut, correo, telefono, hash_contrasena)"
                    " VALUES (?, ?, ?, ?, ?)", valores)
                cliente_id = cursor.lastrowid
            else:
                self._conexion.execute(
                    "UPDATE clientes SET nombre = ?, rut = ?, correo = ?, telefono = ?, hash_contrasena = ?"
                    " WHERE id = ?", (*valores, cliente.id))
                cliente_id = cliente.id
        return self.buscar_por_id(cliente_id)

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        fila = self._conexion.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        return self._a_cliente(fila) if fila else None

    def buscar_por_correo(self, correo: str) -> Cliente | None:
        """R9: el correo identifica al cliente, sin distinguir mayúsculas."""
        fila = self._conexion.execute(
            "SELECT * FROM clientes WHERE correo = ? COLLATE NOCASE", (correo.strip(),)).fetchone()
        return self._a_cliente(fila) if fila else None

    def existe_correo(self, correo: str) -> bool:
        return self.buscar_por_correo(correo) is not None

    def listar(self) -> list[Cliente]:
        return [self._a_cliente(f) for f in self._conexion.execute("SELECT * FROM clientes ORDER BY nombre")]

    @staticmethod
    def _a_cliente(fila: sqlite3.Row) -> Cliente:
        return Cliente(nombre=fila["nombre"], rut=fila["rut"], correo=fila["correo"],
                       telefono=fila["telefono"], hash_contrasena=fila["hash_contrasena"], id=fila["id"])
