# 03 · Bitácora de carga de datos del piloto

> **Simulación con datos ficticios.** Banco Volcán Azul S.A. no existe; fechas, personas y cifras son ilustrativas.

**Fuentes:** las 14 fuentes del piloto, entregadas por sus dueños (DEC-019 a DEC-026) y revisadas con
`FASE1_ARRANQUE/scripts/validar_carga.py`. Los reportes completos están en `resultados/validacion_*.csv`.

| Ronda | Fecha | Qué cambió | Errores esquema | Errores reglas | Advertencias | Resultado |
|---|---|---|---|---|---|---|
| Ronda 1 | 2026-12-07 | Primera entrega de los dueños de fuentes | 31 | 0 | 0 | NO APTA |
| Ronda 2 | 2026-12-11 | Correcciones de esquema | 0 | 3 | 4 | NO APTA |
| Ronda 3 | 2026-12-16 | Correcciones de reglas de negocio y parámetros aprobados | 0 | 0 | 3 | APTA |
| Carga final | 2027-01-12 | Nuevos tiempos estándar y volumen de ACT-017 | 0 | 0 | 2 | APTA |

## Ronda 1 · Errores típicos de una primera entrega

| Hallazgo | Regla | Corrección pedida |
|---|---|---|
| Nómina incluyó la columna `cedula` (324 filas) | S-04 | Eliminarla: el piloto solo usa seudónimos (DEC-025) |
| 6 colaboradores con modalidad "Hibrido" | S-08 | Usar el valor de la lista: "Híbrida" |
| Ausentismo de septiembre con período "09/2026" (301 filas) | S-06 | Formato AAAA-MM |
| No se entregó `13_vacantes.csv` | S-01 | Talento Humano la envía |
| Un volumen negativo (−350) y un registro duplicado en el core | S-07, S-09 | Corregir en el origen |

## Ronda 2 · Lo que solo ven las reglas de negocio

| Hallazgo | Regla | Causa confirmada por el dueño de la fuente |
|---|---|---|
| COL-9001 en la unidad AG-QCE, que no existe | V-02 | Registro de prueba de nómina: se elimina |
| COL-9002 con salida anterior al ingreso | V-04 | Registro de prueba de nómina: se elimina |
| Volumen de la actividad ACT-999 | V-08 | Código de prueba del core: se elimina |
| COL-0150 con 220 h de vacaciones en julio | V-11 | Era el saldo acumulado; las horas reales son 88 |

En la ronda 3 también se registran como aprobados los parámetros PAR-001, 002, 004 y 005 (piloto) y PAR-006.

## Carga final · Advertencias que quedan (no impiden calcular)

| regla | archivo | registro | detalle |
|---|---|---|---|
| V-16 | cálculo | 2025-12|AG-AMB|CAR-JAG | Carga de 141.7 h sin personal disponible del cargo → Revisar asignación de actividad o vacante |
| V-16 | cálculo | 2026-08|AG-IBA|CAR-SOP | Carga de 128.8 h sin personal disponible del cargo → Revisar asignación de actividad o vacante |

Las advertencias V-16 corresponden a meses con una vacante abierta: la carga existió y la cubrió otra persona.
Se informan al Comité como observación.

**Lección:** sin el validador, la primera entrega habría producido resultados con datos personales,
una persona inexistente y volúmenes de prueba. Con él, la carga quedó apta en 3 rondas y 7 días hábiles.
