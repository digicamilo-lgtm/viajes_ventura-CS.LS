from app.dominio.errores import ReglaNegocioError
from app.dominio.usuario import Usuario


class Cliente(Usuario):
    """Persona que se registra para reservar paquetes (sección 1.3 del caso). Reglas R9, R10, R17."""

    ROL = "cliente"

    def __init__(self, nombre: str, rut: str, correo: str, telefono: str, hash_contrasena: str,
                 id: int | None = None):
        super().__init__(nombre=nombre, correo=correo, hash_contrasena=hash_contrasena, id=id)
        self._rut = self._validar_rut(rut)
        self._telefono = self._validar_texto(telefono, "teléfono")

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def telefono(self) -> str:
        return self._telefono

    def puede_gestionar_catalogo(self) -> bool:
        return False

    def datos_publicos(self) -> dict:
        """Datos que pueden aparecer en cualquier listado: sin RUT ni teléfono (R17, RNF-02)."""
        return {"id": self._id, "nombre": self._nombre, "correo": self._correo}

    # --- validaciones ----------------------------------------------------
    @staticmethod
    def _validar_rut(valor: str) -> str:
        """Valida el dígito verificador (módulo 11) y normaliza a 12345678-K.

        El mensaje de error nunca repite el RUT recibido (R17, sección 7.2).
        """
        limpio = (valor or "").replace(".", "").replace(" ", "").upper()
        cuerpo, _, dv = limpio.rpartition("-")
        if not cuerpo:                       # sin guion: el último carácter es el dígito verificador
            cuerpo, dv = limpio[:-1], limpio[-1:]
        if not cuerpo.isdigit() or len(dv) != 1 or not 1 <= len(cuerpo) <= 8:
            raise ReglaNegocioError("El RUT no tiene un formato válido.")
        if Cliente._digito_verificador(cuerpo) != dv:
            raise ReglaNegocioError("El RUT no es válido.")
        return f"{int(cuerpo)}-{dv}"

    @staticmethod
    def _digito_verificador(cuerpo: str) -> str:
        suma = sum(int(d) * (2 + i % 6) for i, d in enumerate(reversed(cuerpo)))
        resto = 11 - suma % 11
        return {11: "0", 10: "K"}.get(resto, str(resto))
