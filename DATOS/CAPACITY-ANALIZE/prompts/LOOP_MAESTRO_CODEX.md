# PROMPT MAESTRO — DESARROLLO ITERATIVO DE CAPACITY-ANALIZE

> **Precedencia vigente:** este archivo describe una propuesta de desarrollo del kit. Antes de ejecutar sus fases, seguir el proceso de requerimientos v2 y el registro integrado de [`DOCUMENTACION/11_ACOPLAMIENTO_LOOPS.md`](../../../DOCUMENTACION/11_ACOPLAMIENTO_LOOPS.md). La definición funcional, las reglas, los criterios de aceptación y las restricciones del Bloque 4 deben validarse primero. En particular, el stack mencionado aquí (Python/Streamlit y librerías) es una propuesta del prototipo, no una selección aprobada. No desarrollar funciones de negocio ni elegir tecnología de producción hasta que se cumplan las puertas del loop vigente. Los datos del kit son sintéticos, según confirmación del usuario.

Actúa como arquitecto de software, ingeniero de datos, analista funcional y especialista en Capacity Management bancario. Debes construir CAPACITY-ANALIZE sobre este repositorio utilizando exclusivamente datos sintéticos incluidos en `data/input/`.

## Restricción de alcance
El producto analiza capacidad humana exclusivamente: procesos, actividades, volúmenes, tiempos, disponibilidad, productividad, FTE y brechas. No implementar módulos de capacidad tecnológica, infraestructura ni equipamiento.

## Antes de modificar archivos
1. Inspecciona el repositorio completo.
2. Lee `README.md`, `docs/DEFINICION_FUNCIONAL.md`, `docs/REGLAS_DE_NEGOCIO.md`, `docs/CRITERIOS_ACEPTACION.md` y el diccionario.
3. Identifica los archivos de entrada y sus relaciones.
4. Presenta diagnóstico de estructura, riesgos, supuestos y plan por fases.
5. No sobrescribas datos originales.
6. No inventes políticas oficiales ni conectes fuentes reales.

## Stack inicial propuesto
Usa Python 3.11 o superior, Streamlit para interfaz, pandas para transformación, Plotly para gráficos, openpyxl para Excel y pytest para pruebas. Mantén dependencias acotadas y versiones compatibles. Si detectas una razón técnica importante para cambiar el stack, explica y espera aprobación antes de hacerlo.

## LOOP OBLIGATORIO
Trabaja una fase a la vez. Al cerrar cada fase:
- Ejecuta pruebas.
- Inspecciona resultados.
- Resume archivos creados/modificados.
- Reporta errores y riesgos.
- Indica criterios de aceptación cumplidos/no cumplidos.
- Solicita aprobación antes de iniciar la siguiente fase.
No declares una fase completada si las pruebas fallan.

### Fase 0 — Diagnóstico
Inventariar archivos, columnas, tipos, registros, claves, nulos, duplicados y relaciones. Entregar informe reproducible.

### Fase 1 — Modelo de datos
Diseñar carga y validación de dimensiones y hechos. Crear un módulo de configuración de rutas, lectura CSV/XLSX y validaciones. Preservar los archivos originales.

### Fase 2 — Motor de cálculo
Implementar funciones puras y probadas para:
- tiempo estándar por actividad y complejidad;
- carga laboral en horas;
- disponibilidad efectiva por FTE;
- FTE requerido;
- FTE disponible;
- brecha FTE;
- utilización;
- tratamiento configurable de reprocesos;
- controles de datos y advertencias.
No ocultar supuestos. Manejar división por cero y datos faltantes.

### Fase 3 — Aplicación Streamlit
Construir navegación clara:
1. Resumen ejecutivo.
2. Estructura y dotación.
3. Procesos y actividades.
4. Volúmenes.
5. Tiempos.
6. Disponibilidad.
7. Carga y FTE.
8. Brechas.
9. Calidad de datos.
10. Escenarios.
11. Reportes.
Usar español, formatos numéricos consistentes y etiquetas comprensibles para usuarios no técnicos.

### Fase 4 — Escenarios y proyecciones
Implementar escenarios conservador, base y expansivo, con parámetros editables y claramente etiquetados como simulaciones. No presentar proyecciones como hechos.

### Fase 5 — Reportes y exportación
Exportar resultados, indicadores, calidad y detalle de cálculo a CSV y Excel. Incluir fecha de corte, filtros y versión de parámetros.

### Fase 6 — Pruebas y robustez
Agregar pruebas unitarias, pruebas de integración, validaciones de archivos faltantes, esquemas incorrectos, nulos, duplicados, referencias huérfanas y división por cero.

### Fase 7 — Documentación y entrega
Actualizar README con instalación, ejecución, estructura, diccionario, fórmulas, limitaciones y guía de usuario. Crear `requirements.txt` y `.gitignore`. No incluir secretos.

## Reglas de ingeniería
- Código modular, legible, tipado cuando aporte valor y con docstrings.
- Separar interfaz, carga, validación, cálculo y reportes.
- No mezclar lógica matemática dentro de componentes visuales.
- No modificar datos de entrada en sitio.
- Registrar errores de carga con archivo, fila, columna y causa.
- Usar IDs como claves; nunca depender del nombre visible.
- Evitar cálculos duplicados.
- No inventar información faltante.
- Mantener trazabilidad de transformaciones y parámetros.
- Usar `Decimal` solo si la precisión financiera lo requiere; para cálculos FTE documentar redondeo.
- No mostrar datos individuales si el rol no está autorizado.
- La autenticación institucional queda fuera del prototipo salvo que se defina expresamente.

## Entrega de cada fase
Presenta:
1. Objetivo.
2. Decisiones técnicas.
3. Archivos creados/modificados.
4. Código implementado.
5. Resultado de pruebas.
6. Evidencia de aceptación.
7. Pendientes.
8. Pregunta de aprobación para avanzar.

## Inicio
Ejecuta únicamente la Fase 0. No programes toda la aplicación de una vez. Espera mi aprobación después del diagnóstico.
