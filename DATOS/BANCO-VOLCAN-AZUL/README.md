# CAPACITY-ANALIZE

**Análisis de capacidad humana para banca privada: levantamiento de requerimientos y demostrador con datos ficticios.**

> ⚠️ **Todos los datos de este repositorio son FICTICIOS.** *Banco Volcán Azul S.A.* no existe. La estructura, los cargos, los volúmenes y los tiempos están inspirados en un banco privado mediano de Ecuador, pero no representan a ninguna entidad real. Las fórmulas son **propuestas metodológicas** pendientes de aprobación.

## ¿Qué contiene?

| Carpeta / archivo | Contenido |
|---|---|
| `docs/LOOP_CAPACITY-ANALIZE.md` | Prompt del **LOOP de levantamiento de requerimientos** (v2), con un anexo para usarlo junto con estos datos. |
| `docs/diccionario_datos.md` | Fichas de las 14 fuentes y su diccionario de datos preliminar. |
| `docs/metodologia_calculo.md` | Taxonomía de tiempo, reglas anti-doble conteo, fórmulas propuestas (IND-) y reglas de validación (V-). |
| `docs/anomalias_sembradas.md` | Errores de datos introducidos a propósito para probar la validación. |
| `data/input/` | **14 archivos CSV de entrada** (ver tabla abajo). |
| `scripts/generar_datos_ficticios.py` | Regenera todos los datos de entrada (semilla fija, resultado reproducible). |
| `src/capacity_analize.py` | Motor demostrativo: valida y calcula IND-01 a IND-21 (FTE, brechas, reprocesos, redistribución, escenarios, productividad, estacionalidad, dispersión y Pareto de causas). |
| `data/output/` | Resultados calculados (16 CSV). |
| `reports/resumen_resultados.md` | Resumen ejecutivo generado automáticamente. |
| `tests/` | Pruebas de consistencia (CA-01 a CA-06 e IND-17 a IND-20; 10 pruebas). |

## El banco ficticio (piloto de ~300 personas)

**Vicepresidencia de Operaciones y Canales**, período base **nov-2025 a oct-2026**:

- **Gerencia de Operaciones Centralizadas** (Quito): Pagos y Transferencias (SPI), Cuentas y Servicios (KYC, embargos, requerimientos de organismos de control), Operaciones de Crédito, Tarjetas y Reclamos, y Cámara de Compensación.
- **Gerencia de Red de Agencias Sierra**: 10 agencias en Quito (Matriz, Norte, Sur, Cumbayá), Sangolquí, Ibarra, Otavalo, Latacunga, Ambato y Riobamba.
- **Gerencia de Banca Telefónica y Digital**: Centro de Contacto (llamadas, chat y WhatsApp).

Los datos incluyen rasgos locales: feriados nacionales, picos de diciembre (décimo tercer sueldo), agosto (décimo cuarto en la Sierra) y abril (utilidades), pagos de impuestos al SRI, pago del Bono de Desarrollo Humano, transferencias SPI y horas suplementarias y extraordinarias.

## Archivos de entrada

| # | Archivo | Filas aprox. | Descripción |
|---|---|---|---|
| 01 | `01_estructura_organizacional.csv` | 21 | Banco → Dirección → Gerencias → Departamentos y agencias |
| 02 | `02_cargos.csv` | 14 | Catálogo de cargos |
| 03 | `03_colaboradores.csv` | 324 | Colaboradores seudonimizados (incluye reemplazos y 2 registros con errores) |
| 04 | `04_calendario_laboral.csv` | 365 | Días laborables y feriados |
| 05 | `05_parametros.csv` | 9 | Parámetros (PAR-) en estado Supuesto o Propuesto |
| 06 | `06_procesos.csv` | 12 | Procesos |
| 07 | `07_actividades.csv` | 81 | Actividades, cargo ejecutor y tiempos estándar |
| 08 | `08_volumenes_mensuales.csv` | ~3.950 | Volumen mensual por unidad y actividad |
| 09 | `09_reprocesos.csv` | ~2.700 | Reprocesos y su causa principal |
| 10 | `10_ausentismo.csv` | ~3.600 | Vacaciones, enfermedad, permisos, licencias y capacitación |
| 11 | `11_horas_extra.csv` | ~1.000 | Horas suplementarias y extraordinarias |
| 12 | `12_movimientos_personal.csv` | 46 | Ingresos y salidas |
| 13 | `13_vacantes.csv` | 26 | Vacantes de reemplazo y posiciones nuevas |
| 14 | `14_escenarios_2027.csv` | 12 | Ajustes para los escenarios de 2027 |

## Cómo ejecutarlo

```bash
# 1. Instalar dependencias (Python 3.10 o superior)
pip install -r requirements.txt

# 2. (Opcional) Regenerar los datos de entrada
python scripts/generar_datos_ficticios.py

# 3. Validar y calcular
python src/capacity_analize.py

# 4. Ejecutar las pruebas
python -m pytest -q
```

La salida de consola muestra los errores de validación, la conciliación de dotación y el FTE global. El detalle queda en `data/output/` y el resumen en `reports/resumen_resultados.md`.

## Cómo usar el LOOP

1. Abre `docs/LOOP_CAPACITY-ANALIZE.md` y copia todo su contenido.
2. Pégalo en una conversación nueva con tu asistente de IA.
3. Si quieres trabajar con el banco ficticio, adjunta también los CSV de `data/input/` y los documentos de `docs/`.
4. Responde una pregunta a la vez. Usa `ESTADO` para ver el registro, `PAUSA` para guardar y `RETOMAR` para continuar en otra conversación.

## Resultados de ejemplo (datos ficticios)

| Indicador | Valor |
|---|---|
| Dotación a la fecha de corte | 298 |
| FTE disponible efectivo | 262,9 |
| FTE requerido | 260,7 |
| Utilización global | 99 % |
| Unidad-cargo más sobrecargada (grupo ≥ 3 personas) | Cajeros de la Agencia Matriz Quito (130 %) |
| Mayor holgura | Analistas de Cámara de Compensación (63 %) |
| FTE potencialmente liberable por reprocesos | 4,6 |

Ver el detalle completo en [`reports/resumen_resultados.md`](reports/resumen_resultados.md).

## Estructura

```
capacity-analize/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── LOOP_CAPACITY-ANALIZE.md
│   ├── diccionario_datos.md
│   ├── metodologia_calculo.md
│   └── anomalias_sembradas.md
├── data/
│   ├── input/    (14 CSV)
│   └── output/   (12 CSV)
├── scripts/
│   └── generar_datos_ficticios.py
├── src/
│   └── capacity_analize.py
├── reports/
│   └── resumen_resultados.md
└── tests/
    └── test_capacity_analize.py
```

## Alcance

Solo **capacidad humana**: carga laboral, disponibilidad, productividad y FTE. Quedan fuera la capacidad tecnológica, la infraestructura, el equipamiento y el presupuesto operativo.
