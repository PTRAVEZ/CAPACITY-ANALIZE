# 12 · LOOP v2.1 — Bloque 1: Proceso, decisión y usuarios

> ✅ **Bloque aprobado por el usuario en el chat (2026-11-20).** DEC-004 a DEC-018 pasan a *Confirmado*; los SUP- siguen como supuestos y PEN-004 sigue pendiente.

> **Modo de trabajo autorizado por el usuario (chat, 2026-11-20):** como el banco es **ficticio** (*Banco Volcán Azul S.A.*), el consultor propone las respuestas de cada tema en lugar de esperar una respuesta del usuario.
> Por eso **todo lo de este bloque está en estado _Propuesto_ o _Supuesto_**, salvo lo que ya estaba confirmado (DEC-001 a DEC-003). Las cifras provienen de los datos sintéticos de `DATOS/BANCO-VOLCAN-AZUL/` y son **ilustrativas**.

## 0. Resolución de PEN-002 y PEN-003

| ID | Estado | Descripción |
|---|---|---|
| DEC-004 | Confirmado | El escenario de referencia del LOOP es **Banco Volcán Azul S.A.**, tal como lo describe el Anexo v2.1: piloto de 300 posiciones, 3 gerencias, 10 agencias de la Sierra, centro de contacto y período base 2025-11 a 2026-10. Su paquete completo se incorpora en `DATOS/BANCO-VOLCAN-AZUL/`. |
| DEC-005 | Confirmado | El kit previo (`DATOS/CAPACITY-ANALIZE/`, "Banco Andino del Ecuador": 180 colaboradores y 8 agencias) se conserva como **referencia histórica**. No se borra ni se mezcla con el escenario de referencia. |
| DEC-006 | Confirmado | Las rutas citadas por el Anexo v2.1 (`docs/diccionario_datos.md`, `docs/metodologia_calculo.md`, `docs/anomalias_sembradas.md`, `src/capacity_analize.py`, `reports/resumen_resultados.md`, `data/input/`, `data/output/`) son relativas a `DATOS/BANCO-VOLCAN-AZUL/` y ahora existen. |
| PEN-002 | Resuelto → DEC-004, DEC-005 | Discrepancia de escenario. |
| PEN-003 | Resuelto → DEC-006 | Archivos de referencia del Anexo. Las anomalías sembradas quedan documentadas en `docs/anomalias_sembradas.md` y las detecta el motor (reglas V-02, V-04, V-07 a V-11). |

---

## Tema 1.1 · Problema organizacional y situación actual (cierra PEN-001)

**Situación actual propuesta (ficticia):**

| Aspecto | Cómo ocurre hoy |
|---|---|
| Método | En el ciclo presupuestario (septiembre a noviembre), cada gerencia pide dotación en su propia hoja de Excel. Talento Humano consolida las solicitudes y las presenta a la Vicepresidencia. No existen tiempos estándar comunes: la justificación se basa en la percepción de carga, en las horas extra y en comparaciones con el año anterior. |
| Esfuerzo | Unas 6 semanas por ciclo: 2 analistas de Talento Humano a tiempo parcial y unas 8 horas de cada una de las ~16 jefaturas del piloto. En total, ≈ 400 horas-persona al año (SUP-001). |
| Fallas e impactos | (a) Las vacantes se aprueban sin un sustento cuantitativo y la decisión toma ≈ 45 días (SUP-002). (b) Hay sobrecarga persistente en unidades como Cajeros de Agencia Matriz Quito (utilización ≈ 130 %) y el Centro de Contacto (≈ 114 %), mientras otras tienen holgura, como Cámara de Compensación (≈ 63 %). (c) En el período base se pagaron ≈ 14.200 horas extra en el piloto. (d) No se sabe cuánto trabajo se pierde en reprocesos (≈ 8.200 h ≈ 4,6 FTE según los datos sintéticos). |

| ID | Estado | Descripción |
|---|---|---|
| DEC-007 | Confirmado | **Problema:** el banco decide su dotación sin una medición común de la carga de trabajo y de la disponibilidad real. Eso produce sobrecargas y holguras simultáneas, horas extra sostenidas y decisiones de vacantes lentas y difíciles de justificar. Desarrolla los síntomas A, B y C de DEC-003. |
| SUP-001 | Supuesto | Esfuerzo actual del ciclo ≈ 400 horas-persona al año. Es la línea base para medir la reducción de trabajo manual (CA- del Bloque 4). |
| SUP-002 | Supuesto | Tiempo actual de decisión de una vacante ≈ 45 días calendario. |
| PEN-001 | Resuelto → DEC-007 | |

