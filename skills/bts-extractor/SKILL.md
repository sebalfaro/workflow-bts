---
name: bts-extractor
description: "Leer la fuente de trabajadores BTS en A–F, conservar filas repetidas y preparar su agrupación exacta por proveedor con identidad estable y planes de reutilización de Sheets."
---

# bts-extractor

Estado: distribución pública candidata 0.7.1-rc.1, contrato bts-5.2; Fase 7 PARCIAL y sin aprobación para producción. Leer autoridad/configuración y contratos del orquestador antes de usar el procedimiento. Mantener las cuatro carpetas juntas. Operaciones externas requieren configuración local, autorización y capacidades corroboradas. No contiene evidencia privada ni decide ingreso.

## Leer fuente

Leer maestro de configuración, Hoja 1, A:F tras comprobar MIME actual y [transporte](../bts-orquestador/references/capacidades.md). No convertir ni modificar fuente. Enlace distinto: CONFIG_CONFLICT. Sin acceso/lector o pestaña: dependencia localizada.

Preservar exactamente A Apellido, B Nombre, C DNI, D Proveedor, E Función, F Accesos con tipos, literal/formato, fórmulas/cache y localizador. CUIT hallado en documentación sirve como evidencia de identidad; no añadir séptima columna fuente. No recortar ni rellenar identificadores numéricos. Fórmulas sin caché suficiente o ceros perdidos van a revisión.

## Seleccionar y agrupar

Comprobar encabezado por etiquetas/conjunto/estructura; excluir sólo encabezados demostrados y filas totalmente vacías. Continuar tras huecos hasta límites verificados. Fila dudosa permanece en revisión; D vacía no hereda proveedor. Agrupar por D literal exacta, sin fusionar nombres que BUS normaliza igual. Contar ocurrencias y justificar cada exclusión.

## Identidad y destinos

Aplicar [identidad](../bts-orquestador/references/identidad.md): UUID persistente por ocurrencia y contexto; reconciliar nuevas/alteradas/retiradas con prueba. Nunca deduplicar por DNI, hash de A–F o ordinal mutable. Si repetidas no pueden reconciliarse, ROW_ID_AMBIGUOUS sin reasignación automática.

Planear Sheet por proveedor: ID/carpeta/proveedor literal/esquema; cero compatibles plan de crear, uno reutilizar, varios revisión. Nombre del archivo exactamente D. Para nuevo Sheet preparar A:F conservadas y resultados G:O vacíos; para existente actualizar sólo cambios, sin vaciar resultados válidos. Esquema anterior G:N requiere migración comprobada D-05. EXT no ejecuta writes: devuelve persistence_plan a ORQ.

## Salida

Entregar rows, exact_provider_groups, excluded_rows, review_rows, identity_reconciliation y persistence_plan con localizadores y hashes. Trabajador nuevo dispara asociación del índice ya existente, incluso documentos SIN_CORRESPONDENCIA_EN_FUENTE. Centralización conserva todas las filas por source_row_id/row_context_id; no la realiza EXT de manera independiente.
