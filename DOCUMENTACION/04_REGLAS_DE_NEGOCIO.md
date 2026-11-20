# 04. Reglas de negocio

> **Actualización (2026-11-20):** sí existen fórmulas y reglas candidatas en `DATOS/CAPACITY-ANALIZE/docs/REGLAS_DE_NEGOCIO.md` y en `src/calculations.py`; su presencia es evidencia de una propuesta implementada parcialmente, no de aprobación del banco. `RN-001` permanece Propuesto. La taxonomía de tiempo, el tratamiento de reprocesos, las horas extra y el parámetro de 1 FTE requieren validación conforme al Bloque 3 del LOOP v2.

**Estado:** PENDIENTE DE DEFINICIÓN

## Reglas confirmadas

No hay reglas de negocio oficiales confirmadas. El kit recibido contiene reglas y fórmulas candidatas, descritas como iniciales/ilustrativas; deben permanecer Propuestas hasta validación y aprobación explícitas.

La regla metodológica confirmada es no convertir hipótesis ni propuestas del kit en fórmula, indicador o comportamiento requerido. Esta regla gobierna el levantamiento, pero no es una regla del dominio del producto.

## Reglas pendientes

Se deben obtener de una fuente de negocio autorizada:

- Definición de capacidad y unidad de análisis.
- Entradas válidas, unidades, calendario y período de referencia.
- Fórmulas, redondeo, umbrales, excepciones y tratamiento de datos faltantes.
- Reglas de agregación, comparación y priorización, si aplican.
- Validaciones y resultados esperados para casos representativos.

Este documento no aprueba ninguna fórmula ni valor por defecto del kit. Hasta confirmar las reglas, el cálculo implementado en el prototipo no puede considerarse validado para decisiones del banco.
