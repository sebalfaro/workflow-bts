# Aislamiento y modelos — piloto instrumentado

## Garantía y límites

REQ-018/019 se implementan como cierre y apertura de contexto operativo, no como borrado de memoria del modelo. ContextRuntime exige checkpoint local fsync antes de cerrar trabajador o cambiar proveedor; invalida asociaciones, conserva extracciones neutrales por hash de fuente y versión de extracción, y exige una autorización contextual nueva para reutilizarlas. Comprueba run/proveedor/contexto/hash de entrada y referencias documentales de respuesta. El journal encadena hashes; una recuperación incompleta se detiene para reconciliación, no descarta estado. No demuestra identidad estable de fuente, verdad de extracción, completitud, permisos, almacén compartido, concurrencia ni publicación.

La caché debe contener hechos/literales de extracción, no dictámenes previos ni instrucciones operativas. Un grant lo emite ORQ sólo después de corroborar vínculo y alcance; el auxiliar no descubre ni prueba ese vínculo. No agregar historia de otros trabajadores ni resultados esperados al input de evaluación. Mantener los originales y el journal fuera del repositorio público.

## Ejecución aislada y prueba

tools/benchmark_models.py prepara contextos sintéticos y usa una invocación Codex CLI nueva por caso, sin resume/fork, memoria/herramientas generales deshabilitadas y directorio de trabajo temporal. No hereda el historial del caso anterior en el payload. --ephemeral no prueba eliminación de datos en el servicio. Los logs del runner demuestran el payload y opciones solicitadas; no revelan todo el input interno del proveedor. Cualquier herramienta observada invalida la prueba; ausencia de marcador en output sola no basta para demostrar aislamiento.

tools/check_context_isolation.py ejecuta una prueba local con journal y cinco checkpoints: dos trabajadores del mismo proveedor, cambio de proveedor, regreso al anterior y reinicio local. Registrar resultados como LOCAL_BOUNDARY_CONFIRMED; no como prueba de memoria del modelo.

Tests locales ejercitan cambio de trabajador/proveedor, DNI repetido sin transferencia de documentos, documento colectivo con grant explícito, respuesta cruzada, mutación de payload, fallo de checkpoint, reinicio tras checkpoint, journal manipulado y contexto sin cerrar. Tests con mocks son pruebas del control de errores, no llamadas reales a modelos. El corpus textual sintético cubre doce casos de inclusión/ausencia/insuficiencia/identidad y pago independiente; no es OCR ni benchmark de documentos visuales.

## Modelos candidatos y escalamiento

model_routing.py propone Luna5.6 para clasificación/extracción sencilla, Sol6.1 para validación y complejidad, Astra6 para escalamiento residual. Terra5.6 y Sol5.6 compiten en benchmark antes de incorporarse a la ruta; Mini5.4 y Mini4.1 se comparan en tareas acotadas. Una versión anterior no es automáticamente más económica. Todas las rutas empiezan sin calificación: EVALUATE_ONLY. qualified_models requiere evidencia de evaluación revisada por tarea/modalidad, registrada por ORQ; no aceptarlo de una respuesta de modelo. EXECUTE tampoco autoriza escribir resultados. Hashes y publicación son tareas de adaptador determinista.

Señales: cobertura incompleta, tabla desordenada, región ilegible, conflicto de identificadores, desacuerdo de extracción o alcance complejo. Tras rutas agotadas: REVIEW_REQUIRED y DEC-019; no convertir incertidumbre en ausencia. Registrar modelo solicitado, modelo reportado por proveedor cuando esté disponible, modalidad, razonamiento, input hash, intentos, señales, tiempo, tokens y costo por caso correcto incluyendo escalamiento. No identificar el modelo real a partir de su propia respuesta o de un alias solicitado.

## Activación incremental

1. Verificar controles locales y congelar corpus/oráculo sintéticos. Oráculo ausente del input del modelo.
2. Resolver capacidad real CLI/cuenta; ejecutar los mismos casos, repeticiones y controles de orden A/B y proveedor. Un fallo de backend no recibe score.
3. Ampliar con tablas e imágenes sintéticas con verdad corroborada; después comparar contra documentos privados autorizados y revisión original. Mantener datos privados fuera de GitHub.
4. Medir costo por resolución correcta, falsos positivos/ausencias y escalamiento. Cero contaminación o resultado crítico incorrecto observado es requisito de admisión del lote, no garantía universal. Modelos no aptos se descartan para la tarea.
5. Integrar ORQ/BUS/EXT/VAL en modo sombra sin writes; comparar y confirmar antes de habilitar publicación normal. El runner sintético no está conectado al piloto Sheets. Windows permanece en Fase8 Staging; segundo actor/concurrencia no se reanudan por esta implementación.

Fuentes de capacidades: [CLI](https://developers.openai.com/codex/cli/reference), [orquestación](https://developers.openai.com/api/docs/guides/agents/orchestration). Tarifas orientativas consultadas2026-10-13 en las páginas oficiales de modelos; las cuotas de Codex no se deducen de precios API.
