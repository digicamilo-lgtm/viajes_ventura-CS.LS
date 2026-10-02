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

## Cambio 8 — Reparto del Sprint 2 (2026-10-01)

- **Objetivo:** el Sprint Backlog (Cambio 5) dejaba el Sprint 2 sin repartir entre los integrantes ("el equipo" de forma genérica); con los 4 dominios ya implementados (Cambio 6 y Cambio 7), había que decidir quién integra, quién revisa seguridad y quién construye el frontend antes de seguir.
- **Implementación:** el usuario decidió el reparto: **Camilo Sepúlveda** integra los 4 dominios en un flujo único de extremo a extremo y revisa la seguridad del sistema integrado (sección 7.3); **Logan Silva** construye el frontend React/Vite (HU-05) sobre las rutas ya existentes. Se actualizó la sección 4.3 del Informe Técnico (párrafo bajo el Sprint Backlog) y la sección 8 (ítems "Pendiente"), y el README ("Próximos pasos").
- **Revisión técnica:** el reparto es coherente con quién construyó cada pieza — Camilo hizo el esqueleto compartido en el Cambio 6 y conoce ambos lados de la API; Logan ya tiene clara la autenticación (HU-03) que el frontend tendrá que consumir, pero no construirá él mismo la integración de su propio código (evita que el mismo integrante revise su propio trabajo sin otro par de ojos).
- **Validación:** se verificó con el validador del skill de docx que el `.docx` no cambió de párrafos (633 → 633) tras los reemplazos de texto puntuales.

## Cambio 9 — Integración de los 4 dominios y revisión de seguridad del sistema integrado (2026-10-01)

- **Objetivo:** cumplir la parte de Camilo del Sprint 2 definida en el Cambio 8: integrar los 4 dominios en un flujo único de punta a punta y revisar la seguridad del sistema integrado (sección 7.3, criterio 4.1.5). También se resolvió el punto «pendiente de decidir» del Cambio 8, la autenticación de administrador.
- **Implementación:**
  - **Revisión del código de Logan (Cambio 7):** sigue el mismo patrón por capas y cumple el diseño de la sección 7.1: bcrypt con costo 12, algoritmo JWT fijado, clave en una variable de entorno, mensaje de error genérico y `cliente_id` tomado del token.
  - **Dos sospechas, demostradas antes de corregirlas** con un script contra el servidor real (uvicorn):
    - **Sobreventa por concurrencia:** en un paquete con cupo 5, 20 reservas simultáneas de 1 persona se aceptaron todas (cupo −15). La lectura del cupo y la inserción eran pasos separados, y es exactamente la falla del caso que el sistema debía resolver.
    - **Enumeración de correos por tiempo de respuesta:** un login fallido tardaba 214 ms con un correo registrado y 2 ms con uno inexistente, porque sin correo no se ejecutaba bcrypt.
  - **Decisión del usuario:** implementar la autenticación de administrador con la herencia del diagrama de clases, en vez de dejar el catálogo abierto como proponía el Cambio 7. Sin ella, cualquiera podía borrar el catálogo sin sesión, y el código no implementaba `Usuario` → `Cliente`/`Administrador`, que el UML (Figura 5) y el criterio 4.1.4 sí exigen.
  - **Cambios en el código:**
    - **Herencia del UML:** `Usuario` abstracta con `verificar_contrasena()` y el método abstracto `puede_gestionar_catalogo()`. `Cliente` (de Logan) ahora hereda de `Usuario`, con la misma firma, y suma `datos_publicos()` y la validación del RUT por módulo 11. `Administrador` es nueva.
    - **Persistencia del administrador:** tabla `administradores` y `AdministradorRepositorio`.
    - **Rol en el token:** el JWT lleva el rol, se rechaza un token sin rol y se exige una clave de al menos 32 bytes.
    - **Tiempo constante:** `simular_verificacion()` ejecuta bcrypt aunque el correo no exista.
    - **Transacción exclusiva:** `Repositorio.transaccion_exclusiva()` (`BEGIN IMMEDIATE`) envuelve la lectura del cupo y la inserción en `POST /api/reservas`.
    - **Autorización:** dependencias `obtener_usuario_actual`, `obtener_cliente_actual` y `obtener_administrador_actual`; esta última aplica el polimorfismo con `puede_gestionar_catalogo()`. Las rutas que modifican el catálogo exigen administrador (401 sin sesión, 403 con sesión de cliente).
    - **Rutas nuevas:** `POST /api/administradores/sesiones`, `GET /api/administradores/yo` y `GET /api/paquetes/publicados/{id}` (detalle público que no muestra borradores).
    - **Comando `python -m app.crear_administrador`:** pide la contraseña con `getpass`, exige 12 caracteres o más y no hay registro público de administradores.
  - **Pruebas:** de 85 a 129. Se agregaron:
    - `test_integracion.py`, con el caso completo y sus datos reales;
    - `test_concurrencia.py`;
    - `test_api_administradores.py` (autorización en 10 rutas, tiempo constante, comando de consola);
    - `test_errores.py`;
    - pruebas de token, de RUT y de herencia y polimorfismo.

    Las pruebas existentes se adaptaron: los helpers del catálogo envían el token de administrador, y las 3 pruebas de token de Logan usan la firma nueva `crear_token(id, rol)`.
  - **Informe:**
    - **3.3 y 3.4:** Figura 6 regenerada con `AdministradorRepositorio` y `transaccion_exclusiva()`.
    - **5.2 y 5.3:** tabla `administradores`, y tabla de rutas con una columna de acceso.
    - **6:** dos decisiones nuevas.
    - **7:** sección reescrita como implementación. La 7.1 tiene 3 filas nuevas, la 7.2 una viñeta sobre el RUT, y la 7.3 la tabla de 7 hallazgos con su evidencia antes y después, la checklist y los riesgos aceptados.
    - **8:** estado actualizado.
