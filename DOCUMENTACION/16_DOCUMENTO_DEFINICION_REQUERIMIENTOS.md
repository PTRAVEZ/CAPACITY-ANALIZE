# DOCUMENTO DE DEFINICIÓN DE REQUERIMIENTOS — CAPACITY-ANALIZE

> **Escenario de referencia ficticio:** *Banco Volcán Azul S.A.* no existe. Datos, cifras y estructuras son sintéticos (DEC-002, DEC-004).
> **Convención:** ✅ = requisito **confirmado** (validado por el usuario en el LOOP). 💡 = **recomendación pendiente de aprobación**. Los parámetros PAR- y las metas CA- requieren aprobación formal del Comité de Capacidad antes de usarse en producción.

---

## 1. Control del documento

| Campo | Valor |
|---|---|
| Documento | Documento de Definición de Requerimientos — CAPACITY-ANALIZE |
| Versión | 1.0 (piloto) |
| Fecha | 2026-11-20 |
| Origen | LOOP de levantamiento v2.1, Bloques 1 a 4 (`DOCUMENTACION/12` a `15`) |
| Elaborado por | Consultor (asistente de IA) con validación del usuario del proyecto |
| Aprobadores sugeridos | Vicepresidencia de Operaciones y Canales; Comité de Capacidad (PEN-004); Talento Humano; Oficial de Protección de Datos |
| Estado | Bloques 1 a 4 aprobados por el usuario en el chat; quedan pendientes PEN-004 a PEN-009 |

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-11-20 | Bloque 1 aprobado |
| 0.2 | 2026-11-20 | Bloque 2 aprobado |
| 0.3 | 2026-11-20 | Bloque 3 aprobado; PAR-001, 002, 004 y 005 aprobados para el piloto |
| 1.0 | 2026-11-20 | Bloque 4 aprobado; documento consolidado |

## 2. Resumen ejecutivo

CAPACITY-ANALIZE es una solución para medir la **capacidad humana** de un banco privado: cuánto trabajo hay (carga), cuánta gente está realmente disponible y cuál es la brecha en FTE. Su fin es que las decisiones de dotación y de vacantes se tomen con datos, no con percepciones.

El piloto cubre la Vicepresidencia de Operaciones y Canales: unas 300 posiciones en 3 gerencias, 10 agencias de la Sierra, operaciones centralizadas y el centro de contacto. Con los datos ficticios, la metodología muestra un equilibrio global (utilización del 99 %), pero con **desbalances locales**. Los cajeros de la Agencia Matriz Quito están al 130 % y el Centro de Contacto al 114 %, mientras que Cámara de Compensación está al 63 %. Además se pagaron unas 14.200 horas extra y hay unos 4,6 FTE perdidos en reprocesos.

Los cuatro bloques de definición están aprobados. Antes de producción falta resolver la normativa aplicable, la retención de datos y las restricciones de infraestructura (PEN-007 a 009).

## 3. Contexto y problema

| Elemento | Definición | Estado |
|---|---|---|
| Situación actual | Cada gerencia pide dotación en su propio Excel durante el ciclo presupuestario. No hay tiempos estándar comunes. El ciclo cuesta unas 400 horas-persona (SUP-001) y una vacante tarda unos 45 días en decidirse (SUP-002). | ✅ DEC-007 (con supuestos) |
| Problema | Se decide la dotación sin una medición común de la carga y de la disponibilidad real. El resultado son sobrecargas y holguras simultáneas, horas extra sostenidas y decisiones lentas. | ✅ DEC-007 |
| Síntomas | A) dificultad para justificar dotación y vacantes; B) poca visibilidad de cómo se distribuye la carga; C) la planificación no refleja los cambios del trabajo. | ✅ DEC-003 |

## 4. Objetivos

**General:** dar al banco una medición confiable, trazable y periódica de la carga laboral, la disponibilidad y las brechas de FTE, para apoyar las decisiones de dotación (D-1 a D-5).

