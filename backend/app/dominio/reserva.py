from datetime import date

from app.dominio.errores import ReglaNegocioError
from app.dominio.paquete import EstadoPaquete, Paquete


class Reserva:
    """Reserva de un cliente sobre un paquete publicado (sección 1.3 del caso). Reglas R12 a R16."""

    def __init__(self, cliente_id: int, paquete_id: int, fecha_emision: date, cantidad_personas: int,
                 total: int, id: int | None = None, cancelada: bool = False):
        self._id = id
        self._cancelada = cancelada
        self._cliente_id = self._validar_id(cliente_id, "cliente")
        self._paquete_id = self._validar_id(paquete_id, "paquete")
        if not isinstance(fecha_emision, date):
            raise ReglaNegocioError("La fecha de emisión es obligatoria.")
        self._fecha_emision = fecha_emision
        self._cantidad_personas = self._validar_personas(cantidad_personas)          # R16
        if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
            raise ReglaNegocioError("El total de la reserva debe ser mayor que cero.")  # R13
        self._total = total

    @classmethod
    def crear(cls, cliente_id: int, paquete: Paquete, cantidad_personas: int, personas_reservadas: int,
              hoy: date) -> "Reserva":
        """Registra una reserva validando vigencia (R15) y cupo (R14) antes de fijar el total (R13)."""
        if paquete.estado is not EstadoPaquete.PUBLICADO:
            raise ReglaNegocioError("Solo se puede reservar un paquete publicado.")
        if paquete.esta_vencido(hoy):
            raise ReglaNegocioError("No se puede reservar: la fecha de salida del paquete ya pasó.")  # R15
        cantidad_personas = cls._validar_personas(cantidad_personas)
        if cantidad_personas > paquete.cupo_disponible(personas_reservadas):
            raise ReglaNegocioError("No hay cupo disponible para esa cantidad de personas.")  # R14
        total = paquete.precio_por_persona * cantidad_personas                        # R13
        return cls(cliente_id=cliente_id, paquete_id=paquete.id, fecha_emision=hoy,
                   cantidad_personas=cantidad_personas, total=total)

    # --- consultas -------------------------------------------------------
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def cliente_id(self) -> int:
        return self._cliente_id

    @property
    def paquete_id(self) -> int:
        return self._paquete_id

    @property
    def fecha_emision(self) -> date:
        return self._fecha_emision

    @property
    def cantidad_personas(self) -> int:
        return self._cantidad_personas

    @property
    def total(self) -> int:
        return self._total

    @property
    def cancelada(self) -> bool:
        return self._cancelada

    def cancelar(self, paquete: Paquete, hoy: date) -> None:
        """Cancela la reserva hasta el día de salida (S4). Libera su cupo al dejar de contarse."""
        if self._cancelada:
            raise ReglaNegocioError("La reserva ya está cancelada.")
        if paquete.esta_vencido(hoy):
            raise ReglaNegocioError("No se puede cancelar: el paquete ya partió.")
        self._cancelada = True

    def reemplazar_por(self, paquete: Paquete, nueva_cantidad_personas: int, personas_reservadas: int,
                       hoy: date) -> "Reserva":
        """Modifica la cantidad de personas (S4): la reserva actual se cancela y se crea una nueva
        al precio vigente, para que cada reserva conserve un total fijo (R13)."""
        if self._cancelada:
            raise ReglaNegocioError("No se puede modificar una reserva cancelada.")
        otras = personas_reservadas - self._cantidad_personas  # esta reserva deja de ocupar cupo
        nueva = Reserva.crear(cliente_id=self._cliente_id, paquete=paquete,
                              cantidad_personas=nueva_cantidad_personas, personas_reservadas=otras, hoy=hoy)
        self.cancelar(paquete, hoy)
        return nueva

    # --- validaciones ----------------------------------------------------
    @staticmethod
    def _validar_id(valor: int, campo: str) -> int:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ReglaNegocioError(f"El {campo} es obligatorio.")
        return valor

    @staticmethod
    def _validar_personas(valor: int) -> int:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 1:
            raise ReglaNegocioError("La cantidad de personas debe ser al menos uno.")
        return valor

    def __repr__(self) -> str:
        return f"Reserva(id={self._id}, cliente_id={self._cliente_id}, paquete_id={self._paquete_id})"
