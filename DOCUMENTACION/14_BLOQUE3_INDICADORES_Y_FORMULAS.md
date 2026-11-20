# 14 · LOOP v2.1 — Bloque 3: Resultados, indicadores y fórmulas

> **Contexto:** el usuario aprobó el Bloque 2 en el chat el 2026-11-20, así que DEC-019 a DEC-026 pasan a *Confirmado*.
> En este bloque **ninguna fórmula es oficial**: todas son *Fórmulas metodológicas propuestas* y los valores son *Parámetros que requieren aprobación* (aprobador: Comité de Capacidad, DEC-016).
> Los ejemplos numéricos son **ilustrativos**: salen de los datos ficticios de `DATOS/BANCO-VOLCAN-AZUL/`.

## 3.0 Taxonomía de tiempo y reglas contra la doble contabilización

```
Horas nominales  = días laborables activos × PAR-001 × (jornada / 40)
 (−) Ausencias   = vacaciones + enfermedad + permisos + licencias        [FTE-SRC-10]
 = Horas presentes
 (−) Capacitación institucional (dato real)                              [FTE-SRC-10]
 (−) Tiempo no productivo = (presentes − capacitación) × PAR-002
 = Horas disponibles efectivas
```

| ID | Estado | Regla |
|---|---|---|
| RN-01 | Propuesto | Las ausencias **solo** reducen la capacidad disponible; nunca se suman a la carga. |
| RN-02 | Propuesto | La capacitación se toma del dato real y queda **fuera** de PAR-002. |
| RN-03 | Propuesto | El volumen cuenta solo el trabajo de primera vez (SUP-003). Los reprocesos se valoran aparte con `tiempo_reproceso_min`, sin aplicar además un factor de reproceso. |
| RN-04 | Propuesto | Cada actividad pertenece a un solo proceso, la ejecuta un solo cargo y se mide en una sola unidad de trabajo. |
| RN-05 | Propuesto | Las horas extra **no** aumentan la capacidad: se reportan como evidencia de brecha (IND-14). |
| RN-06 | Propuesto | La brecha efectiva (IND-07) y la brecha de dotación (IND-11) son dos lecturas del mismo fenómeno: **no se suman**. |
| RN-07 | Propuesto | Ausencias + capacitación ≤ horas nominales. Si se supera, se ajusta proporcionalmente y se registra la advertencia V-11. |
| PAR-001 | Requiere aprobación | Horas de jornada diaria = 8. **Definición de 1 FTE** = días laborables del mes × 8 h (≈ 2.000 h nominales al año en el período base). |
| PAR-002 | Requiere aprobación | Factor no productivo = 10 %. Por lo tanto, 1 FTE productivo ≈ 1.800 h al año. |
| PAR-004 / PAR-005 | Requieren aprobación | Umbrales: sobrecarga si la utilización supera 105 %; holgura si es menor a 80 %. |
| PAR-006 | Requiere aprobación | Agregación mínima para reportar: 3 personas. |

## 3.1 Fichas de indicadores (IND-)

Leyenda de la columna **Naturaleza**: FMP = fórmula metodológica propuesta; PAR = depende de un parámetro que requiere aprobación. La columna **Demo** indica si `src/capacity_analize.py` ya calcula el indicador (✔) o falta programarlo (✖).