| ID | Objetivo específico | Indicador / criterio | Estado |
|---|---|---|---|
| OBJ-01 | Cuantificar el FTE requerido y el disponible por unidad × cargo cada mes | IND-04, IND-06; CA-01 | ✅ |
| OBJ-02 | Sustentar las vacantes y las posiciones nuevas con brechas medibles | IND-10, IND-11; CA-14 | ✅ |
| OBJ-03 | Hacer visible la distribución de la carga y las oportunidades de redistribución | IND-19, IND-21; CA-08 | ✅ |
| OBJ-04 | Cuantificar el trabajo perdido en reprocesos y sus causas | IND-12, 13, 20 | ✅ |
| OBJ-05 | Proyectar necesidades por escenarios | IND-16 | ✅ |
| OBJ-06 | Reducir el trabajo manual del ciclo de planificación | CA-09 (−50 %) | 💡 meta |

## 5. Alcance, exclusiones y estacionamiento de ideas

| Dentro del alcance (✅) | Fuera del alcance (✅) |
|---|---|
| Carga laboral, actividades, volúmenes, tiempos estándar y reprocesos | Capacidad tecnológica, infraestructura, equipamiento |
| Dotación, jornada, ausentismo, capacitación, horas extra, vacantes y rotación | Presupuesto, costos y salarios |
| FTE requerido, disponible y brechas; escenarios; redistribución | Evaluación de desempeño individual con fines disciplinarios |
| Piloto: Vicepresidencia de Operaciones y Canales (DEC-011) | Resto del banco (fase posterior, DEC-012) |

**Estacionamiento de ideas (DEC-009):** turnos diarios del centro de contacto (*workforce scheduling*), integración con la nómina para costear brechas y registro de traslados entre unidades (RSK-003).

## 6. Glosario

| ID | Término | Definición |
|---|---|---|
| GLO-01 | FTE | *Full Time Equivalent.* 1 FTE = días laborables × 8 h (≈ 2.000 h nominales al año; PAR-001). |
| GLO-02 | FTE productivo | 1 FTE × (1 − PAR-002) ≈ 1.800 h al año. |
| GLO-03 | Carga laboral | Horas requeridas = volumen × tiempo estándar + reprocesos × tiempo de reproceso. |
| GLO-04 | Disponibilidad efectiva | Horas nominales − ausencias − capacitación − tiempo no productivo. |
| GLO-05 | Utilización | Carga / horas disponibles efectivas. |
| GLO-06 | Reproceso | Unidad de trabajo que debe rehacerse; se registra aparte del volumen de primera vez. |
| GLO-07 | Tiempo estándar | Minutos por unidad de trabajo, sin reprocesos, medidos según DEC-024. |
| GLO-08 | Brecha efectiva / de dotación | IND-07 e IND-11; no se suman (RN-06). |
| GLO-09 | Seudónimo | Código que reemplaza la identidad del colaborador (COL-xxxx). |
| GLO-10 | Período cerrado | Mes aprobado y congelado (DEC-036). |

## 7. Usuarios y perfiles (matriz R/V/A/C) — ✅ DEC-015

| ID | Perfil | Registra | Valida | Aprueba | Consulta |
|---|---|---|---|---|---|
| USR-01 | Analista de Capacity Management | Fuentes de sistema, catálogo, parámetros (borrador) | Volúmenes manuales | — | Todo el piloto |
| USR-02 | Jefatura | Volúmenes manuales y reprocesos | Actividades y tiempos de su unidad | — | Su unidad |
| USR-03 | Gerente de área | — | Resultados de su gerencia | D-1, D-3 | Su gerencia |
| USR-04 | Talento Humano | Dotación, ausentismo, horas extra, movimientos, vacantes | Conciliación de dotación | D-1 (con el gerente) | Todo el piloto |
| USR-05 | Comité de Capacidad | — | — | Parámetros, catálogo, cierre del período, D-2, D-4, D-5 | Todo el piloto |
| USR-06 | Consulta ejecutiva | — | — | — | Agregado |
| USR-07 | Administrador funcional | Configuración y usuarios | — | — | — |

## 8. Procesos analizados

