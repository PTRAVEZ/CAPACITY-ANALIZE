# 00. Estado del proyecto

**Estado general:** EN ANÁLISIS
**Fase actual:** LOOP v2.1 · Bloque 1 · Tema 1.1
**Última actualización:** 2026-11-20

## Tablero

| Área | Estado | Evidencia / condición |
|---|---|---|
| Reconstrucción histórica accesible | APROBADO | Sesiones, fuentes accesibles y texto v2.1 pegado por el usuario revisados; límites documentados en `01` y diferencias del Anexo en `11`. |
| Auditoría de repositorio y kit | EN VALIDACIÓN | Se identificó el paquete sintético bajo `DATOS/CAPACITY-ANALIZE/`; ver `02`. El directorio `DATOS/` estaba sin seguimiento por Git y se preserva. |
| Propósito y alcance general | APROBADO | El usuario confirmó análisis de capacidad humana en banca privada y que los tres síntomas identificados coexisten; ver `11`. |
| Definición funcional detallada | EN ANÁLISIS | Bloque 1, Tema 1.1 abierto. Falta describir el proceso actual, esfuerzo y fallas concretas antes de avanzar a 1.2. |
| Datos / diccionario | PENDIENTE DE DEFINICIÓN | Hay 15 CSV y un libro Excel sintéticos; definiciones de columnas, relaciones y calidad deben validarse. |
| Reglas de negocio y fórmulas | PENDIENTE DE DEFINICIÓN | Fórmulas y parámetros del kit son iniciales/ilustrativos; `RN-001` permanece Propuesto. |
| Arquitectura de producción y despliegue | PENDIENTE DE DEFINICIÓN | Hay un prototipo Streamlit existente, pero la tecnología, operación, permisos y despliegue no han sido aprobados. Completar Bloque 4 antes de seleccionarlos. |
| Implementación de negocio | NO INICIADO | No iniciar nuevas funciones de negocio hasta las puertas de definición y aceptación. El código de demostración no equivale a producto aprobado. |
| QA y validación integral | NO INICIADO | La suite existe, pero no se ejecutó en este ciclo. |
| Documentación de integración | EN VALIDACIÓN | `11` integra el LOOP v2.1 y compara el Anexo con el kit; falta resolver `PEN-002` y `PEN-003`. |

## Registro del LOOP v2.1

| ID | Estado | Descripción breve |
|---|---|---|
| DEC-001 | Confirmado | Producto de análisis de capacidad humana para un banco privado, dentro del alcance del LOOP v2. |
| DEC-002 | Confirmado | El usuario confirmó que los datos de `DATOS/` son sintéticos y no identifican personas reales. |
| DEC-003 | Confirmado | Coexisten los síntomas A, B y C: justificar dotación/vacantes; visibilidad de distribución de carga; planificación que no refleja bien cambios del trabajo. |
| PEN-001 | Pendiente | Cómo se atienden hoy estos problemas, esfuerzo y fallas/impacto concretos; responsable sugerido: dueño del proceso / usuario. |
| RN-001 | Propuesto | Las fórmulas del kit no son reglas oficiales aprobadas; requieren validación y aprobador. |
| RSK-001 | Pendiente de validación | Hay 110 registros en volúmenes y 110 en reprocesos sin correspondencia con agencias bajo las relaciones inferidas. Confirmar claves y granularidad antes de tratarlos como errores definitivos. |
| PEN-002 | Pendiente | Resolver la discrepancia entre el escenario ficticio del Anexo v2.1 y el paquete actual (nombre, tamaño de dotación y número de agencias). |
| PEN-003 | Pendiente | Confirmar si los archivos existentes sustituyen las rutas de diccionario, metodología, código, reportes y anomalías citadas por el Anexo v2.1. |

## Pruebas

- Ejecutadas en este ciclo: ninguna.
- Aprobadas: ninguna.
- Fallidas: ninguna registrada.
- Existe `DATOS/CAPACITY-ANALIZE/tests/test_calculations.py`; sus casos y ejecución se documentarán al llegar a la fase de validación.

