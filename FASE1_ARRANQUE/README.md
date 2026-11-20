# FASE 1 · Kit de arranque del piloto con datos reales

Este kit prepara el paso de la **fase 0 (demostrador con el banco ficticio)** a la **fase 1 (piloto con datos reales)** del plan de `DOCUMENTACION/16_DOCUMENTO_DEFINICION_REQUERIMIENTOS.md` §23. Su objetivo es destrabar los pendientes PEN-004 a PEN-009 y recibir las fuentes reales con la calidad necesaria.

## Contenido

| Carpeta / archivo | Para qué sirve | Pendiente que atiende |
|---|---|---|
| `plantillas/PLANTILLA_CARGA_FUENTES.xlsx` | Una hoja por fuente (14), con definiciones en cada encabezado, listas desplegables y validaciones de números y fechas | DEC-021, RF-01 |
| `plantillas/FORMULARIO_ESTUDIO_TIEMPOS.xlsx` | Registro de observaciones (calcula minutos por unidad), resumen por actividad y estimación de 3 puntos (PERT) | PEN-005, PEN-006 |
| `scripts/esquema_fuentes.py` | Definición única de columnas, tipos y valores permitidos de las 14 fuentes | DEC-019 a DEC-021 |
| `scripts/generar_plantillas.py` | Vuelve a generar las dos plantillas desde el esquema | — |
| `scripts/validar_carga.py` | Revisa una carga real antes de calcular: esquema (S-01 a S-11) y reglas de negocio (V-01 a V-16) | DEC-022, RF-02 |
| `guias/GUIA_JEFATURAS.md` | Instrucciones para las jefaturas: qué registrar, cómo medir tiempos y qué no incluir | DEC-017, PEN-005/006 |
| `comunicaciones/CORREOS_PEN-007_008_009.md` | Borradores de correos para Legal, Seguridad de la Información y Tecnología | PEN-007, 008, 009 |
| `comite/PROPUESTA_COMITE_CAPACIDAD.md` | Propuesta de estatuto del Comité de Capacidad | PEN-004 |
| `tests/test_validar_carga.py` | 5 pruebas del validador | — |

## Cómo usarlo

```bash
pip install pandas numpy openpyxl pytest

# 1. (Opcional) Regenerar las plantillas
python FASE1_ARRANQUE/scripts/generar_plantillas.py

# 2. Validar una carga entregada en Excel (y exportar los 14 CSV normalizados)
python FASE1_ARRANQUE/scripts/validar_carga.py --excel PLANTILLA_CARGA_FUENTES_lleno.xlsx --exportar carga_2027_01

# 3. O validar una carpeta con los 14 CSV
python FASE1_ARRANQUE/scripts/validar_carga.py --dir carga_2027_01

# 4. Si la carga es APTA, calcular con el motor
python DATOS/BANCO-VOLCAN-AZUL/src/capacity_analize.py --input carga_2027_01 --output resultados_2027_01 --reportes resultados_2027_01

# Pruebas
python -m pytest -q FASE1_ARRANQUE/tests
```

### Reglas de esquema del validador

| Regla | Qué revisa | Severidad |
|---|---|---|
| S-01 | Falta la fuente | ERROR |
| S-02 | Falta una columna | ERROR |
| S-03 | Columna no esperada (se ignora) | ADVERTENCIA |
| S-04 | Columna con dato personal prohibido (nombre, cédula, salario, diagnóstico, correo…) | ERROR |
| S-05 | Valor requerido vacío | ERROR |
| S-06 | Tipo inválido (fecha AAAA-MM-DD, período AAAA-MM, número, S/N) | ERROR |
| S-07 | Número fuera de rango | ERROR |
| S-08 | Valor fuera de la lista permitida | ERROR |
| S-09 | Llave duplicada | ERROR |
| S-10 | El seudónimo parece una cédula, un correo o un nombre | ERROR |
| S-11 | Fuente vacía o fila de ejemplo ignorada | ADVERTENCIA |

Las reglas V-01 a V-16 se ejecutan solo si no hay errores de esquema. Con los datos ficticios, el validador encuentra el duplicado y el volumen negativo sembrados (S-09, S-07). Al corregirlos, encuentra el resto de las anomalías con las reglas V-.

## Hoja de ruta de la fase 1 (12 semanas, propuesta)

| Semana | Actividad | Responsable sugerido | Entregable |
|---|---|---|---|
| 1 | Presentación al patrocinador y aprobación del arranque | Capacity Management | Acta de arranque |
| 1–2 | Envío de los correos de PEN-007, 008 y 009 | Capacity Management | Correos enviados y respuestas |
| 2 | Constitución del Comité de Capacidad | Vicepresidencia de Operaciones y Canales | Estatuto firmado (PEN-004) |
| 2–3 | Mapeo de las fuentes reales contra el esquema y seudonimización por Talento Humano | Talento Humano + Capacity | Diccionario real validado |
| 3–8 | Estudios de tiempos de las 17 actividades priorizadas (ACT-017 y las 16 estimaciones expertas) | Jefaturas + Capacity | Formularios completos |
| 4–6 | Primera carga real con la plantilla y su validación | Dueños de las fuentes | Reporte de validación sin errores |
| 7–9 | Primer cálculo y revisión con los gerentes | Capacity + gerentes | Resultados validados (CA-07, CA-08) |
| 10 | Aprobación del primer período en el Comité | Comité de Capacidad | Período cerrado |
| 11–12 | Lecciones aprendidas y decisión de pasar a la fase 2 | Comité | Informe de cierre de la fase 1 |

**Criterios de salida (documento 16 §23):** CA-07 (trazabilidad), CA-08 (identificación de brechas ≥ 95 %), CA-10 (resultados al día hábil 10) y primer período aprobado por el Comité.
