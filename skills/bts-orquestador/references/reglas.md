# Reglas ejecutables por el agente — versión candidata 5.2

DEC confirmadas prevalecen; para originales no cambiados, detalle de VAL antes del resumen WF (DEC-011). Las claves lógicas preservan el REQ aunque cambie su letra física. PT-002 se adopta técnicamente como layout G:O para candidatas; no se aplicó migración externa. DEC-014 amplía búsqueda a todo el proveedor.

| Original / clave | Propuesta física / encabezado | REQ específico | Regla vigente / DEC |
|---|---|---|---|
| G / regimen | G / Identificación laboral | 055–057 | DEC-005; nunca Ok |
| H / constancia | H / Constancia fiscal | 058 | DEC-001,006 |
| I / pago | I / Pago fiscal | 059 | DEC-009,006 |
| J / J.montos | J / AP montos | 060–061 | subdivisión REQ-061.montos → REQ-061; DEC-012,010 |
| J / J.clausulas | K / AP cláusulas | 043–054,060–062 | subdivisión REQ-061.clausulas → REQ-061; DEC-002,010 |
| K / vigencia_ap | L / Vigencias AP | 063 | DEC-003; nunca Ok |
| L / alta | M / Alta temprana | 064 | original no cambiado |
| M / art | N / ART | 065–067 | DEC-002,005,010; vigencia original |
| N / svo | O / SVO | 068 | original no cambiado |

Las referencias posteriores siempre incluyen `original K / física L`, etc. REQ-009/017/021/041/042 pasan por adaptador de layout sin renumerarse. El seguimiento/evidencia se propone fuera de A–O. Hojas antiguas G:N necesitan identificación de encabezados y versión; no insertar una columna a ciegas. Antes de futura migración: snapshot íntegro, mapping de celdas/fórmulas/consumidores y registro reversible. Un J antiguo compuesto no prueba sus dos nuevas salidas: revalidar J.montos/J.clausulas y conservar histórico. Esquema desconocido o consumidores no identificados: dependencia D-05, sin escribir.

## Rutas de evaluación comunes

Evaluar aplicabilidad, búsqueda/lectura, identidad/vínculo, condición específica y presentación. Dentro de cada verificación, conservar todas las causas; ningún fallo se oculta detrás de un Ok. Candidato válido no anulado/reemplazado para el alcance puede satisfacer la regla entre otros distintos (DEC-005). No sumar alternativas de póliza incompatibles.

| Situación | Resultado documental / celda | Procesamiento |
|---|---|---|
| No aplicable expresamente corroborado | vacío real; estado NO_APLICABLE y motivo fuera de resultados | final documentado |
| Búsqueda completa sin documento requerido | Archivo no encontrado | final documentado |
| PDF localizado insuficiente/ilegible con lectura realizada | Revisar documento: [detalle] | revisión usuario documentada |
| Acceso/listado/descarga/OCR pendientes | ninguna nueva conclusión dependiente; propuesta aviso técnico fuera de celda, histórico marcado desactualizado | pendiente técnico |
| Identidad contradictoria no aclarada | Revisar identidad: [detalle], sin Ok | revisión usuario |
| Resultado favorable según regla | Ok salvo G/vigencias AP; observación invalidez cuando corresponda | final documentado |
| Condición conocida no satisfecha | detalle exacto de incumplimiento, sin Ok | final documentado |

No aplicabilidad no surge de ausencia. Sólo AP corroborado: rama H/I/AP aplicable y rama laboral no aplicable; sólo ART corroborado: rama L/M/N aplicable y rama fiscal/AP no aplicable. Ambas: ambas ramas; ninguna o cobertura sin poder determinar: evaluar búsquedas independientes, conservar aplicabilidad INDETERMINADA hasta evidencia suficiente; no vaciar todas las celdas como no aplicables. La vigencia vencida no borra la detección documental de cobertura.

## Tabla G

| Evidencia vinculada al trabajador | Salida |
|---|---|
| AP solamente | Monotributista o Autónomo |
| ART solamente | Relación de Dependencia |
| AP y ART | propuesta: Monotributista o Autónomo; Relación de Dependencia (AP y ART); evaluar por separado |
| Ninguna tras búsquedas completas | Cobertura no determinada (exacto DEC-005) |
| Documentos sin identidad corroborable | revisión de identidad/documento según causa; no atribuir cobertura por carpeta sola |
| Búsqueda técnica incompleta | pendiente técnico, no afirmar ninguna |

## Tabla H (original H)

Constancia de opción o inscripción con identidad DEC-006. Sólo comparar vencimiento >= 29/10/2026; no exigir inicio 07/10 ni fin 30/10. Vencimiento anterior: intervalo completo literal sin Ok. Fecha no determinable: extraer todo lo posterior a «Vigencia de la presente constancia», manteniendo literal y revisión sin inventar fecha. Rótulo/campo ilegible/ausente: Revisar documento: [detalle]. Identidad contradictoria se informa aunque haya fecha favorable. Evidencia REQ-058/DEC-001: identidad, tipo de constancia, rótulo/intervalo y comparación del vencimiento.

