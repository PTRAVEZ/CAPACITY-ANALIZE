# 06 · Validación de resultados con las jefaturas

> **Simulación con datos ficticios.** Banco Volcán Azul S.A. no existe; fechas, personas y cifras son ilustrativas.

**Fecha:** 18 al 22-ene-2027 · **Método:** cada jefatura revisó la clasificación de sus grupos (sobrecarga, equilibrio u holgura)
sin ver antes la utilización calculada, y luego se compararon. Detalle: `resultados/validacion_jefaturas.csv`.

| Resultado | Valor |
|---|---|
| Grupos revisados | 43 |
| Coinciden | 40 |
| No coinciden | 3 |
| **Coincidencia** | **93,0 %** (meta: 95 %) |

## Discrepancias

| Unidad y cargo | Utilización | Herramienta | Jefatura |
|---|---|---|---|
| Asistente Operativo · Departamento de Tarjetas y Reclamos | 104 % | Equilibrio | Sobrecarga |
| Cajero · Agencia Cumbayá | 82 % | Equilibrio | Holgura |
| Cajero · Agencia Valle de los Chillos | 106 % | Sobrecarga | Equilibrio |

**Resultado:** no se cumple la meta de 95 %.

Todas las discrepancias están en grupos a menos de 2 puntos de un umbral: la jefatura y la herramienta ven lo mismo,
pero lo clasifican distinto por estar en el límite. Fuera de esa franja, la coincidencia es de 100 %
(40 de 40 grupos).

**Propuesta:** en el informe, marcar como "en el límite" los grupos a ±2 puntos de un umbral, en lugar de forzar una
clasificación, y volver a medir la coincidencia en el informe 02.