## Bloqueos e incidencias

1. **Definición funcional:** falta completar y validar el Tema 1.1. No avanzar a 1.2 sin validar el registro o indicar `CONTINUAR CON PENDIENTE`.
2. **Anexo v2.1:** ya fue recibido en el chat. Sus cifras y rutas no coinciden con todos los archivos disponibles; `PEN-002` y `PEN-003` requieren aclaración.
3. **Datos y reglas:** el diccionario y las fórmulas del kit son preliminares; no constituyen aprobación funcional ni regulatoria.

## Próximas actividades

1. Resolver `PEN-002` y `PEN-003` sobre el escenario y las referencias de archivos del anexo.
2. Completar el Tema 1.1 describiendo el método actual, esfuerzo y fallas/impactos; registrar propuesta y esperar validación.
3. Al cerrar 1.1, seguir el orden del Bloque 1 y conservar trazabilidad entre decisiones, fuentes, datos, reglas, indicadores y criterios.
4. No iniciar implementación nueva hasta satisfacer las puertas funcionales y técnicas correspondientes.

## Actualización 2026-11-20 — Integración del Anexo v2.1 y Bloque 1

- Se incorporó el paquete del escenario **Banco Volcán Azul S.A.** en `DATOS/BANCO-VOLCAN-AZUL/` (generador de datos, motor de cálculo, pruebas y documentación del Anexo v2.1).
- `PEN-002` y `PEN-003` quedan resueltos con propuestas DEC-004 a DEC-006 (ver `12_BLOQUE1_PROCESO_DECISION_USUARIOS.md`).
- El usuario autorizó que el consultor proponga las respuestas, porque el banco es ficticio. Bloque 1 (temas 1.1 a 1.9) queda **completo en estado Propuesto**, pendiente de validación del usuario. `PEN-001` resuelto → DEC-007. Nuevo pendiente: `PEN-004` (Comité de Capacidad).
- Próximo paso: Bloque 2 (Datos y fuentes), usando las 14 fuentes de `DATOS/BANCO-VOLCAN-AZUL/data/input/`.

## Actualización 2026-11-20 — Bloque 1 aprobado y Bloque 2 propuesto

- El usuario **aprobó el Bloque 1**: DEC-004 a DEC-018 pasan a *Confirmado*.
- Bloque 2 (Datos y fuentes) completo en estado *Propuesto*: fichas FTE-SRC-01 a 14, llaves de cruce, reglas de calidad V-01 a V-16, vacíos y riesgos (ver `13_BLOQUE2_DATOS_Y_FUENTES.md`).
- Nuevos pendientes: PEN-005 (medir ACT-017) y PEN-006 (reemplazar estimaciones expertas). Riesgos: RSK-001 a RSK-003.
- Próximo paso: validación del Bloque 2 por el usuario y luego el Bloque 3 (indicadores y fórmulas).

## Actualización 2026-11-20 — Bloque 2 aprobado y Bloque 3 propuesto

- El usuario **aprobó el Bloque 2**: DEC-019 a DEC-026 pasan a *Confirmado*.
- Bloque 3 (Indicadores y fórmulas) completo en estado *Propuesto*: taxonomía de tiempo, RN-01 a RN-07, fichas IND-01 a IND-21, escenarios y salidas (ver `14_BLOQUE3_INDICADORES_Y_FORMULAS.md`).
- IND-17 a IND-20 (productividad, estacionalidad, dispersión y Pareto de causas) quedan pendientes de programar en el demostrador.
- Próximo paso: validación del Bloque 3 por el usuario y luego el Bloque 4 (privacidad, accesos, despliegue y criterios de éxito).

## Actualización 2026-11-20 — Bloque 3 aprobado y Bloque 4 propuesto