## Tabla I (original I)

| Hechos corroborados, identidad válida | Salida |
|---|---|
| Al menos un pago incluso parcial imputado a monotributo/autónomo de enero–octubre/2026 | Ok |
| Sólo períodos fuera de enero–octubre/2026 | propuesta: Pago fuera del período requerido: [períodos] |
| Comprobante/VEP generado sin pago demostrado | Revisar documento: pago no demostrado |
| Pago visible sin período o tributo identificable | Revisar documento: período/tributo no visible |

Fecha de pago no agrega corte. No exigir octubre, todos los meses, saldo cero, obligación mensual cancelada ni prima AP. H/I pueden vincular pago y constancia por mismo CUIT para obtener nombre y cotejar DNI central (DEC-006.a); si esa constancia cambia, revalidar identidad de I. REQ-059/DEC-009.

## Tabla J.montos (original J → física J)

| Hechos aplicables a trabajador y conjunto compatible | Resultado / salida |
|---|---|
| Muerte >= ARS80M y gastos >= ARS8M | Ok |
| Lo anterior, sin cifra invalidez | propuesta: Ok — sin cifra de invalidez informada (observación obligatoria no bloqueante) |
| Muerte inferior/ausente o sólo invalidez | detalle montos/cobertura faltante sin Ok |
| Gastos inferiores | detalle importe y mínimo sin Ok |
| Moneda explícita distinta ARS | propuesta: Revisar moneda: [moneda e importes]; revisión usuario, sin conversión |
| Suma global sin aplicación por trabajador clara | propuesta: Revisar alcance del monto: [detalle]; sin dividir por cantidad |
| Cifra/formato no determinable | Revisar documento: monto no determinable |

Gastos: límite conjunto o suma de médicos + farmacia separados; un límite aplicable médicos o farmacia >=8M satisface umbral confirmado. No duplicar un mismo límite conjunto al sumar ni agregar sepelio, renta, asistencia externa o límites incompatibles. $ sin otra moneda se normaliza ARS por DEC-012, conservando que es interpretación, no literal del emisor. Decimales/separadores inequívocos se normalizan; ambiguos se revisan. Ignorar franquicia en evaluación y salida. No usar invalidez en reemplazo de muerte ni imponer mínimo de invalidez. Las fechas AP no vetan montos; sí ayudan a identificar alcance/reemplazos.

## Tabla J.clausulas (original J → física K) y subregla de M

Ocho entidades de REQ-044–051: configurar localmente nombre e identificador exigido para cada REQ. La distribución pública no incluye identidades reales. Sin configuración completa, registrar CONFIG_CONFLICT y no validar cláusulas.

| Evidencia vinculada a obligación y póliza/trabajador | Resultado |
|---|---|
| Ocho entidades con identificadores/nombres admitidos | Ok para AP; en ART sujeto también a identidad/vigencia |
| Faltantes o no coincidencias determinadas | falta o no coincide cláusula de no repetición [detalle] (DEC-010; sin Ok ni Aprobado parcial) |
| CUIT incidental fuera de cláusula | no demuestra obligación; faltante si lectura completa lo determina |
| CUIT correcto, nombre truncado | revisión usuario señalada en celda; propuesta Revisar cláusula: nombre truncado [entidad] |
| Identificadores contradictorios | revisión, no elegir por prioridad |

Acepta separadas o renuncia común seguida de lista de ocho; orden de entidades y nombres reordenados admitidos; personas físicas admiten DNI y nombre completo (DNI y nombre completo configurados localmente). Omisión nominal admitida para trabajador no se traslada a entidades. Formas Experta y MeCubro confirmadas: certificado que declara no iniciar acciones contra lista vinculada a póliza/persona, y listado bajo título CLÁUSULAS DE NO REPETICIÓN en constancia vinculada, respectivamente. No validar por marca sola ni extender aceptación a cualquier listado de CUIT. No exigir modelo literal adicional ni evaluar excepciones culpa/dolo/seguridad como requisito nuevo. Documentos completos pero forma no resoluble: revisión. Evidencia por entidad conserva obligación/título, nombre, identificador y enlace al ámbito.

## Tabla K (original K → física L)

Mostrar todos los intervalos AP de documentos aplicables, separados por punto y coma, con horas y alcance cuando figuren. Conservar intervalos por trabajador frente a período general de póliza; etiquetar ambos para evitar atribución. No fusionar continuidad ni omitir huecos, fechas vencidas o intervalos de otros aspectos todavía aplicables. Anulado/reemplazado no sirve como vigente para alcance sustituido; queda en historial de evidencia con motivo. Fecha insuficiente/ilegible: literal disponible y Revisar documento: [detalle], nunca Ok. Fechas sólo informativas (DEC-003), no decisión de ingreso.

