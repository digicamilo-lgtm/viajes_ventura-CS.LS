"""Hash y verificación de contraseñas (R10, sección 7.1 del Informe Técnico).

Usa la librería `bcrypt` directamente en vez de passlib: su última versión
(1.7.4) es incompatible con bcrypt >= 4.1 porque depende de un atributo
(`__about__.__version__`) que esa librería eliminó — ver VALIDACION_IA.md,
Cambio 7.
"""
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
