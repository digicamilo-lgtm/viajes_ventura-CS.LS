import math
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum

from app.dominio.destino import Destino
from app.dominio.errores import ReglaNegocioError

MIN_DESTINOS, MAX_DESTINOS = 2, 5     # R3


class EstadoPaquete(str, Enum):
    BORRADOR = "BORRADOR"
    PUBLICADO = "PUBLICADO"


class Paquete:
    """Combinación de 2 a 5 destinos con fechas, cupo y margen. Reglas R3 a R8 y R14/R15.

    Mientras está en BORRADOR el precio se recalcula con los costos vigentes de sus
    destinos; al publicarlo queda fijado y ya no cambia (R7).
    """

    def __init__(self, nombre: str, fecha_salida: date, fecha_regreso: date, cupo_maximo: int,
                 margen: float, destinos: list[Destino],
                 estado: EstadoPaquete = EstadoPaquete.BORRADOR,
                 precio_por_persona: int | None = None, id: int | None = None):
        self._id = id
        self._estado = EstadoPaquete(estado)
        self._asignar(nombre, fecha_salida, fecha_regreso, cupo_maximo, margen, destinos)
        if self._estado is EstadoPaquete.PUBLICADO:
            if not precio_por_persona or precio_por_persona <= 0:
                raise ReglaNegocioError("Un paquete publicado debe tener su precio fijado.")
            self._precio_por_persona = precio_por_persona
        else:
            self._precio_por_persona = None

    @classmethod
    def crear(cls, nombre: str, fecha_salida: date, fecha_regreso: date, cupo_maximo: int,
              margen: float, destinos: list[Destino]) -> "Paquete":
        """Arma un paquete nuevo en BORRADOR. Solo admite destinos disponibles (R8)."""
        cls._validar_disponibles(destinos)
        return cls(nombre, fecha_salida, fecha_regreso, cupo_maximo, margen, destinos)

    # --- consultas -------------------------------------------------------
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def fecha_salida(self) -> date:
        return self._fecha_salida

    @property
    def fecha_regreso(self) -> date:
        return self._fecha_regreso

    @property
    def cupo_maximo(self) -> int:
        return self._cupo_maximo

    @property
    def margen(self) -> float:
        return self._margen

    @property
    def destinos(self) -> tuple[Destino, ...]:
        return tuple(self._destinos)

    @property
    def estado(self) -> EstadoPaquete:
        return self._estado

    @property
    def precio_por_persona(self) -> int:
        """Precio fijado si está publicado (R7); si no, el que resulta de los costos vigentes."""
        if self._estado is EstadoPaquete.PUBLICADO:
            return self._precio_por_persona
        return self.calcular_precio()

    def calcular_precio(self) -> int:
        """Suma de los costos base de los destinos más el margen (R6, FR-06), en CLP enteros (S6)."""
        suma = sum(d.costo_base for d in self._destinos)
        precio = Decimal(suma) * (Decimal(1) + Decimal(str(self._margen)))
        return int(precio.quantize(Decimal(1), rounding=ROUND_HALF_UP))

    def cupo_disponible(self, personas_reservadas: int) -> int:
        """Cupo máximo menos las personas ya reservadas (R14, FR-08). Se calcula, no se guarda (S5)."""
        return self._cupo_maximo - personas_reservadas

    def esta_vencido(self, hoy: date) -> bool:
        """True si la fecha de salida ya pasó (R15, FR-14)."""
        return self._fecha_salida < hoy

    # --- comandos --------------------------------------------------------
    def modificar(self, datos: dict, destinos: list[Destino] | None = None) -> None:
        """Cambia los datos de un paquete en borrador. Un paquete publicado no se modifica (R7)."""
        self.verificar_editable()
        permitidos = {"nombre", "fecha_salida", "fecha_regreso", "cupo_maximo", "margen"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            raise ReglaNegocioError(f"Campos no modificables: {', '.join(sorted(desconocidos))}.")
        if destinos is not None:
            self._validar_disponibles(destinos)
        self._asignar(
            datos.get("nombre", self._nombre),
            datos.get("fecha_salida", self._fecha_salida),
            datos.get("fecha_regreso", self._fecha_regreso),
            datos.get("cupo_maximo", self._cupo_maximo),
            datos.get("margen", self._margen),
            destinos if destinos is not None else self._destinos,
        )

    def publicar(self) -> None:
        """Fija el precio con los costos vigentes y deja el paquete disponible para reservas (FR-07)."""
        if self._estado is EstadoPaquete.PUBLICADO:
            raise ReglaNegocioError("El paquete ya está publicado.")
        self._precio_por_persona = self.calcular_precio()
        self._estado = EstadoPaquete.PUBLICADO

    def verificar_editable(self) -> None:
        if self._estado is EstadoPaquete.PUBLICADO:
            raise ReglaNegocioError("Un paquete publicado no se puede modificar ni eliminar.")

    # --- validaciones ----------------------------------------------------
    def _asignar(self, nombre, fecha_salida, fecha_regreso, cupo_maximo, margen, destinos) -> None:
        """Valida todos los datos (R3, R5, R6) y recién entonces los asigna."""
        nombre = (nombre or "").strip()
        if not nombre:
            raise ReglaNegocioError("El campo nombre es obligatorio.")
        if not isinstance(fecha_salida, date) or not isinstance(fecha_regreso, date):
            raise ReglaNegocioError("Las fechas de salida y regreso son obligatorias.")
        if fecha_regreso <= fecha_salida:
            raise ReglaNegocioError("La fecha de regreso debe ser posterior a la fecha de salida.")
        if isinstance(cupo_maximo, bool) or not isinstance(cupo_maximo, int) or cupo_maximo <= 0:
            raise ReglaNegocioError("El cupo máximo debe ser un número entero mayor que cero.")
        if (isinstance(margen, bool) or not isinstance(margen, (int, float))
                or not math.isfinite(margen) or margen < 0):
            raise ReglaNegocioError("El margen de operación no puede ser negativo.")
        destinos = list(destinos)
        if not MIN_DESTINOS <= len(destinos) <= MAX_DESTINOS:
            raise ReglaNegocioError(f"Un paquete combina entre {MIN_DESTINOS} y {MAX_DESTINOS} destinos.")
        ids = [d.id for d in destinos]
        if None in ids:
            raise ReglaNegocioError("Todos los destinos deben estar registrados en el catálogo.")
        if len(set(ids)) != len(ids):
            raise ReglaNegocioError("Un destino no se puede repetir dentro del mismo paquete.")
        self._nombre, self._fecha_salida, self._fecha_regreso = nombre, fecha_salida, fecha_regreso
        self._cupo_maximo, self._margen, self._destinos = cupo_maximo, float(margen), destinos

    @staticmethod
    def _validar_disponibles(destinos: list[Destino]) -> None:
        no_disponibles = [d.nombre for d in destinos if not d.disponible]
        if no_disponibles:
            raise ReglaNegocioError(
                f"Destinos no disponibles para paquetes nuevos: {', '.join(no_disponibles)}.")

    def __repr__(self) -> str:
        return f"Paquete(id={self._id}, nombre={self._nombre!r}, estado={self._estado.value})"
