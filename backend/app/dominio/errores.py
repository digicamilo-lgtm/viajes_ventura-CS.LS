class ReglaNegocioError(Exception):
    """Una operación viola una regla de negocio (R1-R17). El mensaje se muestra al usuario."""


class NoEncontradoError(Exception):
    """La entidad pedida no existe."""
