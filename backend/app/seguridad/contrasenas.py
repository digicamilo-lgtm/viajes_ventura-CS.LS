"""Hash y verificación de contraseñas (R10, sección 7.1 del Informe Técnico).

Usa la librería `bcrypt` directamente en vez de passlib: su última versión
(1.7.4) es incompatible con bcrypt >= 4.1 porque depende de un atributo
(`__about__.__version__`) que esa librería eliminó — ver VALIDACION_IA.md,
Cambio 7.
"""
import secrets

import bcrypt

from app.dominio.errores import ReglaNegocioError

_COSTO = 12  # factor de costo del algoritmo bcrypt (sección 7.1)


def hashear(contrasena: str) -> str:
    try:
        hash_bytes = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt(rounds=_COSTO))
    except ValueError as exc:                      # bcrypt limita la entrada a 72 bytes
        raise ReglaNegocioError("La contraseña es demasiado larga.") from exc
    return hash_bytes.decode("utf-8")


def verificar(contrasena: str, hash_contrasena: str) -> bool:
    return bcrypt.checkpw(contrasena.encode("utf-8"), hash_contrasena.encode("utf-8"))


_hash_ficticio: str | None = None


def simular_verificacion(contrasena: str) -> None:
    """Gasta el mismo tiempo que verificar() cuando el correo no existe.

    Sin esto, un inicio de sesión fallido con un correo registrado tarda ~200 ms
    (bcrypt) y uno con un correo inexistente ~2 ms, lo que revela qué correos
    están registrados (sección 7.1).
    """
    global _hash_ficticio
    if _hash_ficticio is None:
        # Bytes aleatorios: no hay una contraseña literal en el código que coincida con este hash.
        _hash_ficticio = bcrypt.hashpw(secrets.token_bytes(32), bcrypt.gensalt(rounds=_COSTO)).decode("utf-8")
    try:
        verificar(contrasena, _hash_ficticio)
    except ValueError:      # contraseña de más de 72 bytes: igual se rechaza
        pass