## Tema 1.2 · Proceso que apoya el producto

| ID | Estado | Descripción |
|---|---|---|
| DEC-008 | Confirmado | **Proceso principal:** *Planificación anual de dotación y justificación de vacantes*. **Proceso secundario:** *Revisión trimestral de capacidad*, que detecta sobrecargas y holguras y propone redistribución y acciones sobre los reprocesos. |
| DEC-009 | Confirmado | Fuera del proceso en esta versión: evaluación de desempeño individual, cálculo de nómina, turnos diarios del centro de contacto (*workforce scheduling*) y presupuesto de costos. Quedan en el **Estacionamiento de ideas**. |

## Tema 1.3 · Decisiones que permitirá tomar

| Código | Decisión | Quién decide | Frecuencia | Indicadores que la sustentan |
|---|---|---|---|---|
| D-1 | Aprobar, rechazar o diferir vacantes de reemplazo | Gerente de área + Talento Humano | Por evento | Brecha efectiva y de dotación de la unidad y el cargo, y tendencia de utilización |
| D-2 | Aprobar nuevas posiciones | Comité de Capacidad | Trimestral | FTE requerido para dotación, meses en sobrecarga, horas extra |
| D-3 | Redistribuir personal entre unidades del mismo cargo | Gerente de área | Trimestral | Oportunidades de redistribución |
| D-4 | Priorizar iniciativas contra reprocesos o de automatización | Comité de Capacidad | Semestral | Horas y FTE liberables por proceso y causa; escenarios |
| D-5 | Fijar la dotación objetivo del año siguiente | Vicepresidencia + Comité | Anual | Escenarios con FTE requerido para dotación frente a FTE contractual |

| ID | Estado | Descripción |
|---|---|---|
| DEC-010 | Confirmado | El producto apoya las decisiones D-1 a D-5. Las recomendaciones del sistema **no** son decisiones automáticas: siempre requieren aprobación humana. |

## Tema 1.4 · Alcance piloto frente al total

| ID | Estado | Descripción |
|---|---|---|
| DEC-011 | Confirmado | **Piloto:** Vicepresidencia de Operaciones y Canales, con 3 gerencias (Operaciones Centralizadas, Red de Agencias Sierra y Banca Telefónica y Digital), 16 unidades y ≈ 300 posiciones. |
| DEC-012 | Confirmado | **Ampliación posterior:** resto de la red de agencias y demás vicepresidencias, una vez que el piloto cumpla sus criterios de aceptación (Bloque 4). |

## Tema 1.5 · Niveles organizacionales

| ID | Estado | Descripción |
|---|---|---|
| DEC-013 | Confirmado | Jerarquía: Banco → Dirección (Vicepresidencia) → Gerencia → Departamento o Agencia → Proceso → Actividad → Cargo. |
| DEC-014 | Confirmado | **Nivel mínimo de cálculo:** unidad × cargo × actividad × mes. **Nivel mínimo de reporte:** grupos de al menos 3 personas (PAR-006); los grupos menores se muestran agregados al nivel superior. |

## Tema 1.6 · Perfiles de usuario (R = registra, V = valida, A = aprueba, C = consulta)

| ID | Perfil | R | V | A | C | Información que necesita |
|---|---|---|---|---|---|---|
| USR-01 | Analista de Capacity Management | ✔ | | | ✔ | Todas las fuentes, la validación de datos, los cálculos y los escenarios |
| USR-02 | Jefatura de departamento o agencia | ✔ (volúmenes manuales) | ✔ (actividades y tiempos de su unidad) | | ✔ (su unidad) | Carga, utilización y brecha de su unidad; reprocesos |
| USR-03 | Gerente de área | | ✔ (resultados de su gerencia) | ✔ (D-1, D-3) | ✔ (su gerencia) | Comparativo de unidades, redistribución, horas extra |
| USR-04 | Talento Humano | ✔ (dotación, ausentismo, horas extra, movimientos, vacantes) | ✔ (conciliación de dotación) | ✔ (D-1, junto con el gerente) | ✔ | Dotación, indisponibilidad, vacantes |
| USR-05 | Comité de Capacidad | | | ✔ (parámetros, resultados, D-2, D-4, D-5) | ✔ | Resumen ejecutivo, escenarios, parámetros PAR- |
| USR-06 | Consulta ejecutiva (Vicepresidencia, Planificación) | | | | ✔ (agregado) | Indicadores globales y escenarios |
| USR-07 | Administrador funcional | Configuración | | | | Usuarios, perfiles, catálogos, períodos |

