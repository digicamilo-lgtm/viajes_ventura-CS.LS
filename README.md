# Viajes Aventura — Sistema de gestión de agencia de viajes

Proyecto de la asignatura **TI3V21 Programación Orientada a Objeto Seguro** (INACAP Valparaíso), Unidad 4. Profesor: **Rubén Schnettler**.

**Integrantes:** Logan Silva Jara y Camilo Sepúlveda.

**Estado:** Informe Técnico Grupal en elaboración (`Informe_Tecnico_Viajes_Aventura.docx`) — secciones 2 (requerimientos funcionales y no funcionales), 3 (modelamiento UML/BPMN) y 4 (metodología ágil) completas. Backend completo, integrado y con revisión de seguridad (129 pruebas): Destinos (HU-01) y Paquetes (HU-02) de Camilo; Clientes y seguridad (HU-03) y Reservas (HU-04) de Logan; integración, autenticación de administrador y revisión de seguridad (sección 7.3) de Camilo. Falta el frontend.

## Material de referencia

- `POO-TI3V21-Caso-Viajes-Aventura.pdf` — caso de estudio.
- `TI3021_U4_ES_GUÍA.pdf` — guía de la evaluación.
- `rubrica 4.xlsx` — Rúbrica N°2 (Informe Técnico Grupal y Defensa Argumentativa Individual), con los 5 criterios 4.1.1-4.1.5 y sus indicadores grupales/individuales.
- `6_poo_proyecto_consolidacion_rubensch.pdf` — material de consolidación del curso.

## Entregables

- `Informe_Tecnico_Viajes_Aventura.docx` — Informe Técnico Grupal (requerimientos, modelamiento UML/BPMN, metodología ágil, arquitectura y seguridad). Se evalúa con la Rúbrica N°2 (30% de la nota).

## Backend (Python + FastAPI + SQLite)

Estructura de `backend/`, fiel al diagrama de clases de la sección 3.3 del Informe Técnico:

- `app/dominio/` — clases de dominio con las reglas de negocio (`Destino`, `Paquete`, `EstadoPaquete`, `Reserva`, y `Usuario` abstracta con sus subclases `Cliente` y `Administrador`). Es la única fuente de verdad de las reglas R1-R17.
- `app/repositorios/` — `Repositorio[T]` abstracto y un repositorio SQLite por entidad. Todas las consultas van parametrizadas (`?`). `transaccion_exclusiva()` sirve cuando una decisión depende de datos que otra solicitud podría cambiar al mismo tiempo (cupo, R14).
- `app/seguridad/` — hash de contraseñas (`bcrypt`, directo, sin passlib — ver VALIDACION_IA.md Cambio 7) y tokens de sesión (`PyJWT`, HS256, con el rol del usuario).
- `app/api/` — rutas FastAPI y esquemas Pydantic (solo tipos y largos; no repiten reglas de negocio). Las rutas que modifican el catálogo exigen sesión de administrador.
- `app/database.py` — conexión y esquema completo (6 tablas).
- `app/crear_administrador.py` — crea la cuenta de un socio administrador desde la consola.
- `tests/` — 129 pruebas: dominio, seguridad, API, concurrencia e integración de punta a punta (`test_integracion.py`), sobre una base SQLite temporal.

Instalar y ejecutar (Windows, desde `backend/`):

```
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest                       # pruebas
set JWT_SECRET=una-clave-aleatoria-de-al-menos-32-bytes
.venv\Scripts\python -m app.crear_administrador --nombre "Paulina Ovalle" --correo paulina@viajesaventura.cl
.venv\Scripts\python -m uvicorn app.main:app --reload # API en http://127.0.0.1:8000/docs
```

