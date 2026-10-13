---
name: bts-orquestador
description: "Coordinar las etapas del workflow documental BTS 2026, sus cambios, recuperación y publicación compartida por proveedor y en la salida central."
---

# bts-orquestador

Estado: distribución pública candidata 0.7.1-rc.1, contrato bts-5.2; Fase 7 PARCIAL y sin aprobación para producción. Leer autoridad/configuración y contratos del orquestador antes de usar el procedimiento. Mantener las cuatro carpetas juntas. Operaciones externas requieren configuración local, autorización y capacidades corroboradas. No contiene evidencia privada ni decide ingreso.

## Flujo y entrada

Recibir nombre del workflow, etapa operativa e insumos de [contratos](references/contratos.md). Confirmar versión del paquete, configuración, responsable de publicación y estado compartido. No seleccionar trabajo sólo por celdas vacías. Para revisión incremental leer ambas fuentes de cambio: tabla maestra e inventario documental. Frecuencia acordada: dos corridas diarias iniciadas por equipo, sin horarios/automatización instalados.

## Etapas

1. Etapa 1: usar [EXT](../bts-extractor/SKILL.md) para leer A:F por MIME, conservar ocurrencias y planear creación/reutilización de Sheets. Fuente sólo lectura. Conservar resultados existentes independientes.
2. Etapa 2: por proveedor, usar [BUS](../bts-buscador/SKILL.md) para identidad de carpeta e inventario recursivo. Ambigüedad principal suspende ese proveedor; subcarpetas repetidas se recorren. Descargar incrementalmente según [índice](references/indice.md).
3. Pedir a [VAL](../bts-validador/SKILL.md) index_provider para extracción/asociación neutral de todos los documentos disponibles; registrar archivos sin correspondencia, genéricos y huecos de lectura. Después evaluate_context por cada fila afectada, sin trasladar asociación por mero DNI/hash. Correlacionar y comprobar todas respuestas.
4. Usar [estados](references/estados.md) para invalidar cambios y sus consumidores, preservar independientes y retomar pendientes técnicos. Cerrar contexto de fila sólo tras checkpoint durable; invalidar inventario activo al cambiar proveedor. No prometer purga de historial.
5. Publicar resultados según [publicación](references/publicacion.md): intención/evidencia compartidas, preimagen/identidad, escritura y readback de proveedor; consolidar la misma versión por fila/contexto en salida independiente. Actualizar commit compartido sólo con recibos comprobados. No interpretar resultado documental como permiso de ingreso.
6. Etapa 3: reportar por proveedor/fila/verificación, revisiones y dependencias; distinguir cálculo terminado, proveedor actualizado, central pendiente y commit compartido. Informar fecha/alcance de snapshot y denominadores. Si es sólo presentación, no reejecutar evaluación ni mutación.

## Bloqueos y continuidad

Una capacidad ausente detiene sólo consumidores dependientes según [capacidades](references/capacidades.md). No simular éxito ni pedir al usuario que haga manualmente operaciones que la herramienta sí permite dentro del alcance. Pedir datos/acceso faltantes de forma localizada. Escritura incierta: leer antes de repetir; creación incierta: recuperar por operación/ID, nunca crear otro archivo a ciegas. D-11/D-12 sin configurar permite preparación local, no publicación final. Sin responsable/escritor único comprobable, preparar sin mutar.

Comparaciones mecánicas en [auxiliares](references/auxiliares.md). Aplicar [layout](references/layout.json); G:O es decisión técnica, con claves originales preservadas. Nunca cargar recomendaciones rechazadas de fases anteriores como reglas.

### DEC-019 — lectura insuficiente

Aplicar [recuperación y Revisar](references/lectura-insuficiente.md). Mantener review_issue_ids, review_issues y review_output de contrato5.2; no inferir ausencia por OCR negativo dudoso. VAL entrega datos; ORQ publica P central con documento/localizador y relectura.
