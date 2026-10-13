# Auxiliares deterministas

[bts_core.py](../scripts/bts_core.py) usa Python 3.10+ y biblioteca estándar. Importar como módulo desde el paquete; no contiene runner de workflow, adaptadores Google ni OCR. `python3 bts_core.py --describe` imprime sólo interfaz. Fase 5 verifica AST/compilación y este modo descriptivo, sin ejecutar predicados sobre escenarios TC. Las pruebas sintéticas públicas están en tests/ del repositorio; las auditorías privadas no se distribuyen. Requiere Python 3.10+; en esta fase se usó Python 3.12.14 aislado, sin actualizar el sistema.

| Función | Uso | Condición previa / límite |
|---|---|---|
| canonical_hash / file_hash | Hash estable de snapshot JSON / bytes | No demuestra identidad/autenticidad; JSON rechaza float, usar strings para montos/IDs |
| format_name / provider_candidate | Formato autorizado y candidato de proveedor | Probar raíz, número corroborado y unicidad aparte; conservar D literal |
| identifier / central_dni | Normalizar identificador tipado, extraer central CUIT | No rellenar/truncar DNI ni elegir entre contradicciones; OTRO/PASAPORTE literal |
| name_candidate | Tokens de nombre en distinto orden | Sólo propone coincidencia; comparar roles nominales, confirmar ID. Omisión no aplica a entidades de cláusulas |
| expiry_at_least | Predicado de vencimiento H | Recibir ISO corroborado y mínimo evento.json; sin argumento inicio |
| period_in_range | Período I inclusive | Pago/tributo/identidad demostrados fuera del helper; sin fecha de pago ni saldo |
| interval_covers | Intervalo L/M/N | Sólo fechas diarias corroboradas; horas/alcance ambiguos revisión; fin vacío sólo L con evidencia |
| amount_at_least | Umbral decimal exacto | Normalizar separadores con evidencia, comprobar moneda ARS y alcance individual previamente |
| compatible_expense_total | Límite conjunto o médicos+farmacia separados | Pasar un único conjunto compatible. No duplicar joint con sus sublímites; alternativas deben resolverse antes. Sin franquicia/invalidez/sepelio |
| affected_results | Cierre transitivo de dependencias | Grafo debe incluir cambios de inventario, asociaciones, configuración y reglas; no sólo PDF. IDs no vacíos, como list/tuple/set; grafo dict. Una cadena escalar se rechaza como DEPENDENCY_IDS_TYPE |
| compare_readback | Igualdad de snapshot tipado e identidad | `observed` debe provenir de lectura posterior real, no eco del payload; comparación de cells por A1, sin depender del orden recibido (A1 único); conserva types y valores exactos. Igualdad no confirma por sí sola commit compartido |

Cada llamada puede producir InputReview con código. El llamador captura el código y registra revisión de documento/identidad o dependencia de configuración/contrato según causa, sin convertir excepción a False, ausencia o Ok. OSError en file_hash es error técnico. Los booleanos sólo son predicados; VAL debe aportar evidencias de todas condiciones antes de construir un resultado. Nunca utilizar helpers para seleccionar una póliza, inferir vínculo, confirmar cláusula o resolver nombre truncado.

Reglas/config como argumentos: `expiry_at_least(fin, config['h_vencimiento_minimo'])`; I consume `i_periodos`; L/M/N consumen `periodo_evento`; monto consume `str(config['ap']['minimo_muerte_ARS'])` o gasto correspondiente. Valores de hechos son strings, no floats. La configuración no se modifica desde este módulo.

[reading_review.py](../scripts/reading_review.py) separa INCLUDED, VALUE_ABSENT, FILE_ABSENT, READING_INCONCLUSIVE y TECHNICAL_PENDING sobre hechos corroborados y renderiza P por contexto. No realiza OCR, búsqueda ni corroboración; usar [lectura-insuficiente](lectura-insuficiente.md).
