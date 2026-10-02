from abc import ABC, abstractmethod

from app.dominio.errores import ReglaNegocioError


class Usuario(ABC):
    """Lo común a quien inicia sesión en el sistema (Figura 5 del Informe Técnico).

    Concentra la identidad y la verificación de la contraseña para no duplicarlas
    entre Cliente y Administrador (FR-10, RNF-01). Ninguna subclase guarda la
    contraseña en texto plano: solo su hash (R10).
    """

    ROL: str

    def __init__(self, nombre: str, correo: str, hash_contrasena: str, id: int | None = None):
        self._id = id
        self._nombre = self._validar_texto(nombre, "nombre")
        self._correo = self._validar_correo(correo)
        self._hash_contrasena = self._validar_texto(hash_contrasena, "contraseña")  # ya hasheada (R10)

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def hash_contrasena(self) -> str:
        return self._hash_contrasena

    def verificar_contrasena(self, contrasena: str) -> bool:
        from app.seguridad.contrasenas import verificar   # import diferido: seguridad depende del dominio
        return verificar(contrasena, self._hash_contrasena)

    @abstractmethod
    def puede_gestionar_catalogo(self) -> bool:
        """Polimorfismo (RNF-03, S1): el servidor autoriza el catálogo preguntándole al usuario,
        sin revisar su tipo concreto."""

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
        local, separador, dominio = valor.partition("@")
        correo_valido = (separador and local and dominio and "." in dominio
                         and "@" not in dominio and not any(c.isspace() for c in valor))
        if not correo_valido:
            raise ReglaNegocioError("El correo electrónico no tiene un formato válido.")
        return valor

    def __repr__(self) -> str:
        # Nunca datos sensibles ni el hash (R17, sección 7.2).
        return f"{type(self).__name__}(id={self._id}, correo={self._correo!r})"


class Administrador(Usuario):
    """Socio de Viajes Aventura que mantiene el catálogo de destinos y paquetes (S1)."""

    ROL = "administrador"

    def puede_gestionar_catalogo(self) -> bool:
        return True