| Proceso apoyado | Descripción | Estado |
|---|---|---|
| Planificación anual de dotación y justificación de vacantes | Proceso principal | ✅ DEC-008 |
| Revisión trimestral de capacidad | Proceso secundario | ✅ DEC-008 |

**Procesos operativos medidos (FTE-SRC-06):** Atención en caja, Servicios al cliente, Negocios y colocación, Gestión de agencia, Dirección de gerencia, Pagos y transferencias, Gestión de cuentas y cumplimiento, Operaciones de crédito, Tarjetas y reclamos, Cámara y valores, Jefatura de departamento, y Atención telefónica y digital. En total suman 81 actividades.

**Decisiones apoyadas (✅ DEC-010):** D-1 vacantes de reemplazo · D-2 posiciones nuevas · D-3 redistribución · D-4 iniciativas contra reprocesos y de automatización · D-5 dotación del año siguiente.

## 9. Fuentes de información — ✅ DEC-021

| ID | Fuente | Dueño | Frecuencia | Calidad |
|---|---|---|---|---|
| FTE-SRC-01 | Estructura organizacional | Talento Humano | Por cambio | Alta |
| FTE-SRC-02 | Catálogo de cargos | Talento Humano | Por cambio | Alta |
| FTE-SRC-03 | Colaboradores (seudonimizados) | Talento Humano | Mensual | Alta |
| FTE-SRC-04 | Calendario laboral | Talento Humano | Anual | Media (RSK-001) |
| FTE-SRC-05 | Parámetros | Comité | Al aprobarse | — |
| FTE-SRC-06 | Procesos | Procesos y Calidad | Anual | Alta |
| FTE-SRC-07 | Actividades y tiempos estándar | Capacity | Anual | Media (PEN-005, 006) |
| FTE-SRC-08 | Volúmenes mensuales | Operaciones, Centro de Contacto, jefaturas | Mensual | Alta / Media |
| FTE-SRC-09 | Reprocesos | Jefaturas | Mensual | Media |
| FTE-SRC-10 | Ausentismo y capacitación | Talento Humano | Mensual | Alta |
| FTE-SRC-11 | Horas extra | Talento Humano | Mensual | Alta |
| FTE-SRC-12 | Movimientos | Talento Humano | Por evento | Alta |
| FTE-SRC-13 | Vacantes | Talento Humano | Por evento | Alta |
| FTE-SRC-14 | Escenarios | Planificación / Capacity | Anual | Supuesto |

## 10. Diccionario de datos preliminar

El detalle campo por campo (DAT-) está en `DATOS/BANCO-VOLCAN-AZUL/docs/diccionario_datos.md`. Llaves oficiales (✅ DEC-019): `unidad_id`, `cargo_id`, `colaborador_id`, `actividad_id`, `proceso_id` y `periodo`. Granularidad (✅ DEC-020): carga por unidad × actividad × mes; disponibilidad por colaborador × mes.

## 11. Taxonomía de tiempo y reglas contra la doble contabilización — ✅

Horas nominales → (−) ausencias → horas presentes → (−) capacitación → (−) tiempo no productivo (PAR-002) → **horas disponibles efectivas**. Reglas RN-01 a RN-07 (sección 13).

## 12. Indicadores, parámetros y supuestos

**Indicadores (✅ DEC-029):** IND-01 a IND-21. Las fichas completas están en `14_BLOQUE3_INDICADORES_Y_FORMULAS.md`. Todos están implementados en el demostrador, incluidos IND-17 a IND-20.

| Parámetro | Valor | Estado |
|---|---|---|
| PAR-001 Jornada diaria | 8 h | ✅ Aprobado (piloto) |
| PAR-002 Factor no productivo | 10 % | ✅ Aprobado (piloto) |
| PAR-003 Vacaciones anuales (solo para generar datos) | 15 días | 💡 Supuesto |
| PAR-004 Umbral de sobrecarga | 105 % | ✅ Aprobado (piloto) |
| PAR-005 Umbral de holgura | 80 % | ✅ Aprobado (piloto) |
| PAR-006 Agregación mínima | 3 personas | ✅ (Bloque 4) |

