# 03. Requerimientos funcionales

> **Actualización funcional (2026-11-20):** el LOOP v2 y las respuestas del usuario confirman el dominio y alcance de alto nivel: capacidad humana en un banco privado; los síntomas A, B y C coexisten; los datos aportados son sintéticos. El levantamiento sigue en Bloque 1, Tema 1.1: el método actual, el esfuerzo y las fallas/impactos todavía no están descritos. Los módulos, roles y flujos en `DATOS/CAPACITY-ANALIZE/docs/DEFINICION_FUNCIONAL.md` son propuestas iniciales, no requerimientos aprobados. Véase el registro integrado en `11`.

**Estado:** PENDIENTE DE DEFINICIÓN detallada
**Base de evidencia:** el diagnóstico inicial precede al kit y al LOOP v2. Actualmente están confirmados el dominio y los síntomas de alto nivel; todavía no está definido el proceso concreto ni sus resultados.

## Propósito y alcance conocidos

Está confirmado que CAPACITY-ANALIZE apoyará análisis de capacidad humana en un banco privado, para atender los tres síntomas registrados en `11`. El nombre del repositorio no se usa como evidencia adicional para inferir procesos, usuarios ni fórmulas.

Siguen pendientes los procesos concretos, usuarios, entradas, transformaciones, resultados, indicadores, reglas y escenarios. Se levantarán en el orden de los cuatro bloques v2, una pregunta principal por turno; no se usará la lista antigua de preguntas de este archivo como cuestionario simultáneo.

## Requerimientos confirmados

| ID | Requerimiento confirmado | Fuente |
|---|---|---|
| RQ-P01 | No presentar hipótesis como requerimientos ni implementar funcionalidades de negocio sin evidencia suficiente. | Instrucción del usuario de este ciclo. |
| RQ-P02 | Mantener documentación, trazabilidad y resultados de pruebas veraces durante el desarrollo. | Instrucción del usuario de este ciclo. |
| RQ-P03 | Confirmar propósito y definiciones indispensables antes de implementar funcionalidad de negocio. | Instrucción de primera ejecución. |

Estos requerimientos gobiernan el proceso de trabajo; no describen la funcionalidad final del producto.

## Preguntas indispensables para definir el producto

1. **Problema y decisión:** ¿qué proceso concreto debe apoyar CAPACITY-ANALIZE, qué decisión se quiere tomar con sus resultados y quién la toma o utiliza?
2. **Datos de entrada:** ¿qué archivos, sistemas o fuentes existen? Comparte, si es posible, un ejemplo anonimizado y el significado de sus campos, unidades, períodos y granularidad.
3. **Resultados y reglas:** ¿qué resultados necesita el usuario y cuáles son las definiciones oficiales, fórmulas, restricciones y ejemplos de resultados correctos? Si una métrica aún no está definida, indícalo expresamente.
4. **Operación y aceptación:** ¿cómo se usará y actualizará el producto, qué restricciones de acceso/privacidad/despliegue aplican y qué evidencia demostraría que resuelve el problema?

Con estas respuestas se podrá redactar una especificación verificable. Si hay documentos o hojas de cálculo que ya definan el proceso, pueden servir como fuente; no se requiere que las reglas se inventen durante el desarrollo.

## Usuarios, escenarios, entradas y salidas

Todos pendientes de las respuestas anteriores. No se documentan escenarios ficticios.