- **Revisión técnica:**
  - **El análisis estático no bastaba:** Bandit y pip-audit no detectaron ninguna de las dos fallas más graves; solo aparecieron al atacar el servidor en ejecución. Por eso cada hallazgo se demostró con una medición antes de darlo por cierto, y se volvió a medir después de corregirlo.
  - **Contra la conclusión del Cambio 7:** que ningún FR exija autenticación de administrador no significa que el modelo no la contemple. El supuesto S1, RNF-03, el caso de uso CU-03 (compartido) y la Figura 5 ya la modelaban. Se decidió con el usuario, explicando el riesgo concreto: borrar el catálogo sin sesión.
  - **Hallazgo latente al diseñar los roles:** con clientes y administradores en tablas distintas, un token con solo el id habría hecho que el cliente 1 actuara como el administrador 1. Por eso el rol es obligatorio en el token, y hay una prueba de ese escenario exacto.
  - **SonarLint (S6437):** marcó como contraseña comprometida el texto fijo usado para el hash ficticio. Era un falso positivo, pero se cambió por `secrets.token_bytes(32)`, que además impide adivinar ese hash. También se separaron las aserciones compuestas que SonarLint marcó en las pruebas nuevas (S9073).
  - **Velocidad de las pruebas:** las pruebas bajan el costo de bcrypt a 4 con `monkeypatch`; en producción sigue siendo 12. Por eso el tiempo constante se verifica contando las llamadas a bcrypt y no midiendo milisegundos, que sería una prueba frágil.
  - **SonarCloud no se ejecutó:** requiere vincular el repositorio a una cuenta. Se usaron Bandit (PyCQA) y pip-audit (PyPA), de PyPI, y se declaró así en el informe en vez de afirmar que se usó SonarCloud.
- **Validación:**
  - **Pruebas:** pasan las 129.
  - **Las pruebas detectan las fallas reales:** se desactivó a propósito cada corrección y fallaron sus pruebas.
    - Sin la transacción exclusiva, la prueba de concurrencia volvió a aceptar 20 reservas en vez de 5.
    - Sin la verificación ficticia, falló la prueba de tiempo constante.
    - Sin la autorización, fallaron 11 pruebas.
  - **Servidor real, antes → después**, con bcrypt en costo 12:
    - catálogo sin sesión: 201 → 401;
    - 20 reservas simultáneas con cupo 5: 20 aceptadas → 5 aceptadas y 15 rechazadas, cupo 0;
    - login fallido con correo registrado / inexistente: 214 ms / 2 ms → 216 ms / 220 ms.
  - **Bandit:** 0 hallazgos en 1.270 líneas. Como control positivo, sí detectó una consulta SQL concatenada en un archivo de prueba, lo que confirma que la herramienta funciona.
  - **pip-audit:** sin vulnerabilidades conocidas.
  - **Informe:** pasó el validador del skill de docx (633 → 721 párrafos). Se exportaron con Word las páginas 14 y 19 a 26 para revisarlas, se corrigió el ancho de la columna «Severidad» y se actualizó el índice.

