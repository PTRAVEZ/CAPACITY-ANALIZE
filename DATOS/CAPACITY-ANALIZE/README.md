> **Kit historico (Banco Andino del Ecuador, ficticio).** Se conserva solo como referencia (DEC-005). El escenario oficial del LOOP es [DATOS/BANCO-VOLCAN-AZUL/](../BANCO-VOLCAN-AZUL/) (DEC-004). No mezclar datos ni resultados de ambos kits.

# CAPACITY-ANALIZE
## Kit inicial de datos ficticios y definición funcional

**Institución simulada:** Banco Andino del Ecuador (FICTICIO)  
**País de referencia:** Ecuador  
**Corte de datos:** octubre de 2026  
**Período histórico de volúmenes y disponibilidad:** enero de 2025 a octubre de 2026.

> ADVERTENCIA: todos los datos de este repositorio son sintéticos. No representan clientes, colaboradores, operaciones, cifras ni políticas de una institución financiera real. No utilizar para decisiones reales de contratación, desempeño o dimensionamiento.

## Objetivo
Prototipar un sistema de análisis de capacidad humana: carga laboral, tiempos estándar, disponibilidad, productividad, FTE requerido, FTE disponible y brechas.

## Alcance
Incluye exclusivamente trabajo humano y su dimensionamiento. No calcula capacidad tecnológica, infraestructura, equipos ni presupuesto de otros recursos.

## Estructura
- `data/input/`: CSV de entrada y libro Excel consolidado.
- `data/reference/`: diccionario de datos.
- `data/output/`: reservado para resultados calculados.
- `docs/`: alcance, reglas, arquitectura funcional y criterios de aceptación.
- `prompts/`: prompt maestro de desarrollo iterativo para Codex.
- `src/`: reservado para implementación.
- `tests/`: pruebas automatizadas.

## Cómo empezar
1. Clona el repositorio.
2. Revisa `docs/REGLAS_DE_NEGOCIO.md`.
3. Revisa el diccionario `data/reference/diccionario_datos.csv`.
4. Abre `data/input/CAPACITY_ANALIZE_DATOS_FICTICIOS.xlsx` para inspeccionar las tablas.
5. Usa el prompt `prompts/LOOP_MAESTRO_CODEX.md` en Codex para construir la aplicación por fases.
6. No sustituyas los parámetros ilustrativos por políticas institucionales sin aprobación.

## Archivos de entrada
Los CSV son la fuente de datos portable y el Excel es una vista consolidada para revisión manual. Los IDs son claves sintéticas.

## Principios de cálculo
- Volumen y tiempos deben estar expresados en unidades compatibles.
- Los tiempos se convierten de minutos a horas.
- El FTE se calcula como carga total en horas / horas efectivas disponibles por FTE.
- El FTE disponible se calcula a partir de dotación activa equivalente, considerando dedicación.
- No sumar ausentismo dos veces si ya está descontado en disponibilidad.
- Reprocesos deben tratarse de forma explícita para evitar duplicidad de volumen.
- Las métricas deben poder desagregarse por período, dirección, departamento, agencia, proceso, actividad y cargo, cuando exista granularidad.

## Estado
Este es un kit de datos y especificación inicial. No contiene aún una aplicación productiva. La aplicación debe construirse y probarse siguiendo el prompt maestro.
