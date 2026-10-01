class ReglaNegocioError(Exception):
    """Una operación viola una regla de negocio (R1-R17). El mensaje se muestra al usuario."""


class NoEncontradoError(Exception):
    """La entidad pedida no existe."""


class NoAutenticadoError(Exception):
    """Falta un token de sesión válido, o las credenciales no coinciden (R10, R11)."""


class NoAutorizadoError(Exception):
    """El usuario está autenticado pero su rol no permite la operación (S1, RNF-03)."""