La base de datos se crea sola en `backend/viajes.db`, que está ignorada por git. Se puede usar otra ruta con la variable de entorno `VIAJES_DB`. `JWT_SECRET` es obligatoria y debe tener al menos 32 bytes; en pruebas la fija `tests/conftest.py`. `crear_administrador` pide la contraseña sin mostrarla (mínimo 12 caracteres); no existe registro público de administradores.

Para usar las rutas protegidas desde `/docs`: iniciar sesión en `POST /api/administradores/sesiones` (o `/api/clientes/sesiones`), copiar el `token` y pegarlo en el botón **Authorize**.

Para agregar un dominio nuevo: crear la clase en `app/dominio/`, su repositorio heredando de `Repositorio`, el router en `app/api/` (registrándolo en `app/main.py`) y sus pruebas en `tests/`. Una regla incumplida se informa lanzando `ReglaNegocioError` (responde 400), `NoEncontradoError` (404), `NoAutenticadoError` (401) o `NoAutorizadoError` (403).

Análisis estático (sección 7.3 del informe): `.venv\Scripts\python -m pip install bandit pip-audit`, luego `.venv\Scripts\python -m bandit -r app` y `.venv\Scripts\python -m pip_audit -r requirements.txt`.

## Diagramas

`docs/diagramas/` contiene las fuentes editables y las imágenes de los diagramas de la sección 3 del Informe Técnico:

- `generar_bpmn.py` → `bpmn-1-gestion-destinos`, `bpmn-2-publicar-paquete` y `bpmn-3-reservar-paquete` (`.svg` + `.png`). Regenerar los SVG: `py generar_bpmn.py`.
- `generar_casos_uso.py` → `casos-de-uso` (`.svg` + `.png`). Regenerar el SVG: `py generar_casos_uso.py`.
- `clases.mmd` (dominio) y `clases-persistencia.mmd` (repositorios), en Mermaid. Regenerar: `mmdc -i clases.mmd -o clases.png -c config.json -s 2 -b white`.

Si se modifica un diagrama, hay que regenerar su `.png` (los SVG se pueden exportar desde cualquier navegador) y reemplazar la figura correspondiente en el Informe Técnico.

## Trazabilidad

Cada cambio del proyecto (código, documentación o avance del Informe Técnico) se registra en `VALIDACION_IA.md` (objetivo, implementación, revisión técnica y validación) y se refleja en este README. **Convención del repo:** cualquiera de los dos integrantes (y la IA con la que trabaje cada uno) debe seguir este mismo ciclo — actualizar `README.md`, `VALIDACION_IA.md` y, si corresponde, `Informe_Tecnico_Viajes_Aventura.docx`, en cada cambio, antes de hacer commit. Último cambio: Cambio 9 — integración de los 4 dominios y revisión de seguridad del sistema integrado (2026-10-01).

## Próximos pasos

1. ~~Levantar requerimientos a partir del caso de estudio.~~ ✅ hecho (Cambio 3).
2. ~~Modelar la solución (BPMN, casos de uso, diagrama de clases UML).~~ ✅ hecho (Cambio 4).
3. ~~Definir metodología ágil (roles, Product Backlog, Sprint Backlog).~~ ✅ hecho (Cambio 5).
4. ~~Implementar por dominios: esqueleto + HU-01 + HU-02 (Camilo, Cambio 6); HU-03 + HU-04 (Logan, Cambio 7).~~ ✅ hecho.
5. Sprint 2 (4 oct):
   - ~~**Camilo:** integrar los 4 dominios en un flujo único de extremo a extremo y revisar la seguridad del sistema integrado (sección 7.3).~~ ✅ hecho (Cambio 9).
   - ~~Decidir la autenticación de administrador para las rutas de catálogo.~~ ✅ implementada (Cambio 9).
   - **Logan:** frontend React/Vite (HU-05). El frontend debe iniciar sesión de administrador para las pantallas del catálogo, y usar `GET /api/paquetes/publicados` y `/publicados/{id}` para la vista del cliente.
   - Defensa argumentativa individual de cada integrante.
