# Criterios de aceptación iniciales

1. La aplicación carga todos los CSV del directorio `data/input/`.
2. Detecta archivos faltantes, columnas faltantes y tipos inválidos.
3. Reporta duplicados en claves primarias.
4. Reporta referencias huérfanas entre dimensiones y hechos.
5. Valida períodos YYYY-MM y valores no negativos.
6. Calcula tiempo estándar por actividad y complejidad.
7. Calcula carga laboral en horas sin mezclar minutos y horas.
8. Calcula horas efectivas por FTE sin doble descuento.
9. Calcula FTE requerido, FTE disponible y brecha.
10. Permite filtrar resultados por período, dirección, departamento, agencia, proceso, actividad y cargo cuando aplique.
11. Identifica explícitamente datos sintéticos y parámetros no aprobados.
12. Exporta resultados y hallazgos de calidad a CSV/XLSX.
13. Mantiene trazabilidad de archivo, período, versión y fecha de cálculo.
14. Incluye pruebas automatizadas para fórmulas y validaciones críticas.
15. No presenta datos ficticios como resultados reales del banco.
