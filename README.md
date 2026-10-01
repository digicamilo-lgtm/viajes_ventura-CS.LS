# Viajes Aventura — Sistema de gestión de agencia de viajes

Proyecto de la asignatura **TI3V21 Programación Orientada a Objeto Seguro** (INACAP Valparaíso), Unidad 4. Profesor: **Rubén Schnettler**.

**Integrantes:** Logan Silva Jara y Camilo Sepúlveda.

**Estado:** Informe Técnico Grupal en elaboración (`Informe_Tecnico_Viajes_Aventura.docx`) — secciones 2 (requerimientos funcionales y no funcionales) y 3 (modelamiento UML/BPMN) completas. Sin código todavía.

## Material de referencia

- `POO-TI3V21-Caso-Viajes-Aventura.pdf` — caso de estudio.
- `TI3021_U4_ES_GUÍA.pdf` — guía de la evaluación.
- `rubrica 4.xlsx` — Rúbrica N°2 (Informe Técnico Grupal y Defensa Argumentativa Individual), con los 5 criterios 4.1.1-4.1.5 y sus indicadores grupales/individuales.
- `6_poo_proyecto_consolidacion_rubensch.pdf` — material de consolidación del curso.

## Entregables

- `Informe_Tecnico_Viajes_Aventura.docx` — Informe Técnico Grupal (requerimientos, modelamiento UML/BPMN, metodología ágil, arquitectura y seguridad). Se evalúa con la Rúbrica N°2 (30% de la nota).

## Diagramas

`docs/diagramas/` contiene las fuentes editables y las imágenes de los diagramas de la sección 3 del Informe Técnico:

- `generar_bpmn.py` → `bpmn-1-gestion-destinos`, `bpmn-2-publicar-paquete` y `bpmn-3-reservar-paquete` (`.svg` + `.png`). Regenerar los SVG: `py generar_bpmn.py`.
- `generar_casos_uso.py` → `casos-de-uso` (`.svg` + `.png`). Regenerar el SVG: `py generar_casos_uso.py`.
- `clases.mmd` (dominio) y `clases-persistencia.mmd` (repositorios), en Mermaid. Regenerar: `mmdc -i clases.mmd -o clases.png -c config.json -s 2 -b white`.

Si se modifica un diagrama, hay que regenerar su `.png` (los SVG se pueden exportar desde cualquier navegador) y reemplazar la figura correspondiente en el Informe Técnico.

## Trazabilidad

Cada cambio del proyecto (código, documentación o avance del Informe Técnico) se registra en `VALIDACION_IA.md` (objetivo, implementación, revisión técnica y validación) y se refleja en este README. **Convención del repo:** cualquiera de los dos integrantes (y la IA con la que trabaje cada uno) debe seguir este mismo ciclo — actualizar `README.md`, `VALIDACION_IA.md` y, si corresponde, `Informe_Tecnico_Viajes_Aventura.docx`, en cada cambio, antes de hacer commit. Último cambio: Cambio 4 — modelamiento de la solución con BPMN, casos de uso y diagrama de clases UML (2026-10-01).

## Próximos pasos

1. ~~Levantar requerimientos a partir del caso de estudio.~~ ✅ hecho (Cambio 3).
2. ~~Modelar la solución (BPMN, casos de uso, diagrama de clases UML).~~ ✅ hecho (Cambio 4).
3. Definir metodología ágil (roles, Product Backlog, Sprint Backlog).
4. Implementar por dominios (backend + frontend) y seguridad (autenticación).