| ID | Indicador | Objetivo | Fórmula | Unidad | Fuentes | Frecuencia / desagregación | Interpretación | Validación | Doble conteo | Naturaleza | Demo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IND-01 | Horas por FTE nominal | Base de conversión | `H_nom = días_lab × PAR-001` | h | 04, 05 | Mensual / banco | Horas de 1 FTE sin descuentos | > 0 | — | PAR | ✔ |
| IND-02 | Horas por FTE productivo | Base de conversión | `H_prod = H_nom × (1 − PAR-002)` | h | 04, 05 | Mensual / banco | Horas útiles de 1 FTE sin ausencias | < H_nom | RN-02 | PAR | ✔ |
| IND-03 | Carga laboral | Medir el trabajo requerido | `Σ vol × t_std/60 + Σ reproc × t_rep/60` | h | 07, 08, 09 | Mensual / unidad × cargo × actividad | Horas de trabajo necesarias | vol ≥ 0; reproc ≤ vol | RN-03, RN-04 | FMP | ✔ |
| IND-04 | FTE requerido | Dimensionar | `Carga / H_prod` | FTE | IND-03, IND-02 | Mensual / unidad × cargo | Personas productivas necesarias | ≥ 0 | RN-01 | FMP | ✔ |
| IND-05 | FTE contractual | Dotación pagada | `Horas nominales / H_nom` | FTE | 03, 04 | Mensual / unidad × cargo | Dotación equivalente a tiempo completo | Concilia con V-15 | — | FMP | ✔ |
| IND-06 | FTE disponible efectivo | Capacidad real | `Horas disponibles / H_prod` = `FTE contractual × (1 − tasa de indisponibilidad)` | FTE | 03, 10 | Mensual / unidad × cargo | Capacidad real después de ausencias | ≤ FTE contractual | RN-01, RN-02 | FMP | ✔ |
| IND-07 | Brecha efectiva | Detectar faltante o exceso | `IND-06 − IND-04` | FTE | — | Mensual / unidad × cargo | < 0 faltante; > 0 exceso | — | RN-06 | FMP | ✔ |
| IND-08 | Utilización | Nivel de carga | `Carga / Horas disponibles` | % | IND-03, 03, 10 | Mensual / unidad × cargo | > PAR-004 sobrecarga; < PAR-005 holgura | 0–200 % (más alto se investiga) | — | FMP + PAR | ✔ |
| IND-09 | Tasa de indisponibilidad | Medir ausentismo y capacitación | `(Ausencias + Capacitación) / Horas nominales` | % | 10 | Mensual / unidad × cargo | Proporción de tiempo no disponible | 0–100 % | RN-07 | FMP | ✔ |
| IND-10 | FTE requerido para dotación | Planificar contrataciones | `IND-04 / (1 − IND-09 anual)` | FTE | — | Anual / unidad × cargo | Personas a tener en nómina | ≥ IND-04 | RN-01 (las ausencias se aplican una sola vez) | FMP | ✔ |
| IND-11 | Brecha de dotación | Sustentar vacantes (D-1, D-2) | `FTE contractual a la fecha de corte − IND-10` | FTE | 03 | Anual / unidad × cargo | < 0 contratar; > 0 redistribuir | — | RN-06 | FMP | ✔ |
| IND-12 | Proporción de reproceso | Calidad del proceso | `Horas de reproceso / Carga` | % | 09 | Mensual / proceso, unidad | Trabajo que se hace dos veces | 0–100 % | RN-03 | FMP | ✔ |
| IND-13 | FTE liberable por reprocesos | Priorizar mejoras (D-4) | `Horas de reproceso / H_prod` | FTE | 09 | Anual / proceso × causa | Capacidad que se recupera si se eliminan | — | RN-03 | FMP | ✔ |
| IND-14 | FTE equivalente en horas extra | Evidencia de brecha | `(Horas suplementarias + extraordinarias) / H_prod` | FTE | 11 | Mensual / unidad × cargo | Capacidad que se cubre con horas extra | — | RN-05 | FMP | ✔ |
| IND-15 | Estado de capacidad | Semáforo | Sobrecarga / Equilibrio / Holgura según IND-08 | categoría | IND-08 | Mensual y anual | Prioriza la atención | — | — | PAR | ✔ |
| IND-16 | FTE de escenario | Proyectar (D-5) | `Carga base anualizada × Π(1+Δvol) × Π(1+Δtiempo) / H_prod` | FTE | 14 | Anual / escenario × unidad × cargo | Necesidad de FTE en 2027 | Δ entre −100 % y +200 % | RN-01 | FMP + Supuesto | ✔ |
| IND-17 | Productividad por FTE | Comparar unidades del mismo cargo | `Volumen de la actividad / FTE disponible del cargo` | unidades / FTE-mes | 08, IND-06 | Mensual / actividad × unidad | Más alta = más trabajo por persona (comparar solo dentro del mismo cargo) | Excluir grupos < PAR-006 | — | FMP | ✖ |
| IND-18 | Índice estacional | Anticipar picos | `Carga del mes / Carga promedio mensual` | índice | IND-03 | Mensual / proceso | > 1,10 pico (diciembre, agosto, abril) | Requiere ≥ 12 meses (RSK-002) | — | FMP | ✖ |
| IND-19 | Dispersión de carga | Visibilidad de la distribución (síntoma B) | `Desviación estándar / media de IND-08` entre unidades del mismo cargo y gerencia | coeficiente | IND-08 | Trimestral / cargo × gerencia | > 0,20 indica carga desigual | ≥ 3 unidades | — | FMP | ✖ |
| IND-20 | Pareto de causas de reproceso | Causa raíz (D-4) | Ranking de horas de reproceso por causa con % acumulado | h, % | 09 | Trimestral / proceso × causa | El 20 % de causas que explica ~80 % de las horas | — | RN-03 | FMP | ✖ |
| IND-21 | Oportunidad de redistribución | Rebalancear (D-3) | Emparejar holgura y sobrecarga del mismo cargo y gerencia, en múltiplos de 0,5 FTE | FTE | IND-07, IND-08 | Trimestral | Movimiento a **evaluar**, no una orden | Considerar distancia y competencias | — | FMP | ✔ |

### Ejemplo numérico ilustrativo — Cajeros de la Agencia Matriz Quito (período base)