**Supuestos vigentes:** SUP-001 (≈ 400 h-persona por ciclo), SUP-002 (≈ 45 días por vacante), SUP-003 (volumen solo de primera vez), SUP-004 (registros manuales confiables), SUP-005 (horas productivas de 2027), SUP-006 (base legal), SUP-007 (el prototipo no es la tecnología final).

## 13. Reglas de negocio

| ID | Regla | Estado |
|---|---|---|
| RN-01 | Las ausencias solo reducen la capacidad disponible | ✅ |
| RN-02 | La capacitación se toma del dato real y queda fuera de PAR-002 | ✅ |
| RN-03 | Los reprocesos se registran aparte; no se aplica además un factor de reproceso | ✅ |
| RN-04 | Una actividad pertenece a un solo proceso y la ejecuta un solo cargo | ✅ |
| RN-05 | Las horas extra no aumentan la capacidad | ✅ |
| RN-06 | La brecha efectiva y la brecha de dotación no se suman | ✅ |
| RN-07 | Ausencias + capacitación ≤ horas nominales (ajuste y advertencia V-11) | ✅ |
| RN-08 | Un período cerrado no se modifica; las correcciones generan una nueva versión | ✅ DEC-036 |
| RN-09 | Las recomendaciones del sistema (redistribución, escenarios) no son decisiones automáticas | ✅ DEC-010 |
| RN-10 | No se reportan grupos de menos de PAR-006 personas | ✅ DEC-031 |
| RN-11 | Quien registra un dato no lo aprueba | ✅ DEC-033 |

## 14. Requerimientos funcionales

Prioridad MoSCoW: **D** = Debe · **Db** = Debería · **P** = Podría.

