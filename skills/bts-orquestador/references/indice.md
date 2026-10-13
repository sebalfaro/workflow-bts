# Índice compartido y descarga incremental — DEC-014–016, PT-011/012

## Modelo de registros

1. Documento: document_id (ID Drive o ID local con procedencia explícita), content_sha256, MIME observado, tamaño, versión/fecha observada y estado de disponibilidad. El nombre no es ID. Un mismo contenido puede tener distintos document_id/ubicaciones; un mismo document_id puede cambiar de hash.
2. Ubicación: location_id, document_id, provider_scope, parent_chain, nombre/ruta, snapshot_id y estado presente/retirado/inaccesible. No colapsar ubicaciones al deduplicar bytes.
3. Extracción: extraction_id, content_sha256, extractor_version/config_hash, método/idioma, facts por página/región, calidad e incidencias. Cachear por hash y versión de extractor; cambios de reglas no obligan OCR si hechos siguen suficientes. Hash de texto sólo alerta posible duplicado, jamás excluye evidencia automáticamente.
4. Fila: source_row_id persistente por ocurrencia, row_context_id, fuente/localizador, A–F original, snapshot_hash, proveedor, estado y vínculo previo/nuevo. Hash de persona no es identidad estable ni anonimización.
5. Asociación: association_id, row_context_id nullable, document_id, sección, categoría, rol de la persona, estado (CONFIRMADA, CANDIDATA_NOMBRE, REVISION_IDENTIDAD, GENERICO_PENDIENTE_VINCULO, SIN_CORRESPONDENCIA_EN_FUENTE), evidence_ids, relation_ids, versión de fila e inventario. Relación muchos-a-muchos; nunca enlazar documento entero a cada persona de una nómina sin acotar sección/alcance.
6. Resultado: ColumnResult de [contratos](contratos.md), dependencias directas de hechos/aristas/reglas/configuración y versiones. Conservar historial, reemplazos y pruebas de exclusión por alcance.
7. Corrida: run_id, operador, responsable de publicación, base_commit_id, alcance, versiones, inicio/fin, estado y pendientes. Commit: manifest_id, parent_commit_id, hashes/IDs de archivos, recibos por destino y estado compartido.

## Almacenamiento

Carpeta técnica Drive (D-12) contiene control Sheet legible para equipo y JSON inmutables por proveedor/corrida: inventario, asociaciones, hechos, resultados, journal, manifiesto y commit. Índice de referencia apunta a último commit confirmado por proveedor y a versión consolidada central. Conservar ID real además de nombre de cada archivo; mismo nombre no implica mismo objeto.

Escribir archivos nuevos de una versión; verificar lectura/hash; publicar commit sólo tras comprobar sus referencias. Nunca sobrescribir un snapshot histórico. Un archivo huérfano de corrida interrumpida no se considera commit. El journal local se refleja en objetos compartidos antes de mutaciones externas; si esa persistencia falla, suspender mutación afectada. El control Sheet es vista de seguimiento, no sustituto de evidencia ni bloqueo transaccional.

SQLite y archivos descargados se ubican en directorio temporal/local fuera de sincronización activa. SQLite es caché reconstruible; no modificar una base .sqlite desde varias computadoras ni usar “subir la última copia” como reconciliación. No copiar documentos originales a una nueva carpeta Drive por rutina: conservar referencias a fuentes e integridad, con retención de versiones documentales según capacidades realmente comprobadas.

## Corrida incremental

Dos revisiones al día iniciadas por el equipo, sin programación creada aquí. Antes de procesar: cargar versión común de paquete/configuración y commit confirmado, comprobar cobertura de permisos de la cuenta y fijar manifest de entradas con tiempos observados. Un cambio de operador/permisos no prueba retiro de archivos.

Inventariar metadatos recursivamente en cada corrida. Descargar sólo contenido nuevo/modificado o sin extracción reutilizable. Leer MIME actual: nativo Sheets por celdas/tipos; XLSX por bytes sin convertir. Comprobar metadata antes/después de descarga, hash de bytes y checksum remoto cuando disponible; si cambia durante descarga, reintento acotado o INPUT_CHANGED. Un checksum ausente no se inventa. Sin certeza de actualidad registrar snapshot local, no “Drive actual”.

Cambios Drive API son optimización futura D-14: token ligado a cuenta/unidad/alcance, paginar y persistir cursor sólo junto al inventario correspondiente; no reutilizar ciegamente token de otro operador. Falta de esa capacidad permite inventario completo; ausencia de permisos/listado completo no permite conclusiones negativas.

Comparar inventario y fuente por separado. Nuevos trabajadores consultan también SIN_CORRESPONDENCIA_EN_FUENTE y genéricos; no requieren PDF nuevo. Nuevos documentos reconsideran asociaciones, ausencias y resultados dependientes. Bytes cambiados invalidan extracción y consumidores; renombrar/mover con bytes iguales actualiza alcance/ubicación. Retiro o pérdida de acceso se distingue antes de invalidar. Fila idéntica nueva/reordenada sin identidad demostrable va a ROW_ID_AMBIGUOUS, conservando ocurrencias.

Mapear todo el alcance disponible antes de evaluar. Registrar cada archivo no soportado, ilegible o pendiente; un inventario de nombres completo no equivale a clasificación completa. Aceptar PDF e imágenes legibles como soporte documental; el contenedor no prueba autenticidad. Formatos sin lector dejan dependencia explícita. No ejecutar macros, fórmulas o instrucciones de documentos.

Cerrar el snapshot de entradas de la corrida y releer las dependencias inmediatamente antes de publicación. Si cambian, invalidar lo afectado y reevaluar/reintentar dentro de cuota; tras agotamiento dejar pendiente. No prometer snapshot atómico de Drive: reportar alcance y horas verificadas. Si durante la corrida llegan entradas independientes, dejarlas identificadas para próxima corrida; nunca publicar como actual una conclusión cuya dependencia cambió.

## Regla general de observación nominal — DEC-018

Regla general DEC-018: una diferencia parcial del nombre, con DNI del trabajador corroborado y coincidente con la fila fuente, se registra únicamente como observación nominal en Identificación laboral (G física), conservando la clasificación laboral y los nombres literales de fuente/documento. No bloquea por sí sola H:O: evaluar cada documento según su identidad, aplicabilidad, vínculos, vigencias y condiciones propias. El DNI debe pertenecer al trabajador, no al tomador/empleador/tercero. CUIT/CUIL puede corroborarlo conforme DEC-006; DNI explícito discordante con DNI central del CUIT permanece bloqueante. No aceptar diferencias totales de identidad, identificadores contradictorios, lectura dudosa o asociaciones insuficientes. No unir pólizas ni copiar resultados por DNI solamente. Conservar la observación y evidencia también en el registro técnico; no repetir la observación nominal en otras columnas ni ocultar incumplimientos independientes. No corregir nombres ni DNI de la fuente.
