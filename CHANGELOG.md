## 0.7.2-rc.1 — 2026-10-13

- Añade aislamiento operativo local y checkpoint antes de cerrar contextos, con rechazo de referencias cruzadas y grants explícitos para caché neutral.
- Añade selección candidata y escalamiento acotado de modelos; no habilita writes ni promoción automática.
- Añade benchmark textual sintético de doce casos y seis modelos candidatos, con procesos nuevos, trazabilidad y guardas de fallo.
- Pruebas reales de modelos bloqueadas durante inicialización del CLI; sin resultados puntuados, sin benchmark OCR y sin integración nueva del piloto.
- Mantiene contrato bts-5.2, DEC-018/019, F7 parcial y Windows pendiente en F8.

# Changelog

## 0.7.1-rc.1 — 2026-10-13

- DEC-019, recuperación de lectura insuficiente y Revisar P central.
- Contrato bts-5.2 con referencias estructuradas; schema bts-resultados-3.
- Helper puro y regresiones sintéticas de OCR negativo/inconcluso, referencias y resolución.
- Windows diferido a Fase8 Staging; consumidores confirmados por usuario.
- Actualización de contrato requiere componentes/configuración/hashes coherentes; no consumo silencioso como5.1.

## 0.7.0-rc.1 — 2026-10-13

- Primera distribución pública de ORQ/BUS/EXT/VAL y contrato bts-5.1.
- Reglas DEC-001 a DEC-018, con observación nominal no bloqueante por DNI corroborado.
- Configuración de recursos y entidades reales excluida; plantilla requiere configuración local.
- Auxiliares deterministas, pruebas sintéticas y manifiesto SHA-256.
- Fase 7 PARCIAL, sin aprobación para producción ni certificación Windows.
