---
name: bts-buscador
description: "Identificar de forma inequívoca la carpeta de un proveedor BTS y generar su inventario documental recursivo, conservando ubicaciones y pendientes de lectura."
---

# bts-buscador

Estado: distribución pública candidata 0.7.1-rc.1, contrato bts-5.2; Fase 7 PARCIAL y sin aprobación para producción. Leer autoridad/configuración y contratos del orquestador antes de usar el procedimiento. Mantener las cuatro carpetas juntas. Operaciones externas requieren configuración local, autorización y capacidades corroboradas. No contiene evidencia privada ni decide ingreso.

## Identificar proveedor

Tomar D literal exacta, raíz de evento y número sólo si está corroborado. Normalizar mayúsculas/tildes/Unicode/espacios conservando todas palabras y número. Patrón vigente NOMBRE proveedor-número; no usar el formato antiguo - [número]. Excepción sólo UJSA (UNIVERSO PRODUCCIONES), sin número. No aceptar alias ni agregar/quitar BA. [Auxiliar](../bts-orquestador/references/auxiliares.md) coteja formato, no demuestra pertenencia a raíz.

Consultar/listar dentro de raíz autorizada, paginar y guardar cadena de padres. Cero coincidencias con listado íntegro: NOT_FOUND; más de una carpeta principal válida: AMBIGUOUS sin elegir reciente ni mezclar; una: FOUND_UNIQUE. Permisos/404/páginas faltantes: TECHNICAL_PENDING. Una coincidencia textual no evita probar unicidad del ámbito. Enlaces fuera de raíz o shortcuts no comprobados: registrar dependencia sin seguirlos automáticamente.

## Inventariar

Recorrer todos los descendientes de la carpeta principal única, archivos sueltos y carpetas repetidas. Distinguir IDs de nombres iguales; controlar ciclos por ID manteniendo ubicaciones/aristas. Carpetas AP (Accidentes Personales) y ART orientan, no limitan; MONOTRIBUTO, AUTONOMO, CAT (Clave Alta Temprana) y VOLUNTARIO fueron nombres locales observados, no prueba de tipo documental ni de existencia Drive actual.

Registrar por archivo ID/MIME/tamaño/versión/ubicación/hash cuando disponible y disponibilidad. Inventario sin lectura completa se marca incompleto donde corresponda; no concluir ausencia por extensión/nombre. Mantener PDF, imágenes y tipos desconocidos para lectura o dependencia explícita. BUS no decide identidad del trabajador ni cumplimiento. Usar [índice](../bts-orquestador/references/indice.md).

## Retornar

Devolver search_status, carpeta/candidatos, parent_chain, inventario, completeness y query_log según contrato. FOUND_UNIQUE puede coexistir con inventario parcial; indicar qué falta. No aceptar Downloads como evidencia de Drive actual: modo local_snapshot requiere procedencia/hash/fecha, y reconciliación antes de publicación actual. Cambios por permisos no se etiquetan como documentos eliminados.