- El usuario **aprobó el Bloque 3**: RN-01 a RN-07, IND-01 a IND-21 y DEC-027 a DEC-029 pasan a *Confirmado*; PAR-001, 002, 004 y 005 quedan aprobados para el piloto (actualizado en `05_parametros.csv`).
- Bloque 4 (Privacidad, accesos, despliegue y criterios de éxito) completo en estado *Propuesto*: seudonimización y agregación mínima, matriz de permisos, auditoría y cierre de períodos, condiciones de operación y CA-01 a CA-14 (ver `15_BLOQUE4_PRIVACIDAD_ACCESOS_DESPLIEGUE_EXITO.md`).
- Nuevos pendientes: PEN-007 (normativa), PEN-008 (retención) y PEN-009 (infraestructura; condiciona la elección de tecnología).
- Próximo paso: validación del Bloque 4 y generación del Documento de Definición de Requerimientos.

## Actualización 2026-11-20 — LOOP completo y Documento de Definición de Requerimientos

- El usuario **aprobó el Bloque 4**: DEC-030 a DEC-043, la matriz de permisos y CA-01 a CA-14 pasan a *Confirmado*; PAR-006 queda aprobado para el piloto.
- **Los 4 bloques del LOOP v2.1 están completos.** Se generó `16_DOCUMENTO_DEFINICION_REQUERIMIENTOS.md` (23 secciones; RF-01 a RF-24, RNF-01 a RNF-12, matriz de trazabilidad y plan por fases).
- Demostrador: se programaron IND-17 (productividad), IND-18 (estacionalidad), IND-19 (dispersión) e IND-20 (Pareto de causas); 10 pruebas en verde.
- **Fase 0 (demostrador metodológico) completada.** Pendientes para pasar a la fase 1: PEN-004 a PEN-009.

## Actualización 2026-11-20 — Kit de arranque de la fase 1

- Se agregó `FASE1_ARRANQUE/`: plantilla Excel de carga de las 14 fuentes, formulario de estudio de tiempos, validador de carga (esquema S-01 a S-11 y reglas V-01 a V-16), guía para jefaturas, borradores de correos para PEN-007/008/009 y propuesta de estatuto del Comité (PEN-004).
- Los correos son **borradores**: no se ha enviado nada.
- Próximo paso: presentación ejecutiva para el patrocinador.

---

## Actualización 2026-11-20 · Cierre de la Fase 0 (levantamiento y definición)

**Estado:** Fase 0 cerrada. La definición de requerimientos está completa y aprobada (Bloques 1 a 4).

**Entregables finales de la Fase 0:**
- Documentos 12 a 16 de DOCUMENTACION (bloques aprobados y Documento de Definición de Requerimientos).
- Demostrador con datos ficticios en DATOS/BANCO-VOLCAN-AZUL (motor, 21 indicadores, pruebas).
- Kit de arranque de la Fase 1 en FASE1_ARRANQUE (plantillas, validador, guía para jefaturas, propuesta de Comité, borradores de correos).
- Presentación ejecutiva al patrocinador (11 diapositivas): https://claude.ai/artifact/5dGwbNuodPFejwEAeftPcV (privada hasta que se comparta).

**Siguiente hito:** aprobación del patrocinador para arrancar la Fase 1 (12 semanas, VP Operaciones y Canales).

**Pendientes que dependen del banco:** PEN-004 (Comité de Capacidad), PEN-005 y PEN-006 (dueños de fuentes y seudonimización por Talento Humano), PEN-007 a PEN-009 (Legal, Seguridad de la Información y Tecnología). Los correos de PEN-007 a PEN-009 están en borrador y no se han enviado.

---

## Actualización 2026-11-20 · Fase 1 simulada con datos ficticios

- Se agregó `FASE1_SIMULACION/`: simulación reproducible del piloto de 12 semanas (23-nov-2026 al 12-feb-2027).
- Incluye acta del patrocinador, dos sesiones del Comité, tres rondas de carga revisadas con el validador, estudio de tiempos
  en el formulario oficial, informe mensual 01, validación con jefaturas y cierre de la fase.
- Resultado: criterios de salida cumplidos salvo la coincidencia con jefaturas (93,0 % frente a 95 %), por grupos en el límite
  de un umbral. La Fase 2 queda condicionada al informe 02.
- Nota: la sección de cierre de la Fase 0 se había creado por error en la raíz del repositorio; se movió a este archivo.
