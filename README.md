# Viajes Aventura — Sistema de gestión de agencia de viajes

Proyecto de la asignatura **TI3V21 Programación Orientada a Objeto Seguro** (INACAP Valparaíso), Unidad 4. Profesor: **Rubén Schnettler**.

**Integrantes:** Logan Silva Jara y Camilo Sepúlveda.

**Estado:** proyecto cerrado para la entrega del 5 de octubre de 2026. Backend con 140 pruebas, frontend React/Vite probado de punta a punta en navegador, Informe Técnico completo (secciones 1 a 8) y despliegue público en Render (plan gratuito): https://viajes-aventura-o5p1.onrender.com

## Material de referencia

- `docs/curso/POO-TI3V21-Caso-Viajes-Aventura.pdf` — caso de estudio.
- `docs/curso/TI3021_U4_ES_GUÍA.pdf` — guía de la evaluación.
- `docs/curso/rubrica 4.xlsx` — Rúbrica N°2 (Informe Técnico Grupal y Defensa Argumentativa Individual), con los 5 criterios 4.1.1-4.1.5 y sus indicadores grupales/individuales.
- `docs/curso/6_poo_proyecto_consolidacion_rubensch.pdf` — material de consolidación del curso.

## Entregables

- `Informe_Tecnico_Viajes_Aventura.pdf` — Informe Técnico Grupal (requerimientos, modelamiento UML/BPMN, metodología ágil, arquitectura y seguridad). Se evalúa con la Rúbrica N°2 (30% de la nota).

## Backend (Python + FastAPI + SQLite)

Estructura de `backend/`, fiel al diagrama de clases de la sección 3.3 del Informe Técnico:

- `app/dominio/` — clases de dominio con las reglas de negocio (`Destino`, `Paquete`, `EstadoPaquete`, `Reserva`, y `Usuario` abstracta con sus subclases `Cliente` y `Administrador`). Es la única fuente de verdad de las reglas R1-R17.
- `app/repositorios/` — `Repositorio[T]` abstracto y un repositorio SQLite por entidad. Todas las consultas van parametrizadas (`?`). `transaccion_exclusiva()` sirve cuando una decisión depende de datos que otra solicitud podría cambiar al mismo tiempo (cupo, R14).
- `app/seguridad/` — hash de contraseñas (`bcrypt`, directo, sin passlib — ver VALIDACION_IA.md Cambio 7) y tokens de sesión (`PyJWT`, HS256, con el rol del usuario).
- `app/api/` — rutas FastAPI y esquemas Pydantic (solo tipos y largos; no repiten reglas de negocio). Las rutas que modifican el catálogo exigen sesión de administrador.
- `app/database.py` — conexión y esquema completo (6 tablas).
- `app/crear_administrador.py` — crea la cuenta de un socio administrador desde la consola.
- `tests/` — 140 pruebas: dominio, seguridad, API, concurrencia e integración de punta a punta (`test_integracion.py`), sobre una base SQLite temporal.

Instalar y ejecutar (Windows, desde `backend/`):

```
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest                       # pruebas (opcional)
```

**1. Cuenta de administrador:** no existe registro público. Si clonas el repositorio y lo ejecutas en tu equipo, debes crear una cuenta de administrador con el comando siguiente (contraseña con asteriscos, mínimo 12 caracteres). Si solo ingresas a la URL de la demo, el administrador ya existe, creado desde las variables de entorno de Render:

```
.venv\Scripts\python -m app.crear_administrador --nombre "Nombre Apellido" --correo correo@dominio.cl
```

**2. Generar la clave `JWT_SECRET`** (obligatoria, al menos 32 caracteres). Es la clave con la que se firman los tokens de sesión, así que no se escribe en el código ni se sube a git. Genérala con:

```
.venv\Scripts\python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**3. Definir la clave y levantar el servidor**, en la **misma** ventana (PowerShell):

```
$env:JWT_SECRET = "pega-aqui-la-clave-generada"
.venv\Scripts\python -m uvicorn app.main:app --reload
```

En CMD la sintaxis es `set JWT_SECRET=...`. Si la variable no está definida en esa ventana, o tiene menos de 32 caracteres, el servidor no arranca y muestra `Falta configurar la variable de entorno JWT_SECRET`.

API y documentación: http://127.0.0.1:8000/docs · Aplicación: http://127.0.0.1:8000/

La base de datos se crea sola en `backend/viajes.db`, que está ignorada por git. Se puede usar otra ruta con la variable de entorno `VIAJES_DB`. En las pruebas, `tests/conftest.py` fija `JWT_SECRET` por su cuenta.

Para usar las rutas protegidas desde `/docs`: iniciar sesión en `POST /api/administradores/sesiones` (o `/api/clientes/sesiones`), copiar el `token` y pegarlo en el botón **Authorize**.

Para agregar un dominio nuevo: crear la clase en `app/dominio/`, su repositorio heredando de `Repositorio`, el router en `app/api/` (registrándolo en `app/main.py`) y sus pruebas en `tests/`. Una regla incumplida se informa lanzando `ReglaNegocioError` (responde 400), `NoEncontradoError` (404), `NoAutenticadoError` (401) o `NoAutorizadoError` (403).

Análisis estático (sección 7.3 del informe): `.venv\Scripts\python -m pip install bandit pip-audit`, luego `.venv\Scripts\python -m bandit -r app` y `.venv\Scripts\python -m pip_audit -r requirements.txt`.

## Frontend (React + Vite)

Estructura de `frontend/src/`, arquitectura de la sección 5.1 del Informe Técnico:

- `api.js` — cliente HTTP a `/api` (agrega el token `Authorization: Bearer` cuando corresponde).
- `auth.jsx` — contexto de sesión (React Context + `localStorage`): guarda `{ token, rol, perfil }`; el rol siempre sale de lo que el backend valida al iniciar sesión, nunca se simula en el frontend.
- `pages/` — `Catalogo`, `PaqueteDetalle` (pública); `ClienteRegistro`, `ClienteLogin`, `MisReservas` (cliente); `AdminLogin`, `AdminDestinos`, `AdminPaquetes` (administrador).
- `MisReservas` permite al cliente **modificar** la cantidad de personas (la reserva anterior queda cancelada y se crea una nueva al precio vigente) y **cancelar** una reserva hasta la fecha de salida, liberando su cupo (supuesto S4).

Instalar y ejecutar (desde `frontend/`, con el backend ya corriendo en `:8000`):

```
npm install
npm run dev      # http://localhost:5173, con proxy /api -> :8000
```

Para la entrega: `npm run build` compila directamente a `backend/static/` (configurado en `vite.config.js`); luego `uvicorn app.main:app` sirve todo desde `:8000`, un único comando. Para probar el flujo completo hace falta un administrador (paso 1) y un destino/paquete publicado antes de que el catálogo público muestre algo.

## Diagramas

`docs/diagramas/` contiene las fuentes editables y las imágenes de los diagramas de la sección 3 del Informe Técnico:

- `generar_bpmn.py` → `bpmn-1-gestion-destinos`, `bpmn-2-publicar-paquete` y `bpmn-3-reservar-paquete` (`.svg` + `.png`). Regenerar los SVG: `py generar_bpmn.py`.
- `generar_casos_uso.py` → `casos-de-uso` (`.svg` + `.png`). Regenerar el SVG: `py generar_casos_uso.py`.
- `clases.mmd` (dominio) y `clases-persistencia.mmd` (repositorios), en Mermaid. Regenerar: `mmdc -i clases.mmd -o clases.png -c config.json -s 2 -b white`.

Si se modifica un diagrama, hay que regenerar su `.png` (los SVG se pueden exportar desde cualquier navegador) y reemplazar la figura correspondiente en el Informe Técnico.

## Trazabilidad

Cada cambio del proyecto (código, documentación o avance del Informe Técnico) se registra en `VALIDACION_IA.md` (objetivo, implementación, revisión técnica y validación) y se refleja en este README. **Convención del repo:** cualquiera de los dos integrantes (y la IA con la que trabaje cada uno) debe seguir este mismo ciclo — actualizar `README.md`, `VALIDACION_IA.md` y, si corresponde, `Informe_Tecnico_Viajes_Aventura.docx`, en cada cambio, antes de hacer commit. Último cambio: Cambio 22 — se quita la sección de estado del Informe y las conclusiones pasan a ser la sección 8 (2026-10-05).

## Próximos pasos

1. ~~Levantar requerimientos a partir del caso de estudio.~~ ✅ hecho (Cambio 3).
2. ~~Modelar la solución (BPMN, casos de uso, diagrama de clases UML).~~ ✅ hecho (Cambio 4).
3. ~~Definir metodología ágil (roles, Product Backlog, Sprint Backlog).~~ ✅ hecho (Cambio 5).
4. ~~Implementar por dominios: esqueleto + HU-01 + HU-02 (Camilo, Cambio 6); HU-03 + HU-04 (Logan, Cambio 7).~~ ✅ hecho.
5. ~~Sprint 2: integración + seguridad (Camilo, Cambio 9); frontend React/Vite (Logan, Cambio 10).~~ ✅ hecho. Sistema completo, de punta a punta.
6. Pendiente antes de la entrega (5 oct):
   - ~~Ejecutar SonarCloud sobre el repositorio.~~ ✅ hecho: Quality Gate aprobado y 0 New Issues (Cambio 11).
   - ~~Exposición del equipo.~~ ✅ hecha. Las cuentas de administrador las crea el profesor.

## Despliegue

- **Servicio público (demo):** https://viajes-aventura-o5p1.onrender.com (plan gratuito de Render).
- **Configuración:** `render.yaml` en la raíz. El build compila el frontend y el servicio ejecuta `uvicorn` sobre el puerto que asigna Render.
- **Variables de entorno en Render:** `JWT_SECRET` (se genera sola), `ADMIN_CORREO` y `ADMIN_CONTRASENA`. Con estas dos últimas, la aplicación crea el administrador al arrancar si no existe; el profesor es quien define esas credenciales. La contraseña nunca va en el repositorio.
- **Limitación:** el plan gratuito no conserva el disco. La base de datos se reinicia cada vez que el servicio se reinicia, así que la demo puede volver a su estado inicial.
- **Copia pública:** el despliegue usa una copia del repositorio sin los materiales del curso (PDF del caso, guía y rúbrica). Esos archivos se mantienen solo en el repositorio del equipo.

## Calidad estática

El análisis SonarCloud del commit `5c495d17` quedó con Quality Gate aprobado y 0 issues en New Code. El backend mantiene 140 pruebas aprobadas (133 en ese análisis más 7 de cancelación y modificación de reservas, agregadas después) (una agregada en el Cambio 12 tras detectar que la nueva validación de correo aceptaba más de una arroba); Bandit no detecta problemas y pip-audit no encuentra vulnerabilidades conocidas. El frontend compila con `npm run build` y `npm run lint` termina sin advertencias.
