# Validación de uso de IA — Viajes Aventura

Registro de cada cambio del proyecto hecho con apoyo de IA. **Esto aplica a ambos integrantes**, cada uno con la IA que use: antes de cerrar cualquier cambio de código, documentación o avance del Informe Técnico (`Informe_Tecnico_Viajes_Aventura.docx`), hay que agregar aquí una entrada numerada "Cambio N" y actualizar `README.md` (y el Informe Técnico, cuando el cambio sea sobre su contenido). Por cada cambio se documenta:

- **Objetivo:** qué se buscaba resolver o construir.
- **Implementación:** qué hizo la IA y qué decidió el equipo.
- **Revisión técnica:** qué se revisó o corrigió del resultado.
- **Validación:** cómo se comprobó que el resultado es correcto.

## Cambio 1 — Reinicio del proyecto desde cero (2026-10-01)

- **Objetivo:** partir de cero en este repo (`digicamilo-lgtm/viajes_ventura-CS.LS`), sin el avance de requerimientos, código y diagramas que se había hecho antes en el repo anterior (`LSJ-tech/viajes_aventuras`), conservando solo el material de referencia del curso (caso, guía y rúbricas).
- **Implementación:** la IA eliminó `backend/`, `frontend/`, `docs/diagramas/` y `Informe_Tecnico_Viajes_Aventura.docx`, reescribió `README.md` y este archivo desde cero, y reescribió el historial de git completo (rama huérfana + commit único + `push --force` a `main`) para que no quedara rastro de los commits previos.
- **Revisión técnica:** antes de forzar el push se detectó que un integrante (Camilo) había pusheado un commit propio minutos antes; se revisó su contenido (cambio trivial de nombre de archivo) para confirmar que no se perdía trabajo sustantivo.
- **Validación:** se verificó con `git fetch` + `git log` que el remoto quedó con un único commit y solo los archivos esperados (`.gitignore`, README, VALIDACION_IA, PDFs/XLSX de rúbricas y guía).

Desde este cambio, cada modificación del proyecto se documenta aquí y en el README (sección "Trazabilidad"/"Estado").

## Cambio 2 — Se adjunta el Informe Técnico Grupal (2026-10-01)

- **Objetivo:** incorporar al repo el borrador del Informe Técnico Grupal (requerimientos, modelamiento UML/BPMN, metodología ágil, arquitectura y seguridad), evaluado con la Rúbrica N°2.
- **Implementación:** se agregó `Informe_Tecnico_Viajes_Aventura.docx` y se eliminó `TI3021_U4_RU_ES04_EV07 (0).xlsx` (a pedido explícito). Se actualizó el README para listar el Informe Técnico como entregable y para dejar explícito que también debe mantenerse sincronizado con README y esta bitácora en cada cambio.
- **Revisión técnica:** se extrajo el texto del `.docx` para confirmar que corresponde al caso de Viajes Aventura (mismo caso, reparto de dominios Logan/Camilo) y no a un archivo de otro proyecto.
- **Validación:** se confirmó con el usuario que el borrado del xlsx fue intencional antes de dejarlo en el commit.

A partir de este cambio, cualquier avance del Informe Técnico se documenta aquí como un nuevo "Cambio N", igual que el código o la documentación.

## Cambio 3 — Levantamiento de requerimientos (sección 2 del Informe Técnico) (2026-10-01)

- **Objetivo:** completar el Paso 1 de la guía de evaluación (criterio 4.1.1): identificar, clasificar y priorizar los requerimientos funcionales y no funcionales del sistema, redactados de forma independiente (sin reutilizar el levantamiento que ya traía `Informe_Tecnico_Viajes_Aventura.docx` al adjuntarlo en el Cambio 2).
- **Implementación:** se leyó `TI3021_U4_ES_GUÍA.pdf` y `POO-TI3V21-Caso-Viajes-Aventura.pdf` (reglas de negocio R1-R17 y alcance del caso), y se redactó desde cero la sección 2 del Informe Técnico: 15 requerimientos funcionales (FR-01 a FR-15), 6 no funcionales (RNF-01 a RNF-06) y una tabla de verificación contra las fallas medibles del caso (duplicados, sobreventa de cupo, fechas vencidas, precios inconsistentes, datos sensibles expuestos). El contenido anterior de esa sección se descartó.
- **Revisión técnica:** se presentó el borrador de FR/RNF al usuario para su revisión antes de escribirlo en el documento; se editó directamente el XML del `.docx` (desempaquetado/reempaquetado) y se validó la estructura con el validador del skill de docx (conteo de párrafos, XML bien formado) antes de reemplazar el archivo.
- **Validación:** se extrajo el texto del `.docx` resultante para confirmar que tildes y ñ quedaron bien codificados y que las tres tablas (FR, RNF, verificación) se insertaron completas. Antes de comitear, se leyó el contenido real de `rubrica 4.xlsx` (resultó ser la Rúbrica N°2 completa, con indicadores 4.1.1.G.1 a G.4 para el levantamiento de requerimientos) y se contrastó el levantamiento contra esos indicadores, confirmando que cubre el nivel Experto (cobertura exhaustiva, prioridad con criterio explícito, redacción con trazabilidad, verificación de alineación total con el problema). De paso se detectó que `Rubrica 2 y 3.pdf` no correspondía a este proyecto (era la rúbrica de otra evaluación, sobre consumo de APIs externas) y se eliminó del repo; se agregó `~$*` a `.gitignore` para evitar que los archivos temporales de bloqueo de Office (ej. `~$rubrica 4.xlsx`) se cuelen en commits futuros.

