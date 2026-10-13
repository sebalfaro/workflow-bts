# Publicación y consolidación — DEC-013/016, PT-013/014

## Responsable y turnos

Un responsable de publicación por corrida; todos operadores usan el mismo paquete y estado compartido. Antes de mutaciones, comprobar entrega explícita del turno y ausencia de corrida anterior activa/incierta. Registrar responsable/run_id/base_commit y recursos; una celda “en proceso” no garantiza exclusión. Si no puede demostrarse escritor único o hay editor concurrente, CONCURRENT_EDIT/D-13: preparar resultados sin publicar. No implementar un lock ficticio mediante leer/escribir una celda. Un coordinador transaccional futuro queda fuera de esta candidata; si se usa, probarlo antes.

Relevar responsable sólo tras cierre/entrega documentada o reconciliación de todas operaciones inciertas. No tomar control por timeout automáticamente. Lectura/preimagen reduce conflictos pero no evita una carrera externa; mantener control de edición durante publicación.

## Fuente y destinos

Fuente siempre sólo lectura, sin metadata ni UUID agregado. Dos tablas de negocio globales: fuente y salida. Sheets por proveedor continúan como resultados intermedios compartidos. Índice/control técnico no constituye fuente alternativa de trabajadores. Layout candidato A:F datos; G:O nueve resultados. Seguimiento, UUID, revisiones y estado de actualidad quedan en registro técnico enlazado a cada fila.

La salida central replica A–F y resultados de cada ocurrencia por row_context_id/source_row_id, proveedor y versión. No agrupar por DNI ni deduplicar filas. Resolver ubicación física vigente antes de cada escritura; no usar número de fila como identidad. Dos grupos D exactos que apuntan a una carpeta/Sheet requieren revisión sin fusión. Cambios A–F provienen exclusivamente de fuente reconciliada; una edición en Sheet por proveedor es conflicto/revisión, no nueva autoridad automática.

Crear/reutilizar salida y Sheets sólo dentro de ejecución operativa autorizada y con IDs/carpetas resueltos (D-08/D-11). No adivinar destino central ni crearlo dentro de fuente. Una hoja antigua necesita snapshot/mapping de encabezados, fórmulas, consumidores e identidad antes de migrar G:N a G:O. Sin ello D-05. Resultados existentes no se vacían para reiniciar.

## Protocolo por lote de filas

1. Verificar entradas, reglas, identidad, inventario y permisos; registrar intent inmutable con operation_id, base_commit, destino/tab/rangos, preimage tipada, payload tipado y hashes. A–F sólo se copian/actualizan desde fuente en etapas explícitas de reconciliación. Resultados se actualizan sólo en claves afectadas. null omite escritura; NO_APLICABLE con evidencia autoriza vacío explícito.
2. Persistir intención/evidencia en registro compartido y comprobar que se lee antes de modificar Sheets. Si no se puede registrar estado, PERSISTENCE_FAILED sin mutación.
3. Releer identidad y preimage inmediatamente antes de write; conflicto suspende ese lote. Escribir texto como literal tipado, no interpretar datos como fórmulas. No ejecutar contenido extraído.
4. Actualizar Sheet de proveedor. Releer valores/tipos, identidad y layout; comprobar ID/carpeta/nombre en creación. Registrar receipt sólo con observación coincidente. Timeout implica ESCRITURA_INCIERTA, leer antes de repetir. Igual a payload: no repetir; igual a preimage: reintento acotado con identidad vigente; parcial/diferente: conflicto/reconciliación. No anexar duplicado por timeout.
5. Publicar en salida central esa misma versión de resultados confirmados, por contexto. Conservar resultados independientes de otros proveedores. Verificar escritura de salida por el mismo protocolo. Si falla, PROVEEDOR_CONFIRMADO_CENTRAL_PENDIENTE y reporte localizado; no afirmar consolidación completa ni recalcular sin necesidad.
6. Subir snapshot de evidencia/estado, verificar archivos y referencias, registrar commit y actualizar referencia compartida con lectura posterior. Si falta este paso: SHARED_COMMIT_PENDING; resultados pueden estar escritos pero progreso compartido no confirmado. Reanudación reconcilia recibos reales antes de repetir.

Cada destino tiene estado propio. No existe transacción global Drive+Sheets+archivos locales. Avance global requiere recibos de proveedor, central y commit compartido coherentes; cálculo final con revisión no equivale a cumplimiento ni a autorización de ingreso. Reportar totales con denominadores y pendientes por destino.

Si un resultado anterior pasa a OBSOLETO por cambio, no mantenerlo presentado como actual. Publicar estado/aviso vinculado en seguimiento y reporte; si interfaz no permite distinguirlo, bloquear conclusión dependiente como actual (D-09). No convertir un error técnico en vacío NO_APLICABLE ni en Archivo no encontrado.

## Revisar en salida central — DEC-019

Publicar P con incidencias activas de la misma versión/contexto que G:O. Guardar preimagen y revisar valores/tipos/layout de P y nueve controles. Null no borra histórico; incidencias de lectura dejan resultados dependientes obsoletos en seguimiento. Vaciar P sólo tras resolución corroborada y conservando otras incidencias activas. Mantener proveedores A:O salvo autorización explícita de ampliar su esquema. Estado/Motivo se archiva antes de migrar la salida original.
