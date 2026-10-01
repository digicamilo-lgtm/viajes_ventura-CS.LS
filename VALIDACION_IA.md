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