## Tabla L (original L → física M)

Identidad corroborada e inicio <=07/10/2026 y cese >=30/10/2026: Ok. Cese vacío está expresamente permitido; conservar evidencia de campo vacío y exigir inicio suficiente. Fecha inicio ausente/ambigua: revisión. Intervalo fuera del evento: inconsistencia y fechas sin Ok. No aplicar excepción cese vacío a ART/SVO. REQ-064.

## Tabla M (original M → física N)

Buscar en todo el inventario del proveedor, usando ART como ubicación orientativa y palabra interna ART como indicio que debe corresponder al tipo documental; comprobar tipo documental, identidad, vigencia que comprenda 07/10–30/10/2026 y ocho cláusulas según DEC-002. Todo cumple: Ok. Identidad/vigencia fallan: detalle sin Ok; si además faltan cláusulas, conservar detalle de ambas causas. Identidad/vigencia cumplen pero faltantes/no coincidencias: texto exacto DEC-010 ya indicado. No imponer montos AP. Falta de documento, revisión y errores por rutas comunes. Complementación compatible permitida DEC-005; no inventar cobertura continua entre huecos.

## Tabla N (original N → física O)

SVO con identidad y vigencia que cubra 07/10–30/10/2026: Ok. Fuera de fechas/discordancia: detalle sin Ok. Ausencia/insuficiencia: rutas comunes. No copiar resultado de ART ni exigir cláusulas/montos AP no previstos en REQ-068. Fechas/horas incompatibles con cobertura exigida no se redondean para forzar cumplimiento; si el texto no permite resolver alcance del día, revisión documental.

Las plantillas marcadas «propuesta» se adoptan técnicamente como PT-003 en esta candidata; no son textos literales atribuidos al usuario. Los textos confirmados y restricciones nunca Ok se conservan.

## Alcance de búsqueda y precedencia de estados — DEC-014/015

La ausencia de AP (Accidentes Personales) o ART ya no basta para Archivo no encontrado: revisar todos los archivos/secciones del proveedor, incluso imágenes o subcarpetas repetidas. La categoría requiere contenido; nombre/ruta no prueban tipo ni identidad. Documento válido fuera de carpeta se acepta, dejando anomalía de ubicación. No sumar evidencias de proveedores distintos por hash o DNI.

Para declarar “sólo AP” o “sólo ART” y vaciar una rama como NO_APLICABLE, debe haberse completado la búsqueda/clasificación de la otra cobertura sin candidatos pendientes. Con candidatos ilegibles o lectura pendiente, conservar aplicabilidad INDETERMINADA en lo afectado. Una asociación por nombre completo sin ID es CANDIDATA_NOMBRE, requiere corroboración; nunca convierte sola un predicado en verdadero.

Dentro de cada conjunto conservar todos los fallos. Un testigo favorable sólo es utilizable tras comprobar sus vínculos y la ausencia de anulación/reemplazo aplicable pendiente de resolver. Un archivo no leído capaz de alterar alcance deja dependientes pendientes, sin esconderlo tras otro favorable. Otros conjuntos completos distintos no bloquean por mera diferencia.

Resultados independientes pueden evaluarse tras terminar el mapeo del alcance disponible y registrar explícitamente sus huecos. SIN_EVALUAR/error técnico usa output_literal=null y no autoriza vaciar celda; NO_APLICABLE corroborado usa output_literal="" y una operación explícita de vaciado. En K lógica, intervalos son informativos incluso vencidos; historial de documentos sustituidos permanece en evidencia.

## Regla general de observación nominal — DEC-018

Regla general DEC-018: una diferencia parcial del nombre, con DNI del trabajador corroborado y coincidente con la fila fuente, se registra únicamente como observación nominal en Identificación laboral (G física), conservando la clasificación laboral y los nombres literales de fuente/documento. No bloquea por sí sola H:O: evaluar cada documento según su identidad, aplicabilidad, vínculos, vigencias y condiciones propias. El DNI debe pertenecer al trabajador, no al tomador/empleador/tercero. CUIT/CUIL puede corroborarlo conforme DEC-006; DNI explícito discordante con DNI central del CUIT permanece bloqueante. No aceptar diferencias totales de identidad, identificadores contradictorios, lectura dudosa o asociaciones insuficientes. No unir pólizas ni copiar resultados por DNI solamente. Conservar la observación y evidencia también en el registro técnico; no repetir la observación nominal en otras columnas ni ocultar incumplimientos independientes. No corregir nombres ni DNI de la fuente.

## DEC-019 — lectura insuficiente

Aplicar [lectura-insuficiente.md](lectura-insuficiente.md). Una búsqueda OCR negativa sospechosa no autoriza ausencia ni Archivo no encontrado. P central Revisar identifica documento/localizador y controles afectados; no sustituye G:O.
