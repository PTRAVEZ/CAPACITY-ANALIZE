# Anomalías sembradas a propósito en los datos ficticios

Sirven para comprobar que las reglas de validación funcionan (prueba `test_ca05`). Aparecen en `data/output/00_reporte_validacion.csv`.

| # | Archivo | Registro | Anomalía | Regla que la detecta | Tratamiento |
|---|---|---|---|---|---|
| 1 | 03_colaboradores.csv | COL-9001 | Unidad `AG-QCE` no existe en la estructura | V-02 | Excluido |
| 2 | 03_colaboradores.csv | COL-9002 | Fecha de salida anterior a la de ingreso | V-04 | Excluido |
| 3 | 07_actividades.csv | ACT-017 | Actividad sin tiempo estándar ("Pendiente de medición") | V-07 | No suma carga |
| 4 | 08_volumenes_mensuales.csv | 2026-03 · AG-AMB · ACT-001 | Registro duplicado | V-10 | Se conserva el primero |
| 5 | 08_volumenes_mensuales.csv | 2026-03 · AG-RIO · ACT-002 | Volumen negativo (−350) en una fila adicional | V-09 | Excluido |
| 6 | 08_volumenes_mensuales.csv | 2026-06 · DEP-PAG · ACT-999 | Actividad inexistente | V-08 | Excluido |
| 7 | 10_ausentismo.csv | COL-0150 · 2026-07 | 220 h de vacaciones, más que las horas nominales del mes | V-11 | Ajuste proporcional |

COL-9001 y COL-9002 son registros adicionales: no forman parte de la dotación real del piloto, por eso la conciliación (V-15) cuadra después de excluirlos.
