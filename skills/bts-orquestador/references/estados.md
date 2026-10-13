# Estados, revalidación y escrituras — procedimientos candidatos PT-008 a PT-010

## Tres ejes independientes

| Eje | Estados adoptados técnicamente | Significado |
|---|---|---|
| Aplicabilidad | APLICABLE, NO_APLICABLE, INDETERMINADA | Vacío sólo para NO_APLICABLE corroborada |
| Resultado documental | CUMPLE, NO_CUMPLE, AUSENTE, INFORMATIVO, REVISION_USUARIO, SIN_EVALUAR | No equivale a ingreso ni a éxito técnico |
| Procesamiento | PENDIENTE, EN_CURSO, EVALUADO, PREPARADO, ESCRITURA_INCIERTA, CONFIRMADO, ERROR_TECNICO, OBSOLETO | Progreso de trabajo y persistencia |

Registro por verificación y versión; fila agregada mantiene todos los ejes, sin único «aprobado». Un resultado EVALUADO permite trabajo independiente; CONFIRMADO exige persistencia durable y, si debe publicarse, lectura posterior. En esta auditoría no se marcan escrituras CONFIRMADAS.

PENDIENTE→EN_CURSO al tomar trabajo; EN_CURSO→EVALUADO con resultado/evidencia; →ERROR_TECNICO con fallo; ERROR_TECNICO→PENDIENTE para reintento autorizado futuro; EVALUADO→PREPARADO tras journal y precondiciones; PREPARADO→CONFIRMADO tras escritura/leído coincidente; →ESCRITURA_INCIERTA con timeout; cambios de dependencia→OBSOLETO→PENDIENTE. Revisión usuario es resultado final documentado, no error técnico reintentable. Respuesta humana se registra literal, alcance y versión; sólo reevalúa afectado, no autoriza ignorar otras reglas.

Fila terminada: todas verificaciones tienen aplicabilidad/resultado/evidencia documentados y no hay error técnico, escritura incierta, evaluación pendiente ni resultado obsoleto. Puede terminar con NO_CUMPLE, AUSENTE o REVISION_USUARIO (DEC-008.d). Proveedor/corrida termina cuando todas sus filas/operaciones cumplen ese criterio; la presentación conserva revisiones. No exigir todas celdas no vacías ni todas Ok.

## Detección y revalidación

Snapshot por A–F, inventario de archivos/ubicaciones/hashes, reglas, config y esquema. Hora de modificación dispara comprobación, no sustituye hash ni demuestra sustitución. Sheet nativo se compara por snapshot de celdas/tipos y estructura; XLSX por bytes/hash y contenido extraído. Búsquedas negativas dependen del inventario completo: un PDF nuevo obliga a reconsiderarlas. Hash cambiado invalida extracción y todo resultado dependiente antes de reutilizar.

| Cambio | Invalidación mínima diseñada |
|---|---|
| Identidad A/B/C | asociaciones de persona y todas verificaciones que las consumen; G incluido |
| Proveedor D | carpeta/Sheet/contexto y asociaciones/resultados dependientes |
| Función E o accesos F | contexto y alcance documental que los use; preservar resto si dependencia explícita no los consume; no decidir ingreso |
| Constancia fiscal identidad/CUIT | H y vínculo identidad de I |
| Pago/período/tributo | I |
| Monto AP | J.montos y evidencias correspondientes |
| Cláusulas AP/ART | J.clausulas o M respectivamente |
| Fechas AP | K y vínculos/reemplazos que consuman fecha; sin veto temporal a J por sí solo |
| Póliza/aseguradora/nómina/alcance/reemplazo | todas verificaciones que consuman conjunto o versión reemplazada; K y G si afectadas |
| Alta / SVO | L / N originales |
| Inventario/carpeta o archivo nuevo/retirado | selecciones/búsquedas dependientes incluidas ausencias/G |
| Reglas/config evento | consumidores del campo/regla cambiado; no toda fila si independencia demostrada |
| Layout/movimiento/edición destino | mapping y operaciones de escritura; resultado documental sólo si insumo cambió |

Dependencias se guardan por resultado, no sólo por tipo de PDF. Con cambio de bytes sin poder establecer campos afectados, reextraer y revalidar todos los consumidores de ese documento. Mientras obsoleto, el histórico se conserva con vigencia revocada en seguimiento; no se cuenta como comprobado actual. Si falta soporte para advertir obsolescencia en presentación, bloquear publicación de conclusión dependiente y registrar D-09.

## Reutilización y recuperación

Sheet se identifica por ID persistente + carpeta destino + proveedor literal + esquema, no sólo título. Cero coincidencias: plan de crear; una verificada: reutilizar; varias: revisión sin elegir más reciente. Un archivo nuevo se registra como operación con clave idempotente evento/proveedor/operación. Ante respuesta incierta de creación, recuperar por ID/journal/metadata/correspondencia; no crear otro por timeout. Si no hay medio de identificar inequívocamente creación previa, dependencia técnica; detener sólo esa mutación.

Journal durable por corrida y snapshots JSON versionados compartidos en Drive más registro lateral de destino (D-06/D-12), evitando datos operativos mezclados con A–O. Persistir eventos append-only: intent, input hashes, resultado/evidencia, preimage destino, payload esperado/hash, request/operation_id, respuesta, readback, commit, reintentos y revisión. Snapshot compacto se deriva del journal; guardado atómico y checksum. No se construyó ni operó ese almacén en Fase 4.

