"""Conexión a SQLite y esquema de la base de datos (sección 5.2 del Informe Técnico).

El esquema expresa las reglas de negocio que dependen solo de la forma de una
fila (UNIQUE, CHECK, NOT NULL). Las que dependen de otros datos o de la fecha
del día (R3 2..5 destinos, R8 baja lógica, R14 cupo, R15 fecha) viven en el
dominio (app/dominio/).
"""
import os
import sqlite3
from pathlib import Path

RUTA_POR_DEFECTO = Path(__file__).resolve().parent.parent / "viajes.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS destinos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL UNIQUE COLLATE NOCASE,              -- R1
    zona          TEXT    NOT NULL,
    descripcion   TEXT    NOT NULL DEFAULT '',
    duracion_dias INTEGER NOT NULL CHECK (duracion_dias > 0),
    costo_base    INTEGER NOT NULL CHECK (costo_base > 0),             -- R2
    disponible    INTEGER NOT NULL DEFAULT 1 CHECK (disponible IN (0, 1))  -- R8
);

CREATE TABLE IF NOT EXISTS paquetes (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre             TEXT    NOT NULL,
    fecha_salida       TEXT    NOT NULL,                               -- ISO 8601
    fecha_regreso      TEXT    NOT NULL,
    cupo_maximo        INTEGER NOT NULL CHECK (cupo_maximo > 0),       -- R5
    margen             REAL    NOT NULL CHECK (margen >= 0),           -- R6
    precio_por_persona INTEGER NOT NULL CHECK (precio_por_persona > 0),
    estado             TEXT    NOT NULL CHECK (estado IN ('BORRADOR', 'PUBLICADO')),  -- S2
    CHECK (fecha_regreso > fecha_salida)                               -- R5
);

-- R3/R4: relación N:N; la clave primaria impide repetir un destino en el paquete.
CREATE TABLE IF NOT EXISTS paquete_destinos (
    paquete_id INTEGER NOT NULL REFERENCES paquetes (id) ON DELETE CASCADE,
    destino_id INTEGER NOT NULL REFERENCES destinos (id),
    PRIMARY KEY (paquete_id, destino_id)
);

CREATE TABLE IF NOT EXISTS clientes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    rut             TEXT NOT NULL,
    correo          TEXT NOT NULL UNIQUE COLLATE NOCASE,               -- R9
    telefono        TEXT NOT NULL,
    hash_contrasena TEXT NOT NULL                                      -- R10
);

CREATE TABLE IF NOT EXISTS reservas (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id        INTEGER NOT NULL REFERENCES clientes (id),
    paquete_id        INTEGER NOT NULL REFERENCES paquetes (id),
    fecha_emision     TEXT    NOT NULL,                                -- R12
    cantidad_personas INTEGER NOT NULL CHECK (cantidad_personas >= 1), -- R16
    total             INTEGER NOT NULL CHECK (total > 0)               -- R13
);
"""


def ruta_base_datos() -> Path:
    """Ruta del archivo SQLite; se puede cambiar con la variable de entorno VIAJES_DB."""
    return Path(os.environ.get("VIAJES_DB", RUTA_POR_DEFECTO))


def conectar(ruta: Path | str | None = None) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta or ruta_base_datos(), check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_esquema(conexion: sqlite3.Connection) -> None:
    conexion.executescript(ESQUEMA)
