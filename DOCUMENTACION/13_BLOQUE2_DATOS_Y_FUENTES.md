# 13 · LOOP v2.1 — Bloque 2: Datos y fuentes de información

> ✅ **Bloque aprobado por el usuario en el chat (2026-11-20).** DEC-019 a DEC-026 y las fichas FTE-SRC-01 a 14 pasan a *Confirmado*; los SUP-, PEN- y RSK- se mantienen.

> **Contexto:** el usuario aprobó el Bloque 1 en el chat el 2026-11-20, así que DEC-004 a DEC-018 pasan a *Confirmado*.
> Este bloque mantiene el modo de trabajo autorizado: el consultor propone y el usuario valida. Todo lo nuevo queda en estado *Propuesto* o *Supuesto*.
> Las fuentes son los 14 CSV **ficticios** de `DATOS/BANCO-VOLCAN-AZUL/data/input/`. El diccionario campo por campo está en `DATOS/BANCO-VOLCAN-AZUL/docs/diccionario_datos.md` (DAT- de referencia).

## 2.0 Mapa de fuentes frente a la información requerida

| Tema LOOP | Fuente propuesta | Cobertura | Observación |
|---|---|---|---|
| 2.1 Estructura organizacional | FTE-SRC-01 | Completa | 21 unidades y 4 niveles |
| 2.2 Colaboradores y dotación | FTE-SRC-03 | Completa | Seudonimizada; 322 personas reales + 2 registros erróneos sembrados |
| 2.3 Cargos y perfiles | FTE-SRC-02 | Parcial | Sin descriptor de funciones ni competencias (no requeridos para FTE) |
| 2.4 Jornada y disponibilidad | FTE-SRC-03 (jornada) + FTE-SRC-04 (calendario) + FTE-SRC-05 (PAR-001, PAR-002) | Completa | Calendario referencial (ver RSK-001) |
| 2.5 Procesos y actividades | FTE-SRC-06 + FTE-SRC-07 | Casi completa | ACT-017 sin tiempo estándar (PEN-005) |
| 2.6 Volúmenes | FTE-SRC-08 | Completa | 61 % sistema, 23 % registro manual, 14 % bitácora de horas, 2 % centro de contacto |
| 2.7 Tiempos de ejecución | FTE-SRC-07 | Completa con calidad mixta | 32 por estudio de tiempos, 19 por registro de sistema, 16 por estimación experta, 13 por bitácora, 1 pendiente |
| 2.8 Ausentismo y vacaciones | FTE-SRC-10 | Completa | Sin diagnóstico médico (privacidad) |
| 2.9 Horas extra | FTE-SRC-11 | Completa | Horas suplementarias y extraordinarias |
| 2.10 Reprocesos y errores | FTE-SRC-09 | Completa | Solo la causa principal del mes |
| 2.11 Productividad y calidad | Derivada (FTE-SRC-08 + FTE-SRC-03/10) | Derivada | No hay fuente propia: la productividad se calcula (Bloque 3) |
| 2.12 Rotación y vacantes | FTE-SRC-12 + FTE-SRC-13 | Completa | Ingresos y salidas, sin traslados (RSK-003) |
| 2.13 Histórico y proyecciones | 12 meses en FTE-SRC-08 a 11 + FTE-SRC-14 | Parcial | Solo 12 meses de historia (RSK-002) |

## 2.1 Fichas de fuentes (FTE-SRC-)