| Paso | Valor |
|---|---|
| Horas nominales (9,7 FTE contractuales promedio) | 19.336 h |
| (−) Ausencias 2.188 h, (−) capacitación 486 h → tasa de indisponibilidad (IND-09) | 13,8 % |
| Horas disponibles efectivas (después de PAR-002) | 14.996 h → **IND-06 = 8,33 FTE** |
| Carga: 19.423 h estándar + 145 h de reproceso | 19.568 h → **IND-04 = 10,87 FTE** |
| Brecha efectiva (IND-07) | **−2,54 FTE** |
| Utilización (IND-08) | **130 %** → Sobrecarga |
| FTE requerido para dotación (IND-10) = 10,87 / (1 − 0,138) | 12,62 FTE |
| Brecha de dotación (IND-11) = 9 contratados − 12,62 | **−3,62 FTE** (no se suma a IND-07, RN-06) |
| Horas extra pagadas | 1.358 h ≈ 0,75 FTE (IND-14) |

## 3.2 Decisiones y los indicadores que las sustentan

| Decisión (DEC-010) | Indicadores |
|---|---|
| D-1 Vacantes de reemplazo | IND-07, IND-11, IND-08 (tendencia), IND-14 |
| D-2 Posiciones nuevas | IND-10, IND-11, meses en sobrecarga (IND-15), IND-14 |
| D-3 Redistribución | IND-21, IND-19, IND-17 |
| D-4 Reprocesos y automatización | IND-12, IND-13, IND-20, IND-16 (escenario de automatización) |
| D-5 Dotación del año siguiente | IND-16 por escenario, IND-10, IND-18 |

## 3.3 Escenarios (3.x)

| ID | Estado | Descripción |
|---|---|---|
| DEC-027 | Propuesto | Variables que el usuario puede mover en un escenario: % de volumen (global, por proceso o por actividad), % de tiempo estándar por actividad (automatización), tasa de indisponibilidad (opcional) y PAR-002. |
| DEC-028 | Propuesto | Escenarios base para 2027: Base (+4 % de volumen), Migración digital, Automatización de back office y Crecimiento comercial (FTE-SRC-14). Todos son *Supuestos* hasta que los apruebe el Comité. |
| SUP-005 | Supuesto | Las horas productivas de 2027 se estiman con el promedio del período base. |

## 3.4 Salidas (3.y)

| Salida | Contenido | Usuario (DEC-015) | Frecuencia |
|---|---|---|---|
| Tablero ejecutivo | IND-04, 06, 07, 08 y 15 por gerencia, más escenarios | USR-05, USR-06 | Mensual / trimestral |
| Tablero de gerencia | Comparativo de unidades, IND-19, IND-21 y horas extra | USR-03 | Mensual |
| Ficha de unidad | Carga por actividad, IND-08, IND-12 e IND-17 | USR-02 | Mensual |
| Reporte de calidad de datos | Resultados de V-01 a V-16 y conciliación | USR-01, USR-04 | Cada carga |
| Exportación Excel | Todas las tablas de resultados del período | USR-01 | A pedido |
| Sustento de vacante | IND-07, 10, 11 y 14 de la unidad y el cargo, con su tendencia | USR-03, USR-04 | Por evento |

| ID | Estado | Descripción |
|---|---|---|
| DEC-029 | Propuesto | Se adoptan los indicadores IND-01 a IND-21 y las salidas de la tabla anterior. IND-17 a IND-20 se programan en la siguiente fase del demostrador. |

---

## Resumen del Bloque 3

- ✅ **Confirmado (Bloque 2):** DEC-019 a DEC-026.
- 💡 **Propuesto:** RN-01 a RN-07, IND-01 a IND-21 y DEC-027 a DEC-029.
- 🔧 **Parámetros que requieren aprobación:** PAR-001 (8 h; 1 FTE ≈ 2.000 h nominales), PAR-002 (10 %), PAR-004/005 (105 % / 80 %) y PAR-006 (3 personas).
- ⚠️ **Supuestos:** SUP-005 (horas de 2027) y los escenarios de FTE-SRC-14.
- ⏳ **Pendiente:** PEN-004, PEN-005, PEN-006 y la programación de IND-17 a IND-20.
- 🔗 **Impacto:** en el Bloque 4, los permisos de cada salida y los criterios de aceptación de exactitud (reproducir IND-03 a IND-11).
- 🧾 **Decisiones que el usuario debe aprobar:** la taxonomía y RN-01 a RN-07; PAR-001, PAR-002, PAR-004 y PAR-005; IND-17 a IND-20 como indicadores nuevos; DEC-027 y DEC-028 (escenarios).

**Verificación de coherencia:** cada indicador está ligado a fuentes del Bloque 2 y a las decisiones D-1 a D-5 del Bloque 1. Las reglas RN- evitan contar dos veces ausencias, reprocesos y horas extra.