| ID | Estado | Descripción |
|---|---|---|
| DEC-015 | Confirmado | Se adoptan los perfiles USR-01 a USR-07 con la matriz R/V/A/C anterior. El detalle de permisos se completa en el Bloque 4 (tema 4.4). |

## Tema 1.7 · Dueños de la información y aprobadores

| Información | Dueño propuesto | Fuente en `BANCO-VOLCAN-AZUL` |
|---|---|---|
| Estructura, cargos, colaboradores, ausentismo, horas extra, movimientos, vacantes | Talento Humano | 01, 02, 03, 10, 11, 12, 13 |
| Calendario laboral | Talento Humano | 04 |
| Procesos | Procesos y Calidad | 06 |
| Catálogo de actividades y tiempos estándar | Capacity Management (validado por las jefaturas) | 07 |
| Volúmenes transaccionales | Gerencia de Operaciones (extracción del core) y Centro de Contacto (plataforma) | 08 |
| Reprocesos | Jefaturas de cada unidad | 09 |
| Parámetros y escenarios | Comité de Capacidad | 05, 14 |

| ID | Estado | Descripción |
|---|---|---|
| DEC-016 | Confirmado | Los dueños de la información son los de la tabla anterior. Los **resultados** del período los aprueba el Comité de Capacidad, después de la validación del gerente de cada área. |
| PEN-004 | Pendiente | Confirmar si el Comité de Capacidad existe o hay que crearlo, y quiénes lo integran. Responsable sugerido: Vicepresidencia de Operaciones y Canales. |

## Tema 1.8 · Modelo de levantamiento

| ID | Estado | Descripción |
|---|---|---|
| DEC-017 | Confirmado | **Modelo mixto.** Capacity Management carga centralizadamente las fuentes de sistema (nómina, core, centro de contacto). Las jefaturas registran los volúmenes manuales y los reprocesos, y validan una vez al año el catálogo de actividades y los tiempos de su unidad. |

## Tema 1.9 · Periodicidad

| ID | Estado | Descripción |
|---|---|---|
| DEC-018 | Confirmado | **Mensual:** carga de datos y cálculo hasta el día hábil 10 del mes siguiente. **Trimestral:** revisión en el Comité de Capacidad (decisiones D-2 y D-3). **Anual:** actualización de tiempos estándar o cuando cambie un proceso, y ciclo de planificación de dotación en septiembre (D-5). Al aprobarse, cada período se **cierra y congela** para que sus resultados se puedan reproducir. |

---

## Resumen del Bloque 1

- ✅ **Confirmado (anterior):** DEC-001, DEC-002, DEC-003.
- ✅ **Confirmado por el usuario (2026-11-20):** DEC-004 a DEC-018 y los perfiles USR-01 a USR-07.
- ⚠️ **Supuestos vigentes:** SUP-001 (≈ 400 horas-persona por ciclo) y SUP-002 (≈ 45 días por vacante).
- ⏳ **Pendiente:** PEN-004 (existencia e integración del Comité de Capacidad).
- ❌ **Descartado / Estacionamiento:** evaluación individual, nómina, turnos diarios y costos (DEC-009).
- 🔗 **Impacto en bloques siguientes:** el Bloque 2 usa las 14 fuentes de `BANCO-VOLCAN-AZUL` y sus dueños (DEC-016); el Bloque 3 debe sustentar las decisiones D-1 a D-5; el Bloque 4 debe traducir la matriz R/V/A/C en permisos.
- 🧾 **Decisiones que el usuario debe aprobar:** DEC-004/005 (escenario de referencia), DEC-007 (problema), DEC-008 (proceso), DEC-011 (alcance del piloto), DEC-017 (modelo mixto) y DEC-018 (periodicidad).

**Verificación de coherencia:** no se detectan conflictos con DEC-001 a DEC-003 ni con el límite de alcance del LOOP v2. El piloto coincide con el Anexo v2.1 (DEC-004).
