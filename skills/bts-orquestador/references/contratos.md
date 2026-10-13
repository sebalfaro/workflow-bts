# Contratos del paquete BTS — 5.2

## Sobre común

Cada solicitud/respuesta incluye component (ORQ, BUS, EXT o VAL) y usa contract_version=bts-5.2, run_id, request_id, event_id, config_hash, ruleset_hash, schema_hash, provider_scope (null sólo antes de agrupar), row_context_id (null para inventario global), authorized_scope y observed_capabilities. Respuesta además: status, data, evidence, errors y dependencies. Usar el [esquema JSON](contratos.schema.json). Rechazar versión/hash/contexto inesperado con CONTRACT_REJECTED; no consumir parcialmente una respuesta de otra fila. null significa desconocido, no ausencia. IDs y montos son cadenas; fechas conservan literal separado de ISO.

Evidencia tiene ID único, alcance/contexto, archivo/hash o snapshot de inventario, página/localizador, literal, normalización, regla, REQ/DEC, método y fecha observada. Un error contiene code, component, scope, operation, attempt, literal_cause, retryable, next_action, affected_results. Toda salida sin resultado definido requiere error/revisión/dependencia explícita. Listas vacías de documentos sólo representan ausencia cuando completeness=true, incluyendo paginación y clasificación suficiente.

## ORQ

Entrada data: workflow_name, operational_stage (1,2,3 o incremental), source_ref o provider_names según etapa, source_snapshot, destination_registry, shared_checkpoint, operator y publishing_owner. Configuración centraliza IDs. Enlace de disparador distinto del maestro: CONFIG_CONFLICT. Nombre workflow/etapa o insumos requeridos ausentes: INPUT_MISSING.

Salida data: rows, results, excluded_rows, review_rows, pending, write_plans, write_receipts, checkpoints, counts y counts_denominator. Reportar cálculo y publicación por separado; etapas de auditoría no son etapas operativas. ORQ es único responsable de mutaciones, entrega y confirmación. Errores: CONFIG_CONFLICT, CAPABILITY_MISSING, SCHEMA_UNKNOWN, SHEET_AMBIGUOUS, ROW_ID_AMBIGUOUS, CONCURRENT_EDIT, WRITE_UNCERTAIN, PERSISTENCE_FAILED.

## BUS

Entrada data: root_id, provider_literal, corroborated_number nullable, previous_inventory, mode (drive o local_snapshot), local_snapshot_provenance si local. En Drive, comprobar padres/raíz y paginación; local no acredita actualidad Drive.

Salida data: search_status (FOUND_UNIQUE, NOT_FOUND, AMBIGUOUS, TECHNICAL_PENDING), folder_id, parent_chain, candidates, excluded_candidates, inventory, completeness, query_log, anomalies. FOUND_UNIQUE exige exactamente una carpeta principal compatible, pero completeness puede ser false si inventario falla; ORQ no interpreta unicidad como lectura completa. NOT_FOUND exige búsqueda completa de carpetas. Subcarpetas duplicadas se recorren, carpetas principales ambiguas se revisan. Errores: ROOT_UNREADABLE, LIST_INCOMPLETE, PROVIDER_INVALID, MULTIPLE_MATCHES, OUTSIDE_ROOT, SHORTCUT_UNVERIFIED.

## EXT

Entrada data: source_id, current_mime, tab, range, source_snapshot, identity_registry, existing_sheet_registry. source_snapshot preserva valores originales, presentados, fórmulas/cache, tipos, localizadores y completeness.

Salida data: rows (source_row_id, row_context_id, A:F, source_location, source_snapshot_hash), exact_provider_groups, excluded_rows con causa, review_rows, identity_reconciliation y persistence_plan. Contar ocurrencias, no personas únicas. Si identidad de fila no es reconciliable, no reasignar IDs por ordinal. EXT no escribe fuente ni destino. Errores: SOURCE_UNREADABLE, TAB_MISSING, HEADER_AMBIGUOUS, IDENTIFIER_LOSS, PROVIDER_MISSING, DESTINATION_AMBIGUOUS.

## VAL

Dos modos en la misma skill: index_provider y evaluate_context. Primero index_provider recibe inventario, archivos/hashes, filas A–F del proveedor y devuelve extracted_facts, relations, associations, orphan_documents, classification_completeness e issues. No devuelve cumplimiento en ese modo.

evaluate_context recibe un row_context_id, snapshot A:F, índice versionado, inventario/completitud, revisiones humanas y resultados previos. Devuelve selected_sets, excluded_sets y results_by_logical_column para las nueve claves G,H,I,J.montos,J.clausulas,K,L,M,N. La respuesta conserva contexto; un resultado SIN_EVALUAR con dependency_ids cubre una ruta pendiente. Agregar por fila después de considerar conjuntos, nunca sobrescribir por PDF sucesivo. VAL no publica.

ColumnResult requiere logical_key, row_context_id, applicability, document_outcome, processing_state, output_literal, predicates, evidence_ids, req_ids, dec_ids, dependency_ids, issues, input_versions y selected_set_ids. Ok necesita cada precondición demostrada y ningún conflicto irresuelto que afecte ese testigo. Predicados auxiliares no son ColumnResult.

Errores VAL: DOWNLOAD_FAILED, HASH_MISMATCH, OCR_UNAVAILABLE, TEXT_UNREADABLE, IDENTITY_CONFLICT, LINK_UNPROVEN, SCOPE_AMBIGUOUS, DATE_AMBIGUOUS, CURRENCY_REVIEW. Falta de herramienta es pendiente técnico; lectura realizada con contenido insuficiente es revisión. Datos de otra persona/proveedor no se aceptan aunque coincida hash.

## Recepción y persistencia

Validar esquema; cotejar correlación con solicitud, alcance, hashes y existencia de evidence_ids; rechazar referencias circulares o sin testigo externo que pretendan demostrar identidad. Aristas deben referir hechos/localizadores reales. Una asociación CONFIRMADA requiere evidencia de identidad y vínculo; el esquema sólo comprueba forma, el agente corrobora significado.

Toda operación externa exige capacidad observada para la cuenta/recurso en ese contexto y autorización operativa. D-01–D-15 en [capacidades.md](capacidades.md) localizan impedimentos. Un resultado planeado no genera receipt. El adaptador devuelve valores/tipos e identidad realmente leídos tras la escritura; aplicar [publicacion.md](publicacion.md).

## Contrato 5.2: revisiones de lectura

ColumnResult añade review_issue_ids obligatorio, vacío cuando no hay incidencia activa. VAL evaluate_context añade review_issues y review_output obligatorios; ORQ comprueba referencias/contexto y renderiza P central. Incidencia activa ligada a un resultado impide CUMPLE, AUSENTE y NO_APLICABLE; output_literal=null conserva histórico marcado obsoleto, sin sobrescribirlo como vigente. ReviewIssue conserva documento ID/nombre, localizador conocido o null, claves afectadas, evidencia, motivo y status. Referencias semánticas y correspondencia de review_output requieren comprobación más allá del schema. Clientes 5.1 no deben consumir 5.2 silenciosamente; actualizar todos componentes y hashes juntos.
