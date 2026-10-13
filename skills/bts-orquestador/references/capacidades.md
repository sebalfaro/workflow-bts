# Configuración, transporte y dependencias

Las observaciones Fase 4 son históricas: raíz 404 (ID/acceso no distinguidos); metadata del destino observada; maestro observado como XLSX, contenido/Hoja 1/A–F sin verificar; creación, ubicación, writes y readback no comprobados. No se efectuaron nuevas llamadas Google en Fase 5. Disponibilidad de una herramienta no demuestra permisos ni operación. No crear archivos externos sólo para probar capacidades.

## Transporte de fuente

Leer metadata MIME actual antes de elegir adaptador. Sheets nativo: rango A:F de pestaña confirmada y valores/tipos/fórmulas disponibles. XLSX: descargar bytes, comprobar hash, abrir en modo lectura con lector disponible, conservar fórmula y valor cacheado por separado. Sin caché necesaria no calcular por suposición. No convertir ni modificar el maestro. Otro MIME o lector faltante: SOURCE_UNREADABLE/D-08. Constatar encabezados y límites, no imponer fila inicial fija ni terminar al primer hueco.

Datos locales: aceptar snapshot con origen, fecha, hash y límite de actualidad; sólo en alcance autorizado. La carpeta de Downloads observada no reemplaza raíz Drive ni acredita inventario actual. Reconciliar IDs/hashes antes de publicación actual. No localizar archivos fuera del proveedor para completar un caso salvo autorización específica y vínculo demostrado.

## Dependencias vigentes

| ID | Alcance | Resolución futura / salida definida |
|---|---|---|
| D-01 | Lectura/OCR PDF e imágenes | Lector/motor disponible y verificado; falta motor ERROR_TECNICO, lectura insuficiente REVISION_USUARIO |
| D-02 | Identidad estable | Registro por ocurrencia y reconciliación demostrable; ROW_ID_AMBIGUOUS sin copiar resultados |
| D-03 | Vínculos/alcance | Hechos/aristas y revisión documental; LINK_UNPROVEN, no inferir cobertura |
| D-04 | Búsqueda/unicidad | Inventario raíz y clasificación completos; ambiguo revisión, parcial pendiente |
| D-05 | Layout | Adaptador G:O adoptado localmente; migración/consumidores sin verificar, SCHEMA_UNKNOWN |
| D-06 | Persistencia/concurrencia | Journal compartido, recibos y recuperación verificados; PERSISTENCE_FAILED/WRITE_UNCERTAIN |
| D-07 | Acceso raíz | Resolver ID/acceso dentro del ámbito autorizado; ROOT_UNREADABLE no ausencia |
| D-08 | Maestro/destinos | MIME actual, transporte XLSX/nativo, permisos, creación/ubicación/write/readback; CAPABILITY_MISSING |
| D-09 | Presentación | Mostrar revisiones/obsolescencia en seguimiento/reporte enlazados; no afirmar actualidad si no puede representarse |
| D-10 | Reintentos | Tres intentos totales/corrida para transitorios, Retry-After; agotado ERROR_TECNICO |
| D-11 | Salida central | ID/carpeta/pestaña sin aportar, configurar en evento.json; CENTRAL_DESTINATION_UNRESOLVED |
| D-12 | Índice compartido | Carpeta técnica/Sheet control sin aportar; SHARED_STORE_UNRESOLVED; trabajo local preparable |
| D-13 | Equipo/publicación | Operador y responsable por corrida, entrega de turno/escritor único comprobable; PUBLISHER_UNRESOLVED/CONCURRENT_EDIT |
| D-14 | Cambios incrementales API | Optimización opcional no comprobada; fallback a inventario completo; no bloquear por falta de API changes si listado completo funciona |
| D-15 | Empaquetado del equipo | Mismo manifiesto/config/ruleset en cada máquina; PACKAGE_VERSION_MISMATCH; distribución/instalación futura |

El runtime no contiene adaptadores Google/OCR operativos. Las skills especifican cómo usar herramientas disponibles y cómo devolver dependencia cuando faltan. JSON/SHA/contratos locales no acreditan integración. Sólo ORQ puede mutar destinos bajo autorización de ejecución futura; BUS/EXT/VAL retornan datos/planes.

Errores 403/404: acceso/ID pendiente, no ausencia. 429/5xx/timeout: reintento acotado, pero una mutación incierta exige readback primero. Una revisión de negocio no se resuelve reintentando. La frecuencia dos veces al día no crea una automatización ni define horarios.