| ID | Requerimiento | Prioridad | Estado | Responsable de validación | Criterio de aceptación | Trazabilidad |
|---|---|---|---|---|---|---|
| RF-01 | Importar las 14 fuentes en CSV o Excel con plantilla y versión | D | ✅ | USR-01 | Las 14 fuentes se cargan sin errores de formato | DEC-021, DEC-041 |
| RF-02 | Validar automáticamente cada carga con las reglas V-01 a V-16 y emitir un reporte de calidad | D | ✅ | USR-01 | Detecta 7 de 7 anomalías sembradas | DEC-022, CA-05 |
| RF-03 | Conciliar la dotación (inicial + ingresos − salidas = dotación a la fecha de corte) | D | ✅ | USR-04 | 100 % conciliado | CA-02 |
| RF-04 | Calcular la disponibilidad por colaborador-mes según la taxonomía de tiempo | D | ✅ | USR-01 | Identidad IND-06 = IND-05 × (1 − IND-09) | RN-01, RN-02, CA-03 |
| RF-05 | Calcular la carga por unidad × cargo × actividad × mes, incluidos los reprocesos | D | ✅ | USR-01 | Diferencia 0 contra un recálculo independiente | IND-03, CA-01 |
| RF-06 | Calcular IND-04 a IND-15 por mes y por año, para cada nivel organizacional | D | ✅ | USR-03 | La suma por gerencia es igual a la suma por unidad × cargo | CA-06 |
| RF-07 | Clasificar cada unidad × cargo en Sobrecarga, Equilibrio u Holgura | D | ✅ | USR-05 | Usa PAR-004 y PAR-005 vigentes | IND-15 |
| RF-08 | Generar el sustento de vacante (brechas, tendencia, horas extra) de una unidad × cargo | D | ✅ | USR-03 / USR-04 | Reporte con IND-07, 10, 11 y 14 de 12 meses | D-1, CA-14 |
| RF-09 | Identificar oportunidades de redistribución en múltiplos de 0,5 FTE | Db | ✅ | USR-03 | Marcadas como "a evaluar" | IND-21, RN-09 |
| RF-10 | Calcular el índice estacional por proceso | Db | ✅ | USR-01 | Promedio = 1 por proceso | IND-18 |
| RF-11 | Calcular la dispersión de la utilización entre unidades del mismo cargo | Db | ✅ | USR-03 | Solo grupos de ≥ 3 unidades | IND-19 |
| RF-12 | Calcular la productividad por FTE frente a la mediana de la actividad | Db | ✅ | USR-03 | Excluye grupos menores que PAR-006 | IND-17, RN-10 |
| RF-13 | Pareto de causas de reproceso y FTE liberable | D | ✅ | USR-05 | % acumulado = 100 % | IND-12, 13, 20 |
| RF-14 | Crear y comparar escenarios con ajustes de volumen y tiempo por ámbito | D | ✅ | USR-05 | Reproduce los 4 escenarios de 2027 | IND-16, DEC-027 |
| RF-15 | Administrar el catálogo de actividades y tiempos con historial y método de medición | D | ✅ | USR-01 / USR-05 | Cada cambio queda versionado y aprobado | DEC-024 |
| RF-16 | Administrar los parámetros con estado (Supuesto, Propuesto, Aprobado) y su aprobador | D | ✅ | USR-05 | Solo USR-05 cambia el estado a Aprobado | PAR-, DEC-033 |
| RF-17 | Flujo del período: Abierto → Cargado → Validado → Revisado → Aprobado → Cerrado | D | ✅ | USR-05 | No se puede saltar estados | DEC-036, RN-08 |
| RF-18 | Reproducir un período cerrado con sus insumos, parámetros y versión del motor | D | ✅ | USR-01 | Diferencia 0 | DEC-037, CA-13 |
| RF-19 | Tableros: ejecutivo, de gerencia y ficha de unidad | D | ✅ | USR-03 / USR-05 | Muestran los indicadores de 3.4 según el perfil | Bloque 3 §3.4 |
| RF-20 | Exportar resultados a Excel | D | ✅ | USR-01 | Todas las tablas del período | DEC-041 |
| RF-21 | Registrar volúmenes manuales y reprocesos por jefatura hasta el cierre | D | ✅ | USR-02 | Bloqueado después del cierre | DEC-017 |
| RF-22 | Trazar cada indicador publicado hasta sus filas de origen | Db | ✅ | USR-01 | 100 % de una muestra de 20 | CA-07 |
| RF-23 | Alertar las actividades sin tiempo estándar o con estimación experta | Db | ✅ | USR-01 | Lista con PEN-005 y 006 | DEC-024 |
| RF-24 | Registrar traslados entre unidades | P | 💡 | USR-04 | El tipo TRASLADO se incluye en FTE-SRC-12 | RSK-003 |

## 15. Requerimientos no funcionales

| ID | Requerimiento | Prioridad | Estado | Criterio de aceptación | Trazabilidad |
|---|---|---|---|---|---|
| RNF-01 | Aplicación web por navegador, sin instalación | D | ✅ | Funciona en los navegadores corporativos | DEC-039 |
| RNF-02 | Autenticación con la identidad institucional (inicio de sesión único) y perfiles por grupos del directorio | D | ✅ | Sin usuarios locales en producción | DEC-040 |
| RNF-03 | Control de acceso por perfil y alcance de datos | D | ✅ | 0 accesos indebidos en las pruebas | DEC-033, CA-12 |
| RNF-04 | Bitácora de auditoría inmutable | D | ✅ | Cada cambio registra quién, cuándo, valor anterior, valor nuevo y motivo | DEC-035 |
| RNF-05 | Datos seudonimizados; sin nombres, cédulas, salarios ni diagnósticos | D | ✅ | Revisión del modelo de datos | DEC-025, 026, 030 |
| RNF-06 | Se registran las consultas del detalle por persona | D | ✅ | Registro de cada consulta | DEC-038 |
| RNF-07 | Rendimiento: el cálculo mensual del piloto termina en < 5 min | Db | 💡 | Medido con datos del piloto | — |
| RNF-08 | Resultados disponibles el día hábil 10 | D | ✅ | CA-10 | DEC-018 |
| RNF-09 | Usabilidad SUS ≥ 70 | Db | ✅ | CA-11 | — |
| RNF-10 | Base de datos relacional con versionado de períodos | D | ✅ | Revisión de arquitectura | DEC-042 |
| RNF-11 | Pruebas automáticas de los cálculos en cada cambio | D | ✅ | CA-01 a 06 en verde | Suite `tests/` |
| RNF-12 | Cumplir la normativa de datos personales y de seguridad aplicable | D | 💡 | Visto bueno de Legal y Cumplimiento | PEN-007, PEN-008 |

