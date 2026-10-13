# Workflow BTS 2026

Primera versión pública **0.7.1-rc.1**, rama `develop`. Contrato `bts-5.2`. **Fase 7 PARCIAL; sin aprobación para producción.**

Paquete de cuatro skills: orquestador, buscador, extractor y validador. Incluye procedimientos, reglas, contratos JSON y auxiliares Python de comparación. DEC-018 registra diferencias parciales de nombre únicamente en Identificación laboral cuando el DNI está corroborado, sin bloquear otros controles vinculados correctamente.

Los auxiliares reciben hechos ya corroborados: no prueban identidad, vínculos, autenticidad ni aplicabilidad por sí mismos. Esta distribución no contiene un motor autónomo, adaptadores Google operativos ni OCR Windows certificado.

## Uso y comprobación

Requiere Python 3.10 o posterior para los auxiliares y pruebas; biblioteca estándar, sin instalación de dependencias.

```sh
python -m unittest discover -s tests -v
python tools/verify_package.py
python skills/bts-orquestador/scripts/bts_core.py --describe
```

Leer `skills/bts-orquestador/references/autoridad.md` y conservar las cuatro carpetas juntas. No instalar ni ejecutar automáticamente el workflow al clonar este repositorio.

`evento.json` es una plantilla pública sin IDs de recursos ni identidades de entidades. Preparar configuración operativa fuera del repositorio, verificar los ocho requisitos de entidades, permisos, fuente, destinos, layout y responsable de publicación. Valores null son pendientes, no ausencia ni permiso para operar. La depuración pública conserva reglas pero no reemplaza la configuración privada autorizada.

## Estado y límites

El piloto privado probó cuatro trabajadores de dos proveedores: proveedores aleatorios y primeras dos ocurrencias por proveedor. Cuatro casos fue decisión del agente para acotar el piloto, no límite técnico ni cantidad exigida por el usuario. Se confirmaron publicaciones acotadas por relectura; esto no verifica un motor autónomo general. La pestaña original conserva A:F, recibe G:O y Revisar en P; Estado/Motivo fue archivado. Cuatro filas fueron confirmadas por relectura. El usuario confirmó los consumidores; no equivale a una prueba automatizada de compatibilidad ni a validación exhaustiva.

Se corrigió una omisión del agente en un SVO. Un control de hash fallido no detuvo inicialmente una escritura de proveedor; se reconcilió la fuente antes de central y se corrigió el control de salida. Estos antecedentes no constituyen una certificación preventiva completa.

Windows sigue sin verificar. El diagnóstico macOS obtuvo 54/63 cotejos literales, con nueve identificadores pendientes; no es una prueba Windows satisfactoria. Segundo actor y concurrencia quedaron diferidos; timeout real de Google y recuperación desde otro equipo siguen pendientes.

El repositorio excluye documentación laboral, transcripciones, imágenes, paquetes OCR del piloto, credenciales y registros personales. Los fixtures de tests son inventados. No hay release Windows ni tag publicados en esta primera entrega.

## Novedades 0.7.1-rc.1

DEC-019: recuperación dirigida ante lectura insuficiente y Revisar P con referencia documental. Salida central A:P, proveedores A:O; contrato5.2 añade incidencias estructuradas. Consumidores confirmados por usuario. OCR Windows pasa a Fase8 Staging, prueba final previa a producción; todavía pendiente. No se creó una automatización ni un release Windows.
