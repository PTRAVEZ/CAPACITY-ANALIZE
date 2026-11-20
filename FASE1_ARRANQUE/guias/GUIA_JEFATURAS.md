# Guía para jefaturas · Piloto CAPACITY-ANALIZE

> Destinatarios: Jefes de Agencia, Jefes de Departamento y Supervisores del Centro de Contacto de la Vicepresidencia de Operaciones y Canales (perfil USR-02).
> Tiempo estimado de lectura: 10 minutos.

## 1. ¿Para qué es esto?

CAPACITY-ANALIZE mide **cuánto trabajo tiene cada unidad y cuánta gente está realmente disponible para hacerlo**. Con esa medición, su unidad podrá **sustentar vacantes y refuerzos con datos** y no solo con percepción.

**No es una evaluación de desempeño individual.** Los resultados se muestran agregados por unidad y cargo, nunca por persona (RN-10, DEC-031).

## 2. Qué le pedimos

| Qué | Cuándo | Cómo | Tiempo aproximado |
|---|---|---|---|
| Revisar el catálogo de actividades de su unidad | Una vez, al inicio del piloto | Confirmar que estén todas las actividades, que cada una tenga un solo cargo ejecutor y que el tiempo estándar sea razonable | 1 a 2 horas |
| Registrar los volúmenes que **no** salen de un sistema | Cada mes, hasta el día hábil 5 | Hoja `08_volumenes_mensuales` de la plantilla | 30 minutos al mes |
| Registrar los reprocesos y su causa principal | Cada mes, hasta el día hábil 5 | Hoja `09_reprocesos` | 15 minutos al mes |
| Apoyar los estudios de tiempos | Semanas 3 a 8 del piloto | `FORMULARIO_ESTUDIO_TIEMPOS.xlsx` | Según la actividad |
| Revisar los resultados de su unidad | Cada mes, antes del Comité | Ficha de unidad | 30 minutos al mes |

## 3. Reglas para registrar bien los datos

1. **El volumen cuenta solo el trabajo de primera vez.** Si una apertura de cuenta se rechazó y se rehizo, cuenta 1 en volumen y 1 en reprocesos, nunca 2 en volumen (RN-03).
2. **Cada actividad tiene una unidad de trabajo fija:** transacción, expediente, llamada, hora… No las mezcle.
3. **Las actividades de gestión se registran en horas** (por ejemplo, supervisión o comités).
4. **Use los códigos**, no los nombres: `unidad_id`, `actividad_id` y `periodo` en formato AAAA-MM.
5. **Si no está seguro de un dato**, déjelo vacío y anótelo en observaciones: es preferible a inventarlo.

## 4. Privacidad: nunca incluya

- Nombres, cédulas, correos o teléfonos de colaboradores o clientes.
- Salarios o información de la nómina.
- Motivos médicos o diagnósticos.

Para referirse a un colaborador use solo su **seudónimo** (COL-xxxx), que le entregará Talento Humano.

## 5. Cómo hacer un estudio de tiempos

1. Elija la actividad indicada por Capacity Management.
2. Informe al colaborador que se mide **la actividad, no a la persona**.
3. Registre la hora de inicio y fin de cada unidad de trabajo en la hoja **Registro**. La duración y los minutos por unidad se calculan solos.
4. Observe **al menos 30 unidades** en distintos días y horarios, y con distintos colaboradores.
5. Marque `es_reproceso = S` cuando la unidad sea un rehacer.
6. Revise la hoja **Resumen**: debe decir "Sí" en la columna ¿suficiente?
7. Si medir no es posible, complete **Estimacion_3_puntos** con tres valores (optimista, más probable, pesimista).

## 6. Calendario mensual

| Día hábil | Actividad |
|---|---|
| 1–5 | Jefaturas registran volúmenes manuales y reprocesos |
| 1–5 | Talento Humano y Operaciones cargan las fuentes de sistema |
| 6–7 | Capacity valida la carga (`validar_carga.py`) y pide correcciones |
| 8–9 | Cálculo y revisión con los gerentes |
| 10 | Resultados disponibles (DEC-018) |

## 7. Preguntas frecuentes

- **¿Esto se usará para evaluarme a mí o a mi equipo?** No. La productividad (IND-17) solo se muestra por unidad, y un valor alejado del promedio es una señal para revisar, no una calificación.
- **¿Qué pasa si mi unidad sale en sobrecarga?** Es un sustento para pedir refuerzo, redistribución o mejoras de proceso (decisiones D-1 a D-4).
- **¿Puedo corregir un dato después del cierre?** Sí, pero genera una nueva versión del período con su motivo (RN-08).

Contacto: equipo de Capacity Management.