Al reanudar: verificar configuración/manifiestos y journal; reconciliar filas/Sheet; releer operaciones inciertas antes de reenviar; detectar cambios e invalidar dependencias; conservar independientes confirmados; retomar pendientes técnicos según DEC-008.e. No resolver revisiones del usuario autónomamente. Journal corrupto o checkpoint sin evidencia: recuperar último registro íntegro y dejar lo no demostrado pendiente. Interrupción tras evaluación, antes de write: revalidar snapshots y seguir. Tras write, antes de commit: readback y comparación antes de decidir repetir.

PT-010 adopta hasta 3 intentos totales por operación transitoria por corrida, con dos esperas entre intentos (1,2 s) más jitter y respeto a cuota/Retry-After; son parámetros técnicos revisables, no decisión humana. 403/404/acceso ausente no se convierten en documento ausente; dependen de acceso/ID. 429/5xx/timeouts permiten reintento acotado. Fallo permanente o agotamiento conserva ERROR_TECNICO pendiente sin bucle infinito; reanudación posterior tras acceso/cambio o nueva corrida autorizada. No reinterpretar fallo como revisión de negocio sólo para dar corrida por terminada.

## Verificación futura de escrituras

1. Resolver fila por ID/contexto, Sheet/pestaña numérica y esquema; releer A–F y celdas de destino, comparar con preimage/hash. Registrar conflicto si cambió.
2. Persistir intención, payload y resultados con claves lógicas/adaptador. Escribir sólo columnas afectadas, conservar A–F e independientes; no anexar fila repetida si ya existe su ocurrencia. No aplicable vacía intencionalmente se distingue de omisión del payload.
3. Escritura tipada adoptada técnicamente (`stringValue`, sin interpretación de fórmulas) para identificadores/texto. Rangos explícitos; no fórmulas ni conversiones automáticas introducidas por entrada de PDF. API/adaptador y permisos pendientes de prueba.
4. Releer celdas realmente guardadas, valores/tipos y fila/contexto, no basarse sólo en respuesta del write. Comparar payload, identidad, versión de esquema y ubicación; comprobar carpeta/nombre/ID si creación o ubicación. Sólo igualdad confirma commit y progreso.
5. Timeout: ESCRITURA_INCIERTA; readback primero. Si coincide, commit sin repetir; si conserva preimage y contexto, reintento; si parcial/diferente, conflicto y reconciliación sin sobrescritura ciega. Si readback falla, pendiente técnico.

No presumir transacción conjunta Drive+Sheets+journal. Bloqueo cooperativo por Sheet/fila y relectura reducen carreras pero no excluyen editor externo entre verificación y escritura. D-06 exige mecanismo de exclusión fiable o entorno futuro de escritor único/control de edición; sin ello registrar riesgo y suspender mutación sobre fila concurrente. No atribuir writeControl/CAS disponible a Sheets sin prueba. Estos pasos son instrucciones candidatas de ejecución futura; cero escrituras externas realizadas.

## Publicación por destino y continuación compartida

Mantener estados separados para cálculo, Sheet del proveedor, salida central e índice/journal compartido. No hay CONFIRMADO global mientras falte alguno requerido. Si proveedor fue leído y coincide pero central falla: PROVEEDOR_CONFIRMADO_CENTRAL_PENDIENTE; retomar central con la misma versión, sin revalidar documentos salvo cambio de dependencias. Una revisión humana documentada permite terminar cálculo, pero no oculta publicación pendiente.

Al cambiar operador, cargar configuración y último manifiesto compartido confirmado, verificar hashes y recibos. Un checkpoint sólo local sirve para recuperación del mismo operador; no es progreso compartido confirmado. Publicación y entregas siguen [publicacion.md](publicacion.md). No hacer polling ni programar ejecuciones automáticamente: dos corridas manuales por día, horarios todavía sin definir.

Retiro de fila/documento se registra y vuelve obsoleto el resultado dependiente. No borrar filas publicadas automáticamente: conservar historial y estado retirado fuera de A–O; si no puede mostrarse obsolescencia, bloquear publicación como actual y registrar D-09. Una nueva fila debe reevaluar el índice sin correspondencia.

## Regla general de observación nominal — DEC-018

Regla general DEC-018: una diferencia parcial del nombre, con DNI del trabajador corroborado y coincidente con la fila fuente, se registra únicamente como observación nominal en Identificación laboral (G física), conservando la clasificación laboral y los nombres literales de fuente/documento. No bloquea por sí sola H:O: evaluar cada documento según su identidad, aplicabilidad, vínculos, vigencias y condiciones propias. El DNI debe pertenecer al trabajador, no al tomador/empleador/tercero. CUIT/CUIL puede corroborarlo conforme DEC-006; DNI explícito discordante con DNI central del CUIT permanece bloqueante. No aceptar diferencias totales de identidad, identificadores contradictorios, lectura dudosa o asociaciones insuficientes. No unir pólizas ni copiar resultados por DNI solamente. Conservar la observación y evidencia también en el registro técnico; no repetir la observación nominal en otras columnas ni ocultar incumplimientos independientes. No corregir nombres ni DNI de la fuente.
