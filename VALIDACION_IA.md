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