| ID | Fuente | Dueño | Formato | Frecuencia | Histórico | Granularidad | Calidad | Llave de cruce | Acceso |
|---|---|---|---|---|---|---|---|---|---|
| FTE-SRC-01 | Estructura organizacional | Talento Humano / Organización y Métodos | CSV (extracción del organigrama) | Al cambiar la estructura | Vigente | Unidad | Alta | `unidad_id` | Interno |
| FTE-SRC-02 | Catálogo de cargos | Talento Humano | CSV | Al cambiar el catálogo | Vigente | Cargo | Alta | `cargo_id` | Interno |
| FTE-SRC-03 | Colaboradores | Talento Humano (nómina) | CSV seudonimizado | Mensual | Ingresos desde 2006 | Colaborador | Alta (2 errores detectados: V-02, V-04) | `colaborador_id`, `unidad_id`, `cargo_id` | **Confidencial** |
| FTE-SRC-04 | Calendario laboral | Talento Humano | CSV | Anual | 2025-11 a 2026-10 | Día | Media (feriados referenciales) | `fecha`, `periodo` | Público interno |
| FTE-SRC-05 | Parámetros | Comité de Capacidad | CSV | Al aprobarse | Vigente | Parámetro | No aplica (ninguno aprobado) | `parametro_id` | Interno |
| FTE-SRC-06 | Mapa de procesos | Procesos y Calidad | CSV | Anual | Vigente | Proceso | Alta | `proceso_id` | Interno |
| FTE-SRC-07 | Actividades y tiempos estándar | Capacity Management | CSV | Anual o cuando cambia el proceso | Mediciones de 2025 | Actividad | Media (16 estimaciones expertas; 1 pendiente) | `actividad_id`, `cargo_id`, `proceso_id` | Interno |
| FTE-SRC-08 | Volúmenes mensuales | Operaciones (core), Centro de Contacto, jefaturas | CSV | Mensual | 12 meses | Unidad × actividad × mes | Alta en sistema; media en manual (3 errores sembrados) | `periodo`, `unidad_id`, `actividad_id` | Interno |
| FTE-SRC-09 | Reprocesos | Jefaturas | CSV (registro manual) | Mensual | 12 meses | Unidad × actividad × mes | Media | Igual a FTE-SRC-08 | Interno |
| FTE-SRC-10 | Ausentismo y capacitación | Talento Humano | CSV | Mensual | 12 meses | Colaborador × mes | Alta (1 exceso detectado: V-11) | `colaborador_id`, `periodo` | **Confidencial** (salud) |
| FTE-SRC-11 | Horas extra | Talento Humano (nómina) | CSV | Mensual | 12 meses | Colaborador × mes | Alta | `colaborador_id`, `periodo` | **Confidencial** |
| FTE-SRC-12 | Movimientos de personal | Talento Humano | CSV | Por evento | 12 meses | Movimiento | Alta (concilia: V-15) | `colaborador_id` | Confidencial |
| FTE-SRC-13 | Vacantes | Talento Humano (selección) | CSV | Por evento | 12 meses | Vacante | Alta | `unidad_id`, `cargo_id` | Interno |
| FTE-SRC-14 | Escenarios 2027 | Planificación / Capacity | CSV | Anual | Proyección | Ajuste | Supuesto | `proceso_id`, `actividad_id` | Interno |

### Ejemplos anonimizados (una fila por fuente transaccional)

| Fuente | Ejemplo |
|---|---|
| FTE-SRC-03 | `COL-0001, GER-OPC, CAR-GER, 2013-12-02, (sin salida), Indefinido, 40, Presencial` |
| FTE-SRC-07 | `ACT-001, P-CAJ, Depósito en efectivo o cheque, CAR-CAJ, transacción, 2.1 min, 1.5 min, Estudio de tiempos` |
| FTE-SRC-08 | `2025-11, AG-QMA, ACT-001, 12033, Core bancario` |
| FTE-SRC-09 | `2025-11, AG-QMA, ACT-001, 106, Error de digitación` |
| FTE-SRC-10 | `COL-0001, 2025-11, vac 0, enf 0, perm 0, lic 0, cap 4 h` |
| FTE-SRC-11 | `COL-0002, 2025-12, 3 h suplementarias, 4 h extraordinarias` |
| FTE-SRC-12 | `MOV-001, COL-0142, SALIDA, 2025-12-30, DEP-CCT, CAR-ACC` |
| FTE-SRC-13 | `VAC-001, DEP-OCR, CAR-ANO, Reemplazo, 2026-02-15 → 2026-03-11, Cubierta` |

## 2.2 Modelo de relación entre fuentes

```
01 Estructura ──< 03 Colaboradores >── 02 Cargos
     │                 │  ├──< 10 Ausentismo (colaborador × mes)
     │                 │  ├──< 11 Horas extra (colaborador × mes)
     │                 │  └──< 12 Movimientos
     │
     └──< 08 Volúmenes (unidad × actividad × mes) >── 07 Actividades >── 06 Procesos
                 └──< 09 Reprocesos (misma llave)          └── 02 Cargos (ejecutor)
04 Calendario (periodo)   05 Parámetros   13 Vacantes (unidad × cargo)   14 Escenarios
```

| ID | Estado | Descripción |
|---|---|---|
| DEC-019 | Confirmado | Las llaves de cruce oficiales son `unidad_id`, `cargo_id`, `colaborador_id`, `actividad_id`, `proceso_id` y `periodo` (AAAA-MM). Ninguna fuente se cruza por nombres. |
| DEC-020 | Confirmado | **Granularidad mínima de carga:** unidad × actividad × mes. **Granularidad mínima de disponibilidad:** colaborador × mes. Se alinea con DEC-014. |
| DEC-021 | Confirmado | Las 14 fuentes de `BANCO-VOLCAN-AZUL` son las fuentes oficiales del piloto (con DEC-004). Su formato de intercambio es CSV UTF-8. |

