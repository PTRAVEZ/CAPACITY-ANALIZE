# Metodología de cálculo — PROPUESTA (no oficial)

> Todo lo descrito aquí es una **fórmula metodológica propuesta** o un **parámetro que requiere aprobación**.
> Nada debe considerarse política del banco hasta que se valide en el LOOP (Bloque 3) y lo apruebe el responsable indicado.

## 1. Taxonomía de tiempo (categorías mutuamente excluyentes)

```
Horas nominales  (días laborables activos × horas por día × jornada/40)
 ├─ (−) Ausencias: vacaciones + enfermedad + permisos + licencias
 = Horas presentes
 ├─ (−) Capacitación institucional (dato real)
 ├─ (−) Tiempo no productivo = (presentes − capacitación) × PAR-002
 = Horas disponibles efectivas
```

## 2. Reglas anti-doble contabilización

| ID | Regla |
|---|---|
| RN-01 | Las ausencias **solo** reducen la capacidad disponible. Nunca se suman a la carga ni al FTE requerido neto. |
| RN-02 | La capacitación se toma del dato real y **no** forma parte del factor no productivo (PAR-002). |
| RN-03 | El volumen registra solo trabajo **de primera vez**. Los reprocesos se registran aparte y se valoran con `tiempo_reproceso_min`; no se aplica además un factor de reproceso sobre el tiempo estándar. |
| RN-04 | Cada actividad pertenece a un único proceso, la ejecuta un único cargo y se mide en una sola unidad de trabajo. |
| RN-05 | Las horas extra **no** aumentan la capacidad disponible. Se reportan como evidencia de brecha (FTE equivalente en horas extra). |
| RN-06 | La brecha efectiva (FTE disponible − FTE requerido) y la brecha de dotación (FTE contractual − FTE requerido para dotación) son dos lecturas del mismo fenómeno: **no se suman**. |
| RN-07 | Ausencias + capacitación nunca pueden superar las horas nominales. Si lo hacen, se ajustan proporcionalmente y se registra una advertencia (V-11). |

## 3. Fórmulas (para la unidad u, el cargo c y el mes m)

| ID | Indicador | Fórmula | Unidad |
|---|---|---|---|
| IND-01 | Horas por FTE nominal | `H_nom(m) = días_laborables(m) × PAR-001` | h |
| IND-02 | Horas por FTE productivo | `H_prod(m) = H_nom(m) × (1 − PAR-002)` | h |
| IND-03 | Carga laboral | `Σ_a volumen(u,a,m) × t_std(a)/60 + Σ_a reprocesos(u,a,m) × t_rep(a)/60` | h |
| IND-04 | FTE requerido | `Carga / H_prod(m)` | FTE |
| IND-05 | FTE contractual | `Horas nominales / H_nom(m)` | FTE |
| IND-06 | FTE disponible efectivo | `Horas disponibles efectivas / H_prod(m)` (equivale a `FTE contractual × (1 − tasa de indisponibilidad)`) | FTE |
| IND-07 | Brecha efectiva | `FTE disponible − FTE requerido` (negativa = faltante) | FTE |
| IND-08 | Utilización | `Carga / Horas disponibles efectivas` | % |
| IND-09 | Tasa de indisponibilidad | `(Ausencias + Capacitación) / Horas nominales` | % |
| IND-10 | FTE requerido para dotación | `FTE requerido / (1 − tasa de indisponibilidad anual)` | FTE |
| IND-11 | Brecha de dotación | `FTE contractual a la fecha de corte − FTE requerido para dotación` | FTE |
| IND-12 | Proporción de reproceso | `Horas de reproceso / Carga` | % |
| IND-13 | FTE potencialmente liberable por reprocesos | `Horas de reproceso / H_prod` | FTE |
| IND-14 | FTE equivalente en horas extra | `(Horas suplementarias + extraordinarias) / H_prod` | FTE |
| IND-15 | Estado de capacidad | Sobrecarga si IND-08 > PAR-004; Holgura si IND-08 < PAR-005; si no, Equilibrio | categoría |
| IND-16 | Carga de escenario | `Carga base anualizada × Π(1 + ajuste de volumen) × Π(1 + ajuste de tiempo)` | h |

En los indicadores anuales se suman las horas de los 12 meses y se dividen entre la suma de `H_prod(m)` del período.

## 4. Redistribución (oportunidad a evaluar)

Dentro de una misma gerencia y un mismo cargo, se emparejan unidades en **Holgura** (excedente = disponible − requerido) con unidades en **Sobrecarga** (déficit = requerido − disponible), en múltiplos de 0,5 FTE. El resultado es una **oportunidad**, no una decisión: falta evaluar la distancia, las competencias, la normativa laboral y la aprobación de las jefaturas.

## 5. Reglas de validación de datos

| Regla | Qué verifica | Acción |
|---|---|---|
| V-01 | La unidad padre existe | Error |
| V-02 | La unidad del colaborador existe | Excluir |
| V-03 | El cargo del colaborador existe | Excluir |
| V-04 | Fecha de salida ≥ fecha de ingreso | Excluir |
| V-05 | `colaborador_id` no duplicado | Conservar el primero |
| V-06 | El cargo y el proceso de la actividad existen | Excluir |
| V-07 | Tiempo estándar > 0 | Advertencia; la actividad no suma carga |
| V-08 | La actividad y la unidad del volumen existen | Excluir |
| V-09 | Volumen ≥ 0 | Excluir |
| V-10 | Sin duplicados (período, unidad, actividad) | Conservar el primero |
| V-11 | Ausencias + capacitación ≤ horas nominales | Ajuste proporcional y advertencia |
| V-12 | Ausencias y horas extra corresponden a un colaborador válido y activo | Excluir |
| V-13 | Reprocesos ≤ volumen y con volumen asociado | Excluir |
| V-14 | Período dentro del período base | Excluir |
| V-15 | Conciliación: dotación inicial + ingresos − salidas = dotación a la fecha de corte | OK / Error |
| V-16 | Carga sin personal del cargo en la unidad | Advertencia |

## 6. Limitaciones conocidas del demostrador

- No modela traslados entre unidades: cada colaborador tiene una única asignación.
- Los escenarios 2027 usan las horas productivas promedio del período base.
- No hay estacionalidad en la indisponibilidad aplicada a los escenarios (se usa la tasa anual).
- Los tiempos estándar son ficticios y no reflejan mediciones reales.
