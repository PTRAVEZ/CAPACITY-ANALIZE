# Diccionario de datos preliminar — fuentes de entrada (DATOS FICTICIOS)

> Todos los archivos están en `data/input/`, en CSV con codificación UTF-8 y separador coma.
> Las definiciones son **propuestas**. En el LOOP (Bloque 2) cada campo debe validarse antes de pasar a estado *Confirmado*.

## Resumen de fuentes

| ID | Archivo | Fuente simulada (dueño sugerido) | Granularidad | Frecuencia | Histórico |
|---|---|---|---|---|---|
| FTE-SRC-01 | `01_estructura_organizacional.csv` | Organigrama (Talento Humano / Organización y Métodos) | Unidad | Cuando cambia la estructura | Vigente |
| FTE-SRC-02 | `02_cargos.csv` | Catálogo de cargos (Talento Humano) | Cargo | Cuando cambia el catálogo | Vigente |
| FTE-SRC-03 | `03_colaboradores.csv` | Sistema de nómina (Talento Humano) | Colaborador | Mensual | Ingresos desde 2006 |
| FTE-SRC-04 | `04_calendario_laboral.csv` | Calendario de feriados nacionales | Día | Anual | 2025-11 a 2026-10 |
| FTE-SRC-05 | `05_parametros.csv` | Comité de Capacity Management | Parámetro | Cuando se aprueban | Vigente |
| FTE-SRC-06 | `06_procesos.csv` | Mapa de procesos (Procesos / Calidad) | Proceso | Anual | Vigente |
| FTE-SRC-07 | `07_actividades.csv` | Levantamiento de actividades y estudio de tiempos (Capacity Management) | Actividad | Anual o cuando cambia el proceso | Mediciones de 2025 |
| FTE-SRC-08 | `08_volumenes_mensuales.csv` | Core bancario, plataforma del centro de contacto, registros manuales | Unidad × actividad × mes | Mensual | 12 meses |
| FTE-SRC-09 | `09_reprocesos.csv` | Registros de calidad de cada unidad | Unidad × actividad × mes | Mensual | 12 meses |
| FTE-SRC-10 | `10_ausentismo.csv` | Nómina y control de asistencia (Talento Humano) | Colaborador × mes | Mensual | 12 meses |
| FTE-SRC-11 | `11_horas_extra.csv` | Nómina (Talento Humano) | Colaborador × mes | Mensual | 12 meses |
| FTE-SRC-12 | `12_movimientos_personal.csv` | Nómina (Talento Humano) | Movimiento | Por evento | 12 meses |
| FTE-SRC-13 | `13_vacantes.csv` | Selección de personal (Talento Humano) | Vacante | Por evento | 12 meses |
| FTE-SRC-14 | `14_escenarios_2027.csv` | Planificación estratégica / Capacity Management | Ajuste de escenario | Anual | Proyección 2027 |

---

## FTE-SRC-01 · Estructura organizacional

| Campo | Tipo | Definición | Ejemplo |
|---|---|---|---|
| unidad_id | texto | Código único de la unidad organizacional | `DEP-PAG` |
| nombre | texto | Nombre de la unidad | Departamento de Pagos y Transferencias |
| nivel | texto | Banco, Dirección, Gerencia, Departamento o Agencia | Departamento |
| unidad_padre_id | texto | Unidad de la que depende (vacío para el nivel Banco) | `GER-OPC` |
| ciudad / provincia | texto | Ubicación física | Quito / Pichincha |
| tipo_unidad | texto | Back office, Red de agencias, Agencia, Centro de contacto, etc. | Back office |

## FTE-SRC-02 · Cargos

| Campo | Tipo | Definición |
|---|---|---|
| cargo_id | texto | Código único del cargo |
| nombre_cargo | texto | Nombre del cargo |
| familia | texto | Familia de puestos |
| nivel_jerarquico | texto | Gerencial, Jefatura, Supervisión, Profesional u Operativo |
| tipo_rol | texto | Gestión, Supervisión, Operativo, Comercial o Soporte |

## FTE-SRC-03 · Colaboradores (seudonimizados)

| Campo | Tipo | Unidad | Definición |
|---|---|---|---|
| colaborador_id | texto | — | Seudónimo del colaborador (no es cédula ni nombre). |
| unidad_id | texto | — | Unidad a la que está asignado. |
| cargo_id | texto | — | Cargo que ocupa. |
| fecha_ingreso | fecha | AAAA-MM-DD | Primer día laborado en el cargo y la unidad. |
| fecha_salida | fecha | AAAA-MM-DD | Último día laborado (vacío si sigue activo). |
| tipo_contrato | texto | — | Indefinido o Eventual. |
| jornada_horas_semana | número | horas/semana | Jornada contractual (40 = completa; 20 = medio tiempo). |
| modalidad | texto | — | Presencial o Híbrida. |

> **Privacidad:** no se incluyen nombres, cédulas, salarios ni datos de salud. La tabla de correspondencia entre seudónimo e identidad quedaría bajo custodia de Talento Humano (decisión pendiente del Bloque 4).

## FTE-SRC-04 · Calendario laboral

| Campo | Tipo | Definición |
|---|---|---|
| fecha | fecha | Día calendario |
| periodo | texto | Mes en formato AAAA-MM |
| dia_semana | texto | Nombre del día |
| es_laborable | S/N | S = día hábil (lunes a viernes que no es feriado) |
| feriado | texto | Nombre del feriado nacional, si aplica |

