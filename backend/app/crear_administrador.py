"""Crea una cuenta de administrador desde la consola (S1).

Uso, desde la carpeta backend/:
    python -m app.crear_administrador --nombre "Paulina Ovalle" --correo paulina@viajesaventura.cl

La contraseña se pide sin mostrarla en pantalla y nunca pasa por la línea de
comandos, donde quedaría en el historial de la terminal.
"""
import argparse
import getpass
import sys

from app.database import conectar, crear_esquema
from app.dominio import Administrador, ReglaNegocioError
from app.repositorios import AdministradorRepositorio
from app.seguridad import hashear

LARGO_MINIMO = 12


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crea una cuenta de administrador de Viajes Aventura.")
    parser.add_argument("--nombre", required=True)
    parser.add_argument("--correo", required=True)
    args = parser.parse_args(argv)

    contrasena = getpass.getpass("Contraseña: ")
    if len(contrasena) < LARGO_MINIMO:
        print(f"La contraseña debe tener al menos {LARGO_MINIMO} caracteres.", file=sys.stderr)
        return 1
    if getpass.getpass("Repite la contraseña: ") != contrasena:
        print("Las contraseñas no coinciden.", file=sys.stderr)
        return 1

    conexion = conectar()
    try:
        crear_esquema(conexion)
        repo = AdministradorRepositorio(conexion)
        if repo.buscar_por_correo(args.correo):
            print("Ya existe un administrador con ese correo.", file=sys.stderr)
            return 1
        administrador = repo.guardar(
            Administrador(nombre=args.nombre, correo=args.correo, hash_contrasena=hashear(contrasena)))
    except ReglaNegocioError as exc:
        print(exc, file=sys.stderr)
        return 1
    finally:
        conexion.close()
    print(f"Administrador creado: {administrador.correo} (id {administrador.id}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