## Cambio 4 — Modelamiento de la solución con UML y BPMN (sección 3 del Informe Técnico) (2026-10-01)

- **Objetivo:** completar el Paso 2 de la guía de evaluación (criterio 4.1.2, indicadores 4.1.2.G.5 a G.7 e I.8 de `rubrica 4.xlsx`): modelar actores, actividades y procesos con BPMN, desarrollar el diagrama de casos de uso, elaborar el diagrama de clases UML con atributos, métodos y relaciones, y validar la trazabilidad entre requerimientos y modelos. Igual que en el Cambio 3, se rehízo desde cero: la sección 3 que traía el `.docx` (2 BPMN, casos de uso y clases del repo anterior, con referencias a `backend/app/database.py`, que ya no existe) se descartó.
- **Implementación:** la IA construyó los modelos a partir de FR-01..FR-15 y RNF-01..RNF-06 y los dejó como fuentes editables en `docs/diagramas/`:
  - **6 supuestos declarados (S1-S6)** para los vacíos que el propio caso pide cubrir: quién modifica el catálogo, qué pasa con un paquete cuya temporada terminó, desistimiento de reservas, estado borrador/publicado, cupo calculado y montos en CLP enteros.
  - **3 BPMN** (pool con carriles Administrador/Cliente y Sistema, eventos, compuertas XOR y almacén de datos): gestión de destinos (FR-01..04), armado y publicación de paquete (FR-05..07) y registro/autenticación/reserva (FR-08..15).
  - **Casos de uso:** 13 casos (CU-01..CU-13), 2 actores y relaciones «include» justificadas por R11, FR-06, FR-13 y FR-14, con una tabla de detalle.
  - **Clases en dos vistas:** dominio (`Usuario` abstracta → `Cliente`/`Administrador`, `Destino`, `Paquete`, `EstadoPaquete`, `Reserva`) y persistencia (`Repositorio<T>` abstracta + 4 repositorios SQLite).
  - **Matriz de trazabilidad** de los 21 requerimientos (BPMN → caso de uso → clase/método).

  Se reconstruyó la sección 3 del `.docx` (texto, 6 figuras y 3 tablas) y se actualizó el resumen de la sección 8.
- **Revisión técnica:**
  - **Herramienta de los BPMN:** el primer intento con Mermaid se descartó, porque Mermaid no tiene notación BPMN: dibujaba los carriles lado a lado y los flujos cruzaban el diagrama completo. En su lugar se escribió `generar_bpmn.py`, que dibuja la notación BPMN real en una grilla controlada. Cada diagrama se renderizó y se revisó visualmente, iterando hasta que ningún flujo atravesara un nodo.
  - **Casos de uso:** lo mismo se hizo con el diagrama de casos de uso. Las asociaciones cruzaban elipses ajenas y se corrigió anclándolas a los extremos de cada elipse.
  - **Diagrama de clases:** se dividió en dos figuras porque en una sola quedaba ilegible.
  - **Diseño orientado a objetos:** el modelo se diseñó pensando en el criterio 4.1.4 (implementar el UML aplicando encapsulamiento, herencia, polimorfismo y abstracción):
    - El precio y el total no tienen métodos de asignación (R7, R13).
    - `puede_gestionar_catalogo()` se resuelve por polimorfismo (RNF-03).
    - `Reserva.crear()` concentra R14 a R16.
  - **Correcciones de paso:** la sección 8 decía «7 no funcionales» y son 6, así que se corrigió. La sección 5.2 todavía describe `backend/app/database.py` y «cinco tablas». No se tocó porque corresponde al Paso 4 (persistencia) y debe reescribirse junto con el código.