> Calendario **referencial**: los traslados de feriados se definen cada año por decreto y los feriados locales (p. ej., fundación de ciudades) no están incluidos. Validar contra el calendario oficial.

## FTE-SRC-05 · Parámetros

| Campo | Definición |
|---|---|
| parametro_id | Identificador PAR- |
| nombre | Nombre técnico usado por el motor |
| valor / unidad | Valor del parámetro y su unidad |
| estado | Supuesto o Propuesto (ninguno está aprobado) |
| descripcion | Significado y alcance |
| aprobador_sugerido | Quién debería aprobarlo |

## FTE-SRC-06 · Procesos

| Campo | Definición |
|---|---|
| proceso_id | Código del proceso |
| nombre_proceso | Nombre |
| macroproceso | Agrupación superior |
| cargo_dueno_proceso | Cargo responsable del proceso |
| grupo_estacional | Patrón de estacionalidad usado en la simulación |

## FTE-SRC-07 · Actividades y tiempos estándar

| Campo | Tipo | Unidad | Definición |
|---|---|---|---|
| actividad_id | texto | — | Código único de la actividad |
| proceso_id | texto | — | Proceso al que pertenece (una actividad pertenece a un solo proceso) |
| nombre_actividad | texto | — | Descripción |
| cargo_id | texto | — | Cargo que la ejecuta |
| unidad_trabajo | texto | — | Qué se cuenta en el volumen: transacción, expediente, llamada, hora, etc. |
| tiempo_estandar_min | número | minutos | Tiempo estándar por unidad de trabajo, sin reprocesos |
| tiempo_reproceso_min | número | minutos | Tiempo adicional por cada unidad reprocesada |
| metodo_medicion | texto | — | Estudio de tiempos, Registro de sistema, Estimación experta, Bitácora de gestión o Pendiente de medición |
| fecha_medicion | fecha | — | Fecha de la medición |
| ambito | texto | — | Dónde aplica: AGENCIA (todas las agencias), GERENCIA, DEPTO (departamentos de back office) o un `unidad_id` |
| tipo_actividad | texto | — | Core, Soporte o Gestión |

> Las actividades con `unidad_trabajo = hora` (gestión y supervisión) tienen tiempo estándar de 60 min: su volumen representa horas dedicadas.

## FTE-SRC-08 · Volúmenes mensuales

| Campo | Tipo | Definición |
|---|---|---|
| periodo | AAAA-MM | Mes |
| unidad_id | texto | Unidad que ejecutó el trabajo |
| actividad_id | texto | Actividad |
| volumen | entero | Unidades de trabajo **de primera vez** (sin reprocesos) |
| fuente | texto | Origen del dato |

## FTE-SRC-09 · Reprocesos

| Campo | Tipo | Definición |
|---|---|---|
| periodo, unidad_id, actividad_id | — | Llave igual a la de volúmenes |
| cantidad_reprocesos | entero | Unidades que debieron rehacerse (subconjunto del volumen; no se suman al volumen) |
| causa_principal | texto | Causa más frecuente del mes |

## FTE-SRC-10 · Ausentismo y capacitación

| Campo | Unidad | Definición |
|---|---|---|
| colaborador_id, periodo | — | Llave |
| horas_vacaciones | horas | Vacaciones gozadas |
| horas_enfermedad | horas | Ausencia por enfermedad |
| horas_permisos | horas | Permisos (calamidad, citas, paternidad, etc.) |
| horas_licencias | horas | Licencias prolongadas (p. ej., maternidad) |
| horas_capacitacion | horas | Capacitación institucional. **No es ausencia**, pero se descuenta del tiempo disponible |

## FTE-SRC-11 · Horas extra

| Campo | Unidad | Definición |
|---|---|---|
| colaborador_id, periodo | — | Llave |
| horas_suplementarias | horas | Horas adicionales a la jornada en días laborables |
| horas_extraordinarias | horas | Horas trabajadas en días de descanso o feriados |

> La terminología es referencial; validar con Talento Humano. Las horas extra **no** se suman a la capacidad disponible: se reportan como evidencia de brecha.

## FTE-SRC-12 · Movimientos de personal

| Campo | Definición |
|---|---|
| movimiento_id | Identificador |
| colaborador_id | Seudónimo |
| tipo_movimiento | INGRESO o SALIDA |
| fecha | Fecha del movimiento |
| unidad_id, cargo_id | Unidad y cargo involucrados |
| motivo | Reemplazo, Nueva posición, Renuncia voluntaria, Terminación de relación laboral, Jubilación |

## FTE-SRC-13 · Vacantes

| Campo | Definición |
|---|---|
| vacante_id | Identificador |
| unidad_id, cargo_id | Posición vacante |
| motivo | Reemplazo o Nueva posición |
| fecha_apertura / fecha_cierre | Fechas de apertura y cobertura (vacío si sigue abierta) |
| estado | Abierta o Cubierta |

## FTE-SRC-14 · Escenarios 2027

| Campo | Definición |
|---|---|
| escenario_id / nombre_escenario | Escenario |
| descripcion_ajuste | Qué representa el ajuste |
| ambito_tipo | GLOBAL, PROCESO o ACTIVIDAD |
| ambito_id | proceso_id o actividad_id (vacío si es GLOBAL) |
| variable | `volumen_pct` (cambio de volumen) o `tiempo_pct` (cambio del tiempo estándar) |
| valor | Proporción (0.04 = +4 %; −0.18 = −18 %). Los ajustes de un mismo escenario se multiplican |
| estado | Supuesto |
