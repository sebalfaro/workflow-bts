---
name: bts-validador
description: "Indexar y asociar documentación de trabajadores BTS y evaluar sus reglas fiscales, AP, ART, alta y SVO por contexto, con evidencia y revisiones localizadas."
---

# bts-validador

Estado: distribución pública candidata 0.7.0-rc.1, contrato bts-5.1; Fase 7 PARCIAL y sin aprobación para producción. Leer autoridad/configuración y contratos del orquestador antes de usar el procedimiento. Mantener las cuatro carpetas juntas. Operaciones externas requieren configuración local, autorización y capacidades corroboradas. No contiene evidencia privada ni decide ingreso.

## Recursos y modos

Leer [reglas](../bts-orquestador/references/reglas.md), [identidad/evidencia](../bts-orquestador/references/identidad.md) e [índice](../bts-orquestador/references/indice.md). Mantener separación de extracción, asociación y evaluación; usar contrato index_provider antes de evaluate_context. No escribir Sheets.

## Extraer y asociar — index_provider

Procesar cada contenido/hash una vez por versión de extractor, conservando todas ubicaciones y procedencia. Inspeccionar por página texto/cid/tablas/cortes; OCR selectivo o imágenes con lector disponible, corroborando visualmente campos dudosos. Falta de lector es pendiente técnico; lectura realizada insuficiente es revisión documental. No corregir números ni expandir nombres por suposición.

Extraer hechos neutrales con roles de personas, categorías, identificadores, fechas, pólizas, montos y cláusulas; nunca Ok. PDF puede ser multicategoría/multipersona. DNI/CUIT/nombre completo proponen correspondencias, luego corroborar según DEC-006/015; nombre sin ID no confirma. Un CUIT de empleador o entidad de cláusula no identifica trabajador. Documentos sin fila fuente se conservan sin crear trabajadores.

Construir aristas de identidad/vínculo y conjuntos compatibles por trabajador/proveedor/aseguradora/póliza/alcance/fechas. No unir documentos por compañía, nombre de archivo o DNI solo. Aplicar exclusión expresa de anulado/reemplazado únicamente a tramo/persona/cobertura sustituida. Duplicados exactos reutilizan extracción; múltiples pagos/pólizas se conservan. Documento válido fuera de carpeta se admite registrando ubicación discordante. Inventariar/marcar todos los archivos del ámbito disponible antes de pasar a evaluación.

## Evaluar — evaluate_context

Abrir contexto aislado con A–F/versiones/índice. Determinar aplicabilidad con cobertura corroborada; no inferir NO_APLICABLE por ausencia ni por búsqueda incompleta. Aplicar todas las tablas de reglas para G,H,I,J.montos,J.clausulas,K,L,M,N. G y K lógica son informativas, nunca Ok. H compara sólo vencimiento; I admite algún pago parcial dentro del período confirmado; AP separa montos y cláusulas y sólo informa fechas en K; ART/L/N conservan horizonte propio.

Aplicar comparaciones exactas de [auxiliares](../bts-orquestador/references/auxiliares.md) sólo tras normalización documental corroborada. Un booleano de fecha/monto no demuestra identidad, vínculo o cláusula. Evaluar todos conjuntos no excluidos: un testigo válido puede satisfacer la verificación; no fabricar póliza compuesta. Montos y cláusulas AP pueden tener testigos compatibles válidos distintos, identificados separadamente.

Conservar todos incumplimientos y revisiones afectadas; no ocultarlos tras Ok. Testigo con reemplazo/identidad/alcance irresuelto no es válido. Diferencia parcial de nombre con DNI corroborado aplica DEC-018: observación en Identificación laboral, sin bloquear otras verificaciones por ese motivo. Falta de cifra de invalidez sólo observación no bloqueante; franquicia fuera de evaluación/salida. Aplicar tolerancias de entidades separadas de tolerancias de nombres del trabajador.

## Salida y pendientes

Devolver nueve ColumnResult con evidencia, predicados, REQ/DEC, dependencias y conjuntos seleccionados/excluidos; resultados pendientes usan SIN_EVALUAR y dependencia explícita, output_literal=null. Ausencia exige búsqueda/clasificación suficiente del proveedor; documento ilegible y error técnico nunca se convierten en ausencia. K conserva todos intervalos/huecos/horas/alcance. Revisión humana se registra literal con alcance/versión; no decidirla automáticamente.

Liberar contexto activo después de entregar resultado al checkpoint ORQ; sólo caché neutral por hash es reutilizable, asociaciones siempre contextualizadas. Error o respuesta de otro contexto se rechaza; continuar verificaciones independientes que tengan evidencia suficiente. No autorizar ingreso ni declarar capacidades externas probadas.

### Actualización general DEC-018

Regla general DEC-018: una diferencia parcial del nombre, con DNI del trabajador corroborado y coincidente con la fila fuente, se registra únicamente como observación nominal en Identificación laboral (G física), conservando la clasificación laboral y los nombres literales de fuente/documento. No bloquea por sí sola H:O: evaluar cada documento según su identidad, aplicabilidad, vínculos, vigencias y condiciones propias. El DNI debe pertenecer al trabajador, no al tomador/empleador/tercero. CUIT/CUIL puede corroborarlo conforme DEC-006; DNI explícito discordante con DNI central del CUIT permanece bloqueante. No aceptar diferencias totales de identidad, identificadores contradictorios, lectura dudosa o asociaciones insuficientes. No unir pólizas ni copiar resultados por DNI solamente. Conservar la observación y evidencia también en el registro técnico; no repetir la observación nominal en otras columnas ni ocultar incumplimientos independientes. No corregir nombres ni DNI de la fuente.