## Cambio 10 — Frontend React/Vite (HU-05) (2026-10-01)

- **Objetivo:** construir el frontend que faltaba del reparto del Sprint 2 (Cambio 8): una aplicación React que consuma la API ya integrada (Cambio 9) para las 5 pantallas necesarias — catálogo público, detalle y reserva de un paquete, registro/login/historial de un cliente, y login más CRUD de destinos/paquetes de un administrador — cumpliendo la arquitectura de la sección 5.1 (Vite con proxy en desarrollo, build único a `backend/static/` para la entrega).
- **Implementación:** no existía ningún `frontend/` en el repo (se había borrado en el Cambio 1 y nunca se rehízo). Se creó desde cero con `npm create vite@latest -- --template react` más `react-router-dom`:
  - `vite.config.js`: proxy `/api` → `:8000` en desarrollo; `build.outDir` apuntando a `../backend/static` con `emptyOutDir`.
  - `api.js`: cliente `fetch` a `/api` que agrega `Authorization: Bearer` cuando hay sesión y traduce los errores del backend (`detail`) a excepciones de JavaScript.
  - `auth.jsx`: contexto de React con la sesión (`token`, `rol`, `perfil`) persistida en `localStorage`; `iniciarSesionCliente`/`iniciarSesionAdmin` llaman al endpoint de sesión correspondiente y luego a `/yo` para obtener el perfil.
  - 8 páginas en `pages/`, con rutas protegidas (`RutaCliente`, `RutaAdmin` en `App.jsx`) que redirigen a login si no hay sesión del rol correcto — una protección de interfaz, no de seguridad: la API ya rechaza la operación aunque el frontend se salte la redirección (RNF-03).
- **Revisión técnica:**
  - **Bug real de integración, no de la app:** al navegar directo a una ruta de React (`/admin`, `/paquetes/3`) sobre el build servido por FastAPI, el servidor respondía 404 en vez de la página. Causa: `StaticFiles(html=True)` (como estaba armado desde el Cambio 1) solo sirve `index.html` para `/`; para cualquier otra ruta sin archivo real, responde 404 porque no sabe que esa ruta le pertenece a React Router. Se reemplazó por una ruta comodín en `app/main.py` (`"/{ruta_spa:path}"`) que sirve el archivo estático si existe, y si no, `index.html` — dejando que el navegador resuelva la ruta del lado del cliente. Se verificó con `curl` que `/admin` pasó de 404 a 200 y que `/api/destinos` sin token siguió devolviendo 401 (el comodín no tapa las rutas de la API, porque FastAPI prioriza las rutas ya registradas).
  - **Rol nunca decidido por el frontend:** los componentes `RutaCliente`/`RutaAdmin` solo deciden qué pantalla mostrar; cualquier intento de saltárselos (ej. llamando la API a mano) sigue topando con `obtener_administrador_actual`/`obtener_cliente_actual` del backend, que leen el rol del token firmado (Cambio 9), no de nada que el navegador envíe.
  - **Historial de reservas sin nombre de paquete:** `ReservaSalida` (Cambio 7) no incluye el nombre del paquete, solo su id. Se decidió no modificar ese esquema para esto (afectaría las pruebas y el contrato ya probado del Cambio 7/9) y mostrar "Paquete #id" en `MisReservas`; queda anotado como una limitación de UX conocida, no resuelta por no ser parte de ningún FR.
- **Validación:**
  - **`npm run build`:** compila sin errores y deja el build en `backend/static/` (gitignorado, como ya estaba documentado en el Cambio 6).
  - **Recorrido de punta a punta con un navegador real:** se instaló Playwright (Chromium) y se automatizó el flujo completo contra el servidor único (`uvicorn` sirviendo el build): login de administrador → crear 2 destinos → crear y publicar un paquete → cerrar sesión → ver el paquete en el catálogo público → registrar un cliente nuevo → reservar 2 personas → ver la reserva en el historial propio. Se revisaron las capturas de cada paso y no hubo errores de consola ni de página. Los montos calculados coincidieron con las reglas de negocio: precio $516.000 ((310.000 + 120.000) × 1,20, R6) y total de la reserva $1.032.000 (516.000 × 2, R13), con el cupo disponible bajando de 12 a 10 (R14).
  - **Pruebas de backend:** las 129 siguen pasando después del cambio en `app/main.py` (el comodín no interfiere con ninguna ruta `/api`).