## 2.3 Calidad y reglas de validación

| ID | Estado | Descripción |
|---|---|---|
| DEC-022 | Confirmado | Se adoptan las reglas de validación V-01 a V-16 (`docs/metodologia_calculo.md` §5) como controles obligatorios de cada carga mensual. Un **ERROR** excluye el registro; una **ADVERTENCIA** lo incluye ajustado y lo deja registrado. |
| DEC-023 | Confirmado | Cada fuente recibe una calificación de calidad: Alta (registro de sistema o estudio de tiempos), Media (registro manual o estimación experta) o Baja (sin respaldo). Los resultados que dependen de fuentes Media o Baja se señalan en los reportes. |
| DEC-024 | Confirmado | Prioridad de métodos para el tiempo estándar: 1) estudio de tiempos; 2) registro de sistema (marca de inicio y fin); 3) muestreo de trabajo; 4) estimación experta por consenso (técnica de 3 puntos). Las estimaciones expertas se reemplazan gradualmente por mediciones. |

## 2.4 Vacíos y cómo cubrirlos

| ID | Estado | Vacío | Propuesta de recolección |
|---|---|---|---|
| PEN-005 | Pendiente | ACT-017 "Atención de quejas por redes sociales" sin tiempo estándar | Estudio de tiempos de 2 semanas en 3 agencias (≥ 30 observaciones). Responsable: Capacity Management. |
| PEN-006 | Pendiente | 16 actividades con tiempo por estimación experta | Plan de medición en 2 trimestres, priorizado por horas de carga (empezar por ACT-021 microcrédito y ACT-072 garantías). |
| SUP-003 | Supuesto | Los volúmenes registran solo trabajo **de primera vez**; los reprocesos van aparte (RN-03) | Validar con los dueños de FTE-SRC-08 y 09 que no exista doble registro. |
| SUP-004 | Supuesto | Los volúmenes manuales de las jefaturas son confiables | Muestreo trimestral contra evidencia (bitácoras) en 10 % de las unidades. |
| RSK-001 | Riesgo | El calendario de feriados es referencial (traslados y feriados locales) | Talento Humano valida el calendario oficial cada año antes del cálculo. |
| RSK-002 | Riesgo | Solo 12 meses de historia limitan el análisis de estacionalidad y tendencia | Acumular historia; las proyecciones con < 24 meses se marcan como preliminares. |
| RSK-003 | Riesgo | No se registran traslados entre unidades (cada colaborador tiene una sola asignación) | Agregar a FTE-SRC-12 el tipo TRASLADO con unidad de origen y destino (mejora propuesta). |

## 2.5 Privacidad de los datos (insumo para el Bloque 4)

| ID | Estado | Descripción |
|---|---|---|
| DEC-025 | Confirmado | Las fuentes con datos por persona (03, 10, 11 y 12) se manejan seudonimizadas. La tabla que vincula seudónimo e identidad permanece en Talento Humano y **no entra** al producto. |
| DEC-026 | Confirmado | Del ausentismo solo se usan horas por categoría; **no** se almacena el diagnóstico ni el motivo médico. |

---

## Resumen del Bloque 2

- ✅ **Confirmado (Bloque 1):** DEC-004 a DEC-018.
- ✅ **Confirmado por el usuario (2026-11-20):** DEC-019 a DEC-026 y las fichas FTE-SRC-01 a FTE-SRC-14.
- ⚠️ **Supuestos:** SUP-003 (volúmenes solo de primera vez) y SUP-004 (confiabilidad de los registros manuales).
- ⏳ **Pendiente:** PEN-004 (Comité), PEN-005 (medir ACT-017) y PEN-006 (reemplazar estimaciones expertas).
- ⚠️ **Riesgos:** RSK-001 (calendario), RSK-002 (historia corta) y RSK-003 (sin traslados).
- 🔗 **Impacto:** el Bloque 3 usará estas fuentes y llaves para cada fórmula IND-; el Bloque 4 usará DEC-025 y DEC-026 para los permisos.
- 🧾 **Decisiones que el usuario debe aprobar:** DEC-019 (llaves), DEC-020 (granularidad), DEC-022 (reglas de validación), DEC-024 (prioridad de métodos de medición) y DEC-025 (seudonimización).

**Verificación de coherencia:** no hay conflictos con el Bloque 1. Las fuentes cubren las decisiones D-1 a D-5 (DEC-010). La productividad no tiene fuente propia y se define en el Bloque 3.
