from app.dominio.errores import ReglaNegocioError


class Destino:
    """Lugar con un servicio ya cotizado (sección 1.1 del caso). Reglas R1, R2 y R8."""

    def __init__(self, nombre: str, zona: str, descripcion: str, duracion_dias: int,
                 costo_base: int, disponible: bool = True, id: int | None = None):
        self._id = id
        self._nombre = self._validar_texto(nombre, "nombre")
        self._zona = self._validar_texto(zona, "zona")
        self._descripcion = (descripcion or "").strip()
        self._duracion_dias = self._validar_positivo(duracion_dias, "La duración en días")
        self._costo_base = self._validar_positivo(costo_base, "El costo base")       # R2
        self._disponible = bool(disponible)

    # --- consultas -------------------------------------------------------
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def zona(self) -> str:
        return self._zona

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def duracion_dias(self) -> int:
        return self._duracion_dias

    @property
    def costo_base(self) -> int:
        return self._costo_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    # --- comandos --------------------------------------------------------
    def actualizar(self, datos: dict) -> None:
        """Modifica los campos recibidos (FR-02). La disponibilidad solo cambia con marcar_no_disponible()."""
        permitidos = {"nombre", "zona", "descripcion", "duracion_dias", "costo_base"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            raise ReglaNegocioError(f"Campos no modificables: {', '.join(sorted(desconocidos))}.")
        # Se valida todo antes de asignar, para no dejar el objeto a medio modificar.
        nuevo = Destino(
            nombre=datos.get("nombre", self._nombre),
            zona=datos.get("zona", self._zona),
            descripcion=datos.get("descripcion", self._descripcion),
            duracion_dias=datos.get("duracion_dias", self._duracion_dias),
            costo_base=datos.get("costo_base", self._costo_base),
        )
        self._nombre, self._zona, self._descripcion = nuevo.nombre, nuevo.zona, nuevo.descripcion
        self._duracion_dias, self._costo_base = nuevo.duracion_dias, nuevo.costo_base

    def marcar_no_disponible(self) -> None:
        """Baja lógica (R8): el destino deja de ofrecerse para paquetes nuevos."""
        self._disponible = False

    # --- validaciones ----------------------------------------------------
    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        valor = (valor or "").strip()
        if not valor:
            raise ReglaNegocioError(f"El campo {campo} es obligatorio.")
        return valor

    @staticmethod
    def _validar_positivo(valor: int, campo: str) -> int:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ReglaNegocioError(f"{campo} debe ser un número entero mayor que cero.")
        return valor

    def __repr__(self) -> str:
        return f"Destino(id={self._id}, nombre={self._nombre!r})"