- **Validación:**
  - **Estructura del `.docx`:** pasó el validador del skill de docx (esquema XSD, 383 → 550 párrafos).
  - **Revisión visual:** se exportó a PDF con Microsoft Word y se revisaron página por página las 6 figuras, las tablas y los saltos de sección (los BPMN van en páginas horizontales). Word también actualizó el índice: 3.1 en p. 7, 3.2 en p. 11, 3.3 en p. 13 y 3.4 en p. 15.
  - **Trazabilidad:** se verificó que los 15 FR aparecen en un BPMN, en un caso de uso y en una clase o método, y que ningún caso de uso ni clase carece de origen. RNF-06 (navegador web) es el único sin elemento de modelo propio, y así se declara en el informe.

## Cambio 5 — Metodología ágil: roles, Product Backlog y Sprint Backlog (sección 4 del Informe Técnico) (2026-10-01)

- **Objetivo:** completar el Paso 3 de la guía de evaluación (criterio 4.1.3, indicadores 4.1.3.G.9 a G.11 e I.12 de `rubrica 4.xlsx`): definir roles y responsabilidades, elaborar y priorizar un Product Backlog alineado con los requerimientos, y organizar el trabajo en un Sprint Backlog con tiempos y entregables reales. Usuario pidió encargarse personalmente de este paso ("yo voy con el paso 3").
- **Implementación:** se detectó que la sección 4 del `.docx` seguía con el cronograma del repo anterior (Sprint 0 "23-30 sep", entrega "5 oct" calculada desde esas fechas) y con referencias a RNF-05/RNF-06 que ya no corresponden a la numeración vigente desde el Cambio 3. Se confirmó con el usuario que la fecha de entrega sigue siendo el 5 de octubre de 2026, y se descartó y rehizo la sección 4 completa: roles (Logan = Líder de Proyecto + Clientes/seguridad y Reservas; Camilo = Destinos y Paquetes), Product Backlog (HU-01 a HU-05, cubriendo la totalidad de FR-01..FR-15 y RNF-01..RNF-06 sin dejar ninguno sin historia), y Sprint Backlog con el calendario real: Sprint 0 (1 oct, ya completado: requerimientos + modelado), Sprint 1 (2-3 oct: implementación de los 4 dominios), Sprint 2 (4 oct: integración, pruebas, seguridad, cierre del informe), Entrega (5 oct).
- **Revisión técnica:** el borrador de roles/Product Backlog/Sprint Backlog se presentó al usuario para su aprobación antes de escribirlo en el documento. Se editó el XML del `.docx` igual que en el Cambio 3 (desempaquetado, generación de las tres tablas, reempaquetado), reutilizando los mismos IDs de marcador (bookmark) que ya tenía la sección 4 para no romper el índice.
- **Validación:** se validó la estructura del `.docx` resultante con el validador del skill de docx (546 párrafos, sin errores de esquema) y se extrajo el texto de la sección 4 para confirmar que las tres tablas quedaron completas y con tildes bien codificadas.

## Cambio 6 — Esqueleto del backend y dominios Destinos (HU-01) y Paquetes (HU-02) (2026-10-01)

- **Objetivo:** iniciar el Paso 4 de la guía (criterio 4.1.4: implementar la solución respetando el modelo UML y los principios de la programación orientada a objetos, con persistencia y CRUD operativo). Según el reparto de la sección 4.1, Camilo implementa el esqueleto compartido y sus dominios, Destinos y Paquetes. Por decisión del usuario, en esta etapa solo se hace el backend: HU-03, HU-04 y el frontend quedan para Logan y el Sprint 2.
- **Implementación:** en `backend/`, con FastAPI y `sqlite3` de la librería estándar, siguiendo las Figuras 5 y 6 del informe:
  - **Esquema completo de 5 tablas** (`app/database.py`), con las restricciones de la sección 5.2.
  - **Clases de dominio** `Destino`, `Paquete` y `EstadoPaquete` (`app/dominio/`):
    - atributos privados y solo propiedades de lectura;
    - validación completa antes de asignar, para que un error no deje un objeto a medio modificar;
    - precio calculado con `Decimal` y fijado al publicar (R6, R7);
    - baja lógica (R8), cupo calculado (R14, S5) y paquete vencido según la fecha del día (R15).
  - **Persistencia:** `Repositorio[T]` abstracto, más `DestinoRepositorio` y `PaqueteRepositorio`.
  - **API:** 12 rutas CRUD (tabla de la sección 5.3) y un manejo de errores centralizado: 400 por regla incumplida, 404, 409 por integridad, 422 sin repetir el valor recibido y 500 sin traza interna.
  - **Pruebas:** 49 con pytest.
  - **Informe:** se actualizaron las secciones 5.2, 5.3, 6 (tres decisiones nuevas) y 8 para que describan lo realmente implementado. 5.2 citaba columnas que no existen (`password_hash`, `precio_publicado`) y decía que las reglas se validaban en el router.
