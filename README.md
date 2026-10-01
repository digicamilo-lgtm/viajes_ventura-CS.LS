# Viajes Aventura — Sistema de gestión de agencia de viajes

Proyecto de la asignatura **TI3V21 Programación Orientada a Objeto Seguro** (INACAP Valparaíso), Unidad 4. Profesor: **Rubén Schnettler**.

**Integrantes:** Logan Silva Jara y Camilo Sepúlveda.

**Estado:** Informe Técnico Grupal en elaboración (`Informe_Tecnico_Viajes_Aventura.docx`) — secciones 2 (requerimientos funcionales y no funcionales), 3 (modelamiento UML/BPMN) y 4 (metodología ágil) completas. Código (Sprint 1): backend con el esqueleto compartido y los dominios Destinos (HU-01) y Paquetes (HU-02) implementados y probados; faltan Clientes y seguridad (HU-03), Reservas (HU-04) y el frontend.

## Material de referencia

- `POO-TI3V21-Caso-Viajes-Aventura.pdf` — caso de estudio.
- `TI3021_U4_ES_GUÍA.pdf` — guía de la evaluación.
- `rubrica 4.xlsx` — Rúbrica N°2 (Informe Técnico Grupal y Defensa Argumentativa Individual), con los 5 criterios 4.1.1-4.1.5 y sus indicadores grupales/individuales.
- `6_poo_proyecto_consolidacion_rubensch.pdf` — material de consolidación del curso.

## Entregables

- `Informe_Tecnico_Viajes_Aventura.docx` — Informe Técnico Grupal (requerimientos, modelamiento UML/BPMN, metodología ágil, arquitectura y seguridad). Se evalúa con la Rúbrica N°2 (30% de la nota).

## Backend (Python + FastAPI + SQLite)

Estructura de `backend/`, fiel al diagrama de clases de la sección 3.3 del Informe Técnico:

- `app/dominio/` — clases de dominio con las reglas de negocio (`Destino`, `Paquete`, `EstadoPaquete`). Es la única fuente de verdad de las reglas R1-R17.
- `app/repositorios/` — `Repositorio[T]` abstracto y un repositorio SQLite por entidad. Todas las consultas van parametrizadas (`?`).
- `app/api/` — rutas FastAPI y esquemas Pydantic (solo tipos y largos; no repiten reglas de negocio).
- `app/database.py` — conexión y esquema completo (5 tablas, incluidas `clientes` y `reservas` para HU-03 y HU-04).
- `tests/` — pruebas del dominio y de la API sobre una base SQLite temporal.

Instalar y ejecutar (Windows, desde `backend/`):

```
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest                       # pruebas
.venv\Scripts\python -m uvicorn app.main:app --reload # API en http://127.0.0.1:8000/docs
```

La base de datos se crea sola en `backend/viajes.db`, que está ignorada por git. Se puede usar otra ruta con la variable de entorno `VIAJES_DB`.

Para agregar un dominio (HU-03 y HU-04): crear la clase en `app/dominio/`, su repositorio heredando de `Repositorio`, el router en `app/api/` (registrándolo en `app/main.py`) y sus pruebas en `tests/`. Una regla incumplida se informa lanzando `ReglaNegocioError` (responde 400) o `NoEncontradoError` (responde 404).

## Diagramas

`docs/diagramas/` contiene las fuentes editables y las imágenes de los diagramas de la sección 3 del Informe Técnico:

- `generar_bpmn.py` → `bpmn-1-gestion-destinos`, `bpmn-2-publicar-paquete` y `bpmn-3-reservar-paquete` (`.svg` + `.png`). Regenerar los SVG: `py generar_bpmn.py`.
- `generar_casos_uso.py` → `casos-de-uso` (`.svg` + `.png`). Regenerar el SVG: `py generar_casos_uso.py`.
- `clases.mmd` (dominio) y `clases-persistencia.mmd` (repositorios), en Mermaid. Regenerar: `mmdc -i clases.mmd -o clases.png -c config.json -s 2 -b white`.

Si se modifica un diagrama, hay que regenerar su `.png` (los SVG se pueden exportar desde cualquier navegador) y reemplazar la figura correspondiente en el Informe Técnico.

## Trazabilidad

Cada cambio del proyecto (código, documentación o avance del Informe Técnico) se registra en `VALIDACION_IA.md` (objetivo, implementación, revisión técnica y validación) y se refleja en este README. **Convención del repo:** cualquiera de los dos integrantes (y la IA con la que trabaje cada uno) debe seguir este mismo ciclo — actualizar `README.md`, `VALIDACION_IA.md` y, si corresponde, `Informe_Tecnico_Viajes_Aventura.docx`, en cada cambio, antes de hacer commit. Último cambio: Cambio 6 — esqueleto del backend y dominios Destinos y Paquetes (2026-10-01).

## Próximos pasos

1. ~~Levantar requerimientos a partir del caso de estudio.~~ ✅ hecho (Cambio 3).
2. ~~Modelar la solución (BPMN, casos de uso, diagrama de clases UML).~~ ✅ hecho (Cambio 4).
3. ~~Definir metodología ágil (roles, Product Backlog, Sprint Backlog).~~ ✅ hecho (Cambio 5).
4. Implementar por dominios (backend + frontend) y seguridad (autenticación) — Sprint 1, 2-3 de octubre.
   - ~~Esqueleto compartido + HU-01 Destinos + HU-02 Paquetes (Camilo).~~ ✅ hecho (Cambio 6).
   - HU-03 Clientes y seguridad + HU-04 Reservas (Logan).
   - Proteger con autenticación de administrador las rutas que modifican el catálogo (S1, RNF-03), cuando exista HU-03.
   - Frontend React/Vite.