## 16. Matriz de permisos — ✅ DEC-033

Ver la tabla completa en `15_BLOQUE4…` §4.4. Resumen: USR-01 opera los datos y el cálculo; USR-02 registra y valida su unidad; USR-03 valida su gerencia; USR-04 opera los datos de personas y la conciliación; USR-05 aprueba parámetros, catálogo y cierre; USR-06 solo consulta agregados; USR-07 solo configura. Segregación de funciones: RN-11 y DEC-034.

## 17. Privacidad, seguridad y auditoría — ✅ DEC-030 a 038

Seudonimización; agregación mínima de 3 personas; detalle por persona solo para USR-01 y USR-04; ausencias de salud tratadas como sensibles y sin diagnóstico; bitácora inmutable; registro de consultas; cierre y congelamiento de períodos. **Pendiente:** normativa aplicable (PEN-007) y retención (PEN-008).

## 18. Arquitectura funcional propuesta (sin tecnología)

```
[Fuentes CSV/Excel] → (1) Ingesta y plantillas → (2) Validación V-01..V-16 + conciliación
      → (3) Motor de disponibilidad (colaborador-mes) ─┐
      → (4) Motor de carga (unidad × actividad × mes) ─┴→ (5) Motor de capacidad y brechas
      → (6) Análisis: redistribución, estacionalidad, dispersión, productividad, Pareto
      → (7) Escenarios → (8) Tableros, reportes y exportación
Transversales: (9) Catálogos y parámetros versionados · (10) Flujo y cierre de períodos
               (11) Seguridad, perfiles y bitácora de auditoría
```

El demostrador `DATOS/BANCO-VOLCAN-AZUL/src/capacity_analize.py` implementa los módulos 2 a 8 en modo de lotes, para validar la metodología (SUP-007). La tecnología de producción se decide cuando se resuelva PEN-009 (💡).

## 19. Criterios de aceptación — ✅ DEC-043 (metas 💡 hasta que las apruebe el Comité)

| ID | Criterio | Meta | Verificación |
|---|---|---|---|
| CA-01 | Exactitud de la carga | Diferencia 0 | Automática ✔ |
| CA-02 | Conciliación de dotación | 100 % | Automática ✔ |
| CA-03 | Sin doble conteo de ausencias | Identidad exacta | Automática ✔ |
| CA-04 | Integridad de las horas | 100 % | Automática ✔ |
| CA-05 | Detección de anomalías | 7 de 7 | Automática ✔ |
| CA-06 | Coherencia de agregación | Diferencia 0 | Automática ✔ |
| CA-07 | Trazabilidad | 100 % de una muestra de 20 | Manual |
| CA-08 | Identificación de brechas | ≥ 95 % de coincidencia con el analista | Manual |
| CA-09 | Reducción del trabajo manual | −50 % frente a SUP-001 | Piloto |
| CA-10 | Oportunidad | Día hábil 10 | Piloto |
| CA-11 | Usabilidad | SUS ≥ 70 | Encuesta |
| CA-12 | Permisos | 0 accesos indebidos | Prueba de seguridad |
| CA-13 | Reproducibilidad | Diferencia 0 | Automática (fase 2) |
| CA-14 | Decisión de vacantes | ≤ 20 días | Piloto |

Además, las pruebas automáticas cubren IND-17 a IND-20 (`test_ind17` a `test_ind20`).

## 20. Matriz de trazabilidad

