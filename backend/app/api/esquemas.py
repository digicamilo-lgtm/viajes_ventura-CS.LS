"""Esquemas de entrada y salida de la API.

Pydantic valida solo tipos y largos máximos; las reglas de negocio (R1-R8) las
aplica el dominio, que es la única fuente de verdad (RNF-05).
"""
from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.dominio import Cliente, Destino, EstadoPaquete, Paquete, Reserva, Usuario

Texto = Annotated[str, Field(max_length=100)]
# bcrypt ignora cualquier byte más allá del 72; se limita aquí para no truncar en silencio.
Contrasena = Annotated[str, Field(min_length=8, max_length=72)]


# --- Destinos ------------------------------------------------------------
class DestinoEntrada(BaseModel):
    nombre: Texto
    zona: Texto
    descripcion: str = Field(default="", max_length=1000)
    duracion_dias: int
    costo_base: int


class DestinoActualizacion(BaseModel):
    nombre: Texto | None = None
    zona: Texto | None = None
    descripcion: str | None = Field(default=None, max_length=1000)
    duracion_dias: int | None = None
    costo_base: int | None = None


class DestinoSalida(BaseModel):
    id: int
    nombre: str
    zona: str
    descripcion: str
    duracion_dias: int
    costo_base: int
    disponible: bool

    @classmethod
    def desde(cls, d: Destino) -> "DestinoSalida":
        return cls(id=d.id, nombre=d.nombre, zona=d.zona, descripcion=d.descripcion,
                   duracion_dias=d.duracion_dias, costo_base=d.costo_base, disponible=d.disponible)


class ResultadoBaja(BaseModel):
    id: int
    resultado: Literal["eliminado", "no_disponible"]
    mensaje: str


# --- Paquetes ------------------------------------------------------------
class PaqueteEntrada(BaseModel):
    nombre: Texto
    fecha_salida: date
    fecha_regreso: date
    cupo_maximo: int
    margen: float = 0.20          # habitualmente 20 % (R6)
    destino_ids: list[int] = Field(max_length=20)


class PaqueteActualizacion(BaseModel):
    nombre: Texto | None = None
    fecha_salida: date | None = None
    fecha_regreso: date | None = None
    cupo_maximo: int | None = None
    margen: float | None = None
    destino_ids: list[int] | None = Field(default=None, max_length=20)


class DestinoEnPaquete(BaseModel):
    id: int
    nombre: str
    zona: str
    costo_base: int


class PaqueteSalida(BaseModel):
    id: int
    nombre: str
    fecha_salida: date
    fecha_regreso: date
    cupo_maximo: int
    margen: float
    estado: EstadoPaquete
    precio_por_persona: int
    personas_reservadas: int
    cupo_disponible: int
    vencido: bool
    destinos: list[DestinoEnPaquete]

    @classmethod
    def desde(cls, p: Paquete, personas_reservadas: int, hoy: date) -> "PaqueteSalida":
        return cls(
            id=p.id, nombre=p.nombre, fecha_salida=p.fecha_salida, fecha_regreso=p.fecha_regreso,
            cupo_maximo=p.cupo_maximo, margen=p.margen, estado=p.estado,
            precio_por_persona=p.precio_por_persona, personas_reservadas=personas_reservadas,
            cupo_disponible=p.cupo_disponible(personas_reservadas), vencido=p.esta_vencido(hoy),
            destinos=[DestinoEnPaquete(id=d.id, nombre=d.nombre, zona=d.zona, costo_base=d.costo_base)
                      for d in p.destinos],
        )


# --- Clientes --------------------------------------------------------------
class ClienteEntrada(BaseModel):
    nombre: Texto
    rut: Texto
    correo: Texto
    telefono: Texto
    contrasena: Contrasena


class ClienteSalida(BaseModel):
    """Vista pública (R17): nunca incluye RUT ni teléfono."""
    id: int
    nombre: str
    correo: str

    @classmethod
    def desde(cls, c: Cliente) -> "ClienteSalida":
        return cls(**c.datos_publicos())


class ClientePerfil(ClienteSalida):
    """Solo para el propio cliente autenticado (registro y GET /api/clientes/yo); incluye RUT y teléfono."""
    rut: str
    telefono: str

    @classmethod
    def desde(cls, c: Cliente) -> "ClientePerfil":
        return cls(id=c.id, nombre=c.nombre, correo=c.correo, rut=c.rut, telefono=c.telefono)


class AdministradorSalida(BaseModel):
    id: int
    nombre: str
    correo: str

    @classmethod
    def desde(cls, a: Usuario) -> "AdministradorSalida":
        return cls(id=a.id, nombre=a.nombre, correo=a.correo)


class CredencialesEntrada(BaseModel):
    correo: Texto
    contrasena: Annotated[str, Field(max_length=72)]


class TokenSalida(BaseModel):
    token: str
    tipo: Literal["bearer"] = "bearer"


# --- Reservas ----------------------------------------------------------------
class ReservaEntrada(BaseModel):
    paquete_id: int
    cantidad_personas: int = Field(ge=1)          # R16


class ReservaSalida(BaseModel):
    id: int
    paquete_id: int
    fecha_emision: date
    cantidad_personas: int
    total: int

    @classmethod
    def desde(cls, r: Reserva) -> "ReservaSalida":
        return cls(id=r.id, paquete_id=r.paquete_id, fecha_emision=r.fecha_emision,
                   cantidad_personas=r.cantidad_personas, total=r.total)
