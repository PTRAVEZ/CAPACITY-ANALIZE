# FASE 1 · Simulación del piloto (datos ficticios)

> **Todo en esta carpeta es una simulación.** El Banco Volcán Azul S.A. no existe; las fechas, personas y cifras
> son ilustrativas y sirven para mostrar cómo se vería el piloto de 12 semanas de principio a fin.

## Cómo se reproduce

```bash
pip install -r DATOS/BANCO-VOLCAN-AZUL/requirements.txt
python FASE1_SIMULACION/scripts/simular_fase1.py
pytest -q FASE1_SIMULACION/tests
```

El script usa el validador de `FASE1_ARRANQUE/` y el motor de `DATOS/BANCO-VOLCAN-AZUL/`. Regenera los documentos
03 a 08 y la carpeta `resultados/`. Las cargas completas quedan en `trabajo/`, que no se versiona.

## Cronología del piloto

| Semana | Fecha | Hito | Documento |
|---|---|---|---|
| 1 | 23-nov-2026 | El patrocinador aprueba el piloto | [01](01_ACTA_APROBACION_PATROCINADOR.md) |
| 2 | 02-dic-2026 | Sesión 1 del Comité de Capacidad (instalación) | [02](02_COMITE_SESION_01.md) |
| 3-4 | 07 al 16-dic-2026 | Tres rondas de carga de datos hasta quedar apta | [03](03_BITACORA_CARGA_DATOS.md) |
| 4-7 | 14-dic-2026 al 08-ene-2027 | Estudio de tiempos de 5 actividades | [04](04_ESTUDIO_TIEMPOS.md) |
| 8 | 14-ene-2027 | Informe mensual 01 (día hábil 9) | [05](05_INFORME_MENSUAL_01.md) |
| 9 | 18 al 22-ene-2027 | Validación de resultados con las jefaturas | [06](06_VALIDACION_JEFATURAS.md) |
| 10 | 27-ene-2027 | Sesión 2 del Comité: aprueba el informe y decide | [07](07_COMITE_SESION_02.md) |
| 12 | 12-feb-2027 | Cierre de la fase y recomendación para la Fase 2 | [08](08_CIERRE_FASE1.md) |

## Contenido

| Ruta | Qué es |
|---|---|
| `scripts/simular_fase1.py` | Simulación reproducible (semilla 20261123) |
| `resultados/validacion_*.csv` | Reporte del validador para cada ronda de carga |
| `resultados/FORMULARIO_ESTUDIO_TIEMPOS_completado.xlsx` | Formulario oficial con las 160 observaciones |
| `resultados/estudio_tiempos_*.csv` | Observaciones y nuevos tiempos estándar |
| `resultados/resumen_*_piloto.csv` | Resultados del cálculo por unidad-cargo y por gerencia |
| `resultados/validacion_jefaturas.csv` | Comparación herramienta vs. percepción de las jefaturas |
| `tests/test_simulacion.py` | Pruebas de la simulación |