| Problema / síntoma | Decisión | Requerimientos | Indicadores | Fuentes | Criterios |
|---|---|---|---|---|---|
| A · Justificar dotación y vacantes | D-1, D-2 | RF-04 a 08, RF-17 | IND-04 a 11, 14 | 03, 07, 08, 10, 11 | CA-01 a 04, CA-14 |
| B · Visibilidad de la distribución de la carga | D-3 | RF-07, 09, 11, 12, 19 | IND-15, 17, 19, 21 | 01, 03, 08 | CA-06, CA-08 |
| C · La planificación no refleja los cambios del trabajo | D-5 | RF-10, 14, 15 | IND-16, 18 | 07, 08, 14 | CA-13 |
| Trabajo perdido en reprocesos | D-4 | RF-13 | IND-12, 13, 20 | 09 | CA-01 |
| Confianza en los datos | Todas | RF-01 a 03, 18, 22 | — | Todas | CA-02, 05, 07 |
| Privacidad | Todas | RNF-03 a 06, 12 | — | 03, 10, 11, 12 | CA-12 |

## 21. Riesgos y dependencias

| ID | Riesgo / dependencia | Impacto | Mitigación |
|---|---|---|---|
| RSK-001 | Calendario de feriados referencial | Medio | Talento Humano valida el calendario cada año |
| RSK-002 | Solo 12 meses de historia | Medio | Las proyecciones se marcan como preliminares hasta tener ≥ 24 meses |
| RSK-003 | Sin registro de traslados | Bajo | RF-24 |
| RSK-004 | 16 tiempos por estimación experta | Alto (exactitud del FTE) | Plan de medición PEN-006 |
| RSK-005 | Resistencia de las jefaturas a registrar datos | Medio | Plantillas simples y valor visible (ficha de unidad) |
| RSK-006 | Uso de la productividad como evaluación individual | Alto (clima laboral) | RN-10; IND-17 solo agregado y como "señal a revisar" |
| DEP-01 | Restricciones de infraestructura | Bloquea la tecnología | PEN-009 |
| DEP-02 | Normativa de datos personales | Bloquea producción | PEN-007 |

## 22. Decisiones pendientes

| ID | Pendiente | Responsable sugerido | Fecha sugerida |
|---|---|---|---|
| PEN-004 | Existencia e integración del Comité de Capacidad | Vicepresidencia de Operaciones y Canales | Antes de la fase 1 |
| PEN-005 | Medir ACT-017 (quejas por redes sociales) | Capacity Management | Fase 1 |
| PEN-006 | Reemplazar 16 estimaciones expertas por mediciones | Capacity Management | Fases 1 y 2 |
| PEN-007 | Normativa aplicable y evaluación de impacto | Oficial de Protección de Datos / Legal | Antes de la fase 2 |
| PEN-008 | Clasificación y retención de los datos | Seguridad de la Información | Antes de la fase 2 |
| PEN-009 | Restricciones de infraestructura y tecnología | Tecnología / Arquitectura | Antes de la fase 2 |

## 23. Plan de implementación por fases

| Fase | Objetivo | Entregables | Criterios de salida |
|---|---|---|---|
| 0 · Demostrador metodológico (**completada**) | Validar fórmulas y datos con el banco ficticio | Generador, motor IND-01 a 21, 10 pruebas, documentos 12 a 16 | CA-01 a 06 en verde; Bloques 1 a 4 aprobados |
| 1 · Piloto con datos reales (≈ 3 meses) | Ejecutar la metodología con fuentes reales del piloto, en modo de lotes | Fuentes reales mapeadas, mediciones PEN-005 y 006 iniciadas, Comité constituido, primer cierre mensual | CA-07, CA-08 y CA-10; Comité aprueba el primer período |
| 2 · Producto mínimo viable (≈ 4 meses) | Aplicación web con seguridad y flujo de períodos | RF-01 a 23, RNF-01 a 11, tableros, bitácora | CA-11 a CA-13; visto bueno de Legal y Seguridad (PEN-007, 008) |
| 3 · Ampliación y operación continua | Resto del banco y mejora continua | Nuevas vicepresidencias, RF-24, historia ≥ 24 meses | CA-09 y CA-14 medidos un año después |

---

*Fin del documento. Los requisitos marcados ✅ fueron validados por el usuario en el LOOP; los marcados 💡 son recomendaciones pendientes de aprobación.*