- **Revisión técnica:** decisiones y correcciones hechas durante la implementación.
  - **Reglas solo en el dominio:** Pydantic valida únicamente tipos y largos, para que ninguna regla quede duplicada en dos capas que puedan contradecirse (RNF-05).
  - **Campos opcionales:** se detectó y corrigió que reutilizar un mismo `Field(max_length=100)` como valor por defecto volvía obligatorios los campos opcionales de las actualizaciones.
  - **Margen NaN:** se agregó el rechazo de un margen `NaN` o infinito, porque el JSON de Python los acepta y «margen ≥ 0» no los detecta.
  - **Ejemplo de float:** el primer ejemplo del informe para justificar `Decimal` era incorrecto, porque 83.001 × 1,15 da exacto en float. Se verificó numéricamente y se reemplazó por el caso real, 83.000 × 1,15 = 95.449,999… Ese caso quedó como prueba.
  - **`httpx` → `httpx2`:** se cambió porque Starlette marcaba `httpx` como obsoleto en las pruebas.
  - **Fecha del informe:** se corrigió una fecha («2 de octubre» → 1 de octubre, la fecha real del cambio).
  - **Pendiente para la integración:** las rutas que modifican el catálogo todavía no exigen autenticación de administrador (S1, RNF-03). Se dejará cuando exista el módulo de seguridad de HU-03. No se agregó un control simulado que aparentara proteger las rutas sin hacerlo.
- **Validación:**
  - **Pruebas:** pasan las 49 (`pytest`).
  - **Las pruebas detectan errores reales:** se rompieron a propósito R7 (que el precio publicado no cambie) y R8 (no borrar un destino usado). En ambos casos fallaron exactamente las pruebas de esa regla. Con R8 roto, la clave foránea de SQLite igualmente bloqueó el borrado (409), lo que confirma la segunda línea de defensa del esquema. Luego se restauró el código.
  - **Recorrido real con uvicorn**, con los datos del caso:
    - rechazo del nombre «valle del elqui» por duplicado;
    - precio de «Norte Grande» = 516.000;
    - publicación, y el precio se mantiene después de subir el costo del Salar a 400.000;
    - la baja del Salar lo deja «no disponible».

    Con `curl` de Git Bash los cuerpos con tildes no se enviaban en UTF-8; era un problema del cliente de prueba y se resolvió enviando los JSON desde archivos UTF-8.
  - **Informe:** pasó el validador del skill de docx (546 → 609 párrafos). Se exportó a PDF con Word para revisar las páginas 18 a 23, y se actualizó el índice.

## Cambio 7 — Dominios Clientes y seguridad (HU-03) y Reservas (HU-04) (2026-10-01)

