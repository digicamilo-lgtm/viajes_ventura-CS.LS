import re

from app.dominio.errores import ReglaNegocioError

_CORREO_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Cliente:
    """Persona que se registra para reservar paquetes (sección 1.3 del caso). Reglas R9, R10, R17."""

    def __init__(self, nombre: str, rut: str, correo: str, telefono: str, hash_contrasena: str,
                 id: int | None = None):
        self._id = id
        self._nombre = self._validar_texto(nombre, "nombre")
        self._rut = self._validar_texto(rut, "RUT")
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_texto(telefono, "teléfono")
        self._hash_contrasena = self._validar_texto(hash_contrasena, "contraseña")  # ya hasheada (R10)

    # --- consultas -------------------------------------------------------
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def hash_contrasena(self) -> str:
        return self._hash_contrasena

    # --- validaciones ----------------------------------------------------
    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        valor = (valor or "").strip()
        if not valor:
            raise ReglaNegocioError(f"El campo {campo} es obligatorio.")
        return valor

    @staticmethod
    def _validar_correo(valor: str) -> str:
        valor = (valor or "").strip().lower()
        if not _CORREO_RE.match(valor):
            raise ReglaNegocioError("El correo electrónico no tiene un formato válido.")
        return valor

    def __repr__(self) -> str:
        # Nunca el RUT, el teléfono ni la contraseña (R17, sección 7.2).
        return f"Cliente(id={self._id}, correo={self._correo!r})"
