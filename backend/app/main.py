"""Punto de entrada de la API de Viajes Aventura.

Ejecutar desde la carpeta backend/:  uvicorn app.main:app --reload
Documentación interactiva:           http://127.0.0.1:8000/docs
"""
import logging
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import clientes, destinos, paquetes, reservas
from app.database import conectar, crear_esquema
from app.dominio import NoAutenticadoError, NoEncontradoError, ReglaNegocioError

log = logging.getLogger("viajes_aventura")
STATIC = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    conexion = conectar()
    try:
        crear_esquema(conexion)
    finally:
        conexion.close()
    yield


app = FastAPI(title="Viajes Aventura API", version="0.1.0", lifespan=ciclo_de_vida)
app.include_router(destinos.router)
app.include_router(paquetes.router)
app.include_router(clientes.router)
app.include_router(reservas.router)


# --- Manejo de errores: nunca se expone una traza interna (sección 7.3) ---
@app.exception_handler(ReglaNegocioError)
async def regla_negocio(_: Request, exc: ReglaNegocioError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})


@app.exception_handler(NoEncontradoError)
async def no_encontrado(_: Request, exc: NoEncontradoError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(NoAutenticadoError)
async def no_autenticado(_: Request, exc: NoAutenticadoError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def validacion(_: Request, exc: RequestValidationError):
    # Se omite el valor recibido ("input") para no repetir datos sensibles en la respuesta (R17).
    errores = [{"campo": ".".join(map(str, e["loc"][1:])), "mensaje": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        content={"detail": "Datos inválidos.", "errores": errores})


@app.exception_handler(sqlite3.IntegrityError)
async def integridad(_: Request, exc: sqlite3.IntegrityError):
    log.warning("Restricción de integridad: %s", exc)
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"detail": "La operación entra en conflicto con datos existentes."})


@app.exception_handler(Exception)
async def error_interno(_: Request, exc: Exception):
    log.exception("Error no controlado")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": "Error interno del servidor."})


# Build del frontend (sección 5.1): se monta al final para no tapar las rutas /api.
if STATIC.is_dir():
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="frontend")
