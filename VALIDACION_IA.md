# Validación de uso de IA — Viajes Aventura

Registro de cada cambio del proyecto hecho con apoyo de IA. **Esto aplica a ambos integrantes**, cada uno con la IA que use: antes de cerrar cualquier cambio de código o documentación, hay que agregar aquí una entrada numerada "Cambio N" y actualizar `README.md`. Por cada cambio se documenta:

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