- **Objetivo:** completar la parte de Logan Silva del Paso 4 (criterio 4.1.4) sobre el esqueleto que dejó el Cambio 6: HU-03 (registro, autenticación y perfil de clientes, FR-09 a FR-11, RNF-01 a RNF-03) y HU-04 (reservar un paquete y consultar historial propio, FR-12 a FR-15), además del diseño de seguridad de la sección 7.1 (hash de contraseña y token de sesión).
- **Implementación:** siguiendo exactamente el mismo patrón por capas del Cambio 6 (dominio → repositorio → API), sin introducir una arquitectura distinta para el nuevo código:
  - **Dominio** (`app/dominio/cliente.py`, `reserva.py`): `Cliente` (nombre, RUT, correo validado con formato, teléfono, `hash_contrasena` ya hasheada — el dominio nunca hashea, solo exige que la contraseña no llegue vacía) y `Reserva`, con el factory `Reserva.crear()` que valida en orden paquete publicado → vigencia (R15) → cupo (R14) → personas ≥ 1 (R16), y recién entonces fija el total (R13), igual que `Paquete.crear()` valida todo antes de asignar.
  - **Repositorios** (`cliente_repositorio.py`, `reserva_repositorio.py`): `ClienteRepositorio` con `buscar_por_correo`/`existe_correo` (R9); `ReservaRepositorio` que solo inserta, nunca actualiza (una reserva no cambia, R13).
  - **Módulo nuevo `app/seguridad/`** (no existía en el Cambio 6): `contrasenas.py` (hash/verificación) y `tokens.py` (JWT). Se mantiene separado del dominio porque no es una regla de negocio de Viajes Aventura sino infraestructura transversal de seguridad.
  - **API** (`clientes.py`, `reservas.py`): `POST /api/clientes`, `POST /api/clientes/sesiones`, `GET /api/clientes/yo`, `POST /api/reservas`, `GET /api/reservas`. Nueva dependencia `obtener_cliente_actual` (`dependencias.py`) que exige un token Bearer válido (`fastapi.security.HTTPBearer`, visible como candado en `/docs`) y obtiene el `cliente_id` del token, nunca de un parámetro de la solicitud (R11).
  - **Esquemas:** `ClienteSalida` (pública, sin RUT/teléfono) y `ClientePerfil` (solo para el propio cliente, con RUT/teléfono) — dos vistas distintas de la misma entidad para que R17 no dependa de que cada router recuerde excluir el campo.
  - **Pruebas:** 36 nuevas (`test_dominio.py` ampliado, `test_seguridad.py`, `test_api_clientes.py`, `test_api_reservas.py`), total 85.
  - **Informe:** se actualizaron las secciones 5.3 (tabla de rutas, avance del Sprint 1, conteo de pruebas), 6 (nueva decisión: passlib → bcrypt) y 7.1 (misma corrección), y 8 (estado y pendientes).
- **Revisión técnica:**
  - **passlib[bcrypt] no funciona:** la sección 7.1 original (del Cambio 4, antes de escribir código) especificaba `passlib[bcrypt]`, tal como sugiere buena parte de la documentación de IA sobre hashing en Python. Al instalarlo y probarlo, `passlib.context.CryptContext(["bcrypt"]).hash(...)` lanza `AttributeError: module 'bcrypt' has no attribute '__about__'`. Se investigó: passlib 1.7.4 es su última versión (2020) y nunca se actualizó para bcrypt ≥ 4.1, que eliminó ese atributo. No es un error de configuración, es una incompatibilidad real y conocida de dos librerías específicas. Se decidió no fijar `bcrypt<4.1` (congelaría una dependencia transitiva insegura a largo plazo) y en su lugar usar `bcrypt` directamente, sin pasar por passlib — menos una capa, y es la librería activamente mantenida. Se corrigieron el informe (secciones 6 y 7.1) y `requirements.txt` para que digan lo que el código realmente usa.
  - **Longitud de la contraseña:** bcrypt rechaza con `ValueError` una contraseña de más de 72 bytes en vez de truncarla en silencio (comportamiento de versiones nuevas de la librería). Se limitó `Contrasena` a 72 caracteres en el esquema Pydantic y además se capturó el `ValueError` en `hashear()` para convertirlo en `ReglaNegocioError` (400), no en un error 500 no controlado.
  - **Autenticación de administrador, fuera de alcance:** el pendiente que dejó el Cambio 6 (exigir login de administrador en las rutas de catálogo) no se implementó: ningún FR de la sección 2 lo exige — el caso nunca definió una cuenta ni credenciales para el administrador (ver sección 1.3 del caso, los socios son el "administrador"), y agregarlo habría sido diseñar un requerimiento que nadie pidió. Se documentó la decisión en el informe (sección 5.3) en vez de implementarlo o de simular una protección que no es real.
  - **Longitud de la clave JWT en las pruebas:** PyJWT advertía (`InsecureKeyLengthWarning`) porque las claves de prueba tenían menos de 32 bytes; se alargaron para que la salida de las pruebas quede limpia, igual que una clave real debe tener ese largo mínimo (no se documentó como hallazgo de seguridad porque las claves de prueba nunca protegen datos reales).
- **Validación:**
  - **85 pruebas pasan** (`pytest`), incluidas las 49 del Cambio 6 sin cambios.
  - **Prueba de extremo a extremo fuera de pytest:** se levantó la app con `TestClient` fuera de la suite de pruebas y se ejecutó a mano el flujo registrar → iniciar sesión → consultar `/api/clientes/yo` con el token, más `GET /docs`, confirmando que el candado de autenticación aparece en la documentación interactiva.
  - **Aislamiento entre clientes:** una prueba de API registra a dos clientes distintos, cada uno reserva, y verifica que el historial de uno no incluye la reserva del otro (R11).
  - **Informe:** pasó el validador del skill de docx (609 → 633 párrafos).
