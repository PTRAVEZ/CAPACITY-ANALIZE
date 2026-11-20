# CAPACITY-ANALIZE — Resumen de resultados (DATOS FICTICIOS)

> Banco Volcán Azul S.A. es una entidad **ficticia**. Las fórmulas son **propuestas metodológicas** pendientes de aprobación; ningún valor de este reporte constituye una decisión.

**Período base:** 2025-11 a 2026-10 · **Fecha de corte de dotación:** 2026-10-31 · **Horas productivas de 1 FTE en el período:** 1,800 h · **Factor no productivo (PAR-002):** 10%

## 1. Indicadores globales del piloto

| Dotación a la fecha de corte | FTE contractual (corte) | FTE disponible efectivo | FTE requerido | Brecha efectiva (disp − req) | Utilización | Horas extra en el período |
|---|---|---|---|---|---|---|
| 298 | 295.0 | 262.9 | 260.7 | 2.3 | 99% | 14,225.0 |


*Brecha efectiva* compara FTE disponible con FTE requerido (ambos ya netos de ausencias). *Brecha de dotación* compara FTE contractual con FTE requerido ajustado por indisponibilidad. Son dos lecturas del mismo fenómeno: **no deben sumarse**.

## 2. Por gerencia

| gerencia_id | fte_contractual_corte | fte_disponible | fte_requerido | brecha_fte | utilizacion | estado |
|---|---|---|---|---|---|---|
| GER-CCC | 33.0 | 30.1 | 33.0 | -2.9 | 110% | Sobrecarga |
| GER-OPC | 102.0 | 90.8 | 88.5 | 2.3 | 98% | Equilibrio |
| GER-RAS | 160.0 | 142.0 | 139.1 | 2.9 | 98% | Equilibrio |

## 3. Unidades y cargos en sobrecarga (utilización anual > umbral PAR-004)

Grupos con menos de 3 personas (PAR-006) se marcan con agregacion = N: en producción se mostrarían agregados al nivel superior.

| nombre_unidad | nombre_cargo | agregacion | dotacion_corte | fte_disponible | fte_requerido | brecha_fte | utilizacion | meses_sobrecarga | horas_extra |
|---|---|---|---|---|---|---|---|---|---|
| Agencia Ibarra | Supervisor Operativo de Agencia | N | 1 | 0.7 | 0.9 | -0.2 | 132% | 4 | 29 |
| Agencia Matriz Quito (Av. Amazonas) | Cajero | S | 9 | 8.3 | 10.9 | -2.5 | 130% | 11 | 1,358 |
| Departamento de Tarjetas y Reclamos | Analista Operativo | S | 11 | 10.3 | 12.2 | -1.9 | 118% | 9 | 1,521 |
| Agencia Quito Norte (El Condado) | Cajero | S | 7 | 6.0 | 7.0 | -1.0 | 117% | 11 | 854 |
| Centro de Contacto | Agente de Centro de Contacto | S | 30 | 24.7 | 28.1 | -3.4 | 114% | 11 | 3,588 |
| Agencia Ambato | Asesor de Negocios | S | 4 | 3.6 | 4.1 | -0.5 | 113% | 10 | 533 |
| Agencia Matriz Quito (Av. Amazonas) | Asesor de Servicios | S | 7 | 6.2 | 7.0 | -0.8 | 112% | 9 | 1,052 |
| Departamento de Cuentas y Servicios | Analista Operativo | S | 18 | 15.4 | 17.1 | -1.8 | 111% | 9 | 2,429 |
| Agencia Ibarra | Cajero | S | 5 | 4.3 | 4.6 | -0.2 | 106% | 4 | 177 |

## 4. Unidades y cargos con holgura (utilización anual < umbral PAR-005)

| nombre_unidad | nombre_cargo | agregacion | dotacion_corte | fte_disponible | fte_requerido | brecha_fte | utilizacion |
|---|---|---|---|---|---|---|---|
| Departamento de Cámara de Compensación y Valores | Analista Operativo | S | 8 | 7.2 | 4.5 | 2.6 | 63% |
| Agencia Otavalo | Cajero | S | 4 | 3.6 | 2.5 | 1.1 | 70% |
| Departamento de Cámara de Compensación y Valores | Asistente Operativo | S | 4 | 3.6 | 2.5 | 1.0 | 71% |
| Agencia Otavalo | Asesor de Servicios | S | 3 | 2.7 | 2.0 | 0.8 | 72% |
| Agencia Cumbayá | Cajero | S | 4 | 3.6 | 2.8 | 0.8 | 78% |

## 5. Oportunidades de redistribución (a evaluar)

| cargo_id | unidad_origen | unidad_destino | misma_provincia | fte_movible | utilizacion_origen | utilizacion_destino |
|---|---|---|---|---|---|---|
| CAR-ANO | DEP-CAM | DEP-TAR | S | 1.5 | 63% | 118% |
| CAR-ANO | DEP-CAM | DEP-CTA | S | 1.0 | 63% | 111% |
| CAR-ASV | AG-OTA | AG-QMA | N | 0.5 | 72% | 112% |
| CAR-CAJ | AG-OTA | AG-QMA | N | 1.0 | 70% | 130% |
| CAR-CAJ | AG-CUM | AG-QMA | S | 0.5 | 78% | 130% |

## 6. Reprocesos: horas potencialmente liberables (top 10)

| nombre_proceso | causa_principal | cantidad_reprocesos | horas_reproceso | fte_potencialmente_liberable |
|---|---|---|---|---|
| Negocios y colocación en agencia | Información de ingresos no verificable | 1,663 | 616 | 0.34 |
| Servicios al cliente en agencia | Documentación incompleta | 3,000 | 608 | 0.34 |
| Servicios al cliente en agencia | Firma no coincide | 2,902 | 577 | 0.32 |
| Negocios y colocación en agencia | Documentación incompleta | 1,551 | 554 | 0.31 |
| Negocios y colocación en agencia | Error en la simulación | 1,518 | 550 | 0.31 |
| Servicios al cliente en agencia | Información inconsistente del cliente | 2,875 | 540 | 0.30 |
| Gestión de cuentas y cumplimiento | Documentación incompleta desde agencia | 3,264 | 478 | 0.27 |
| Gestión de cuentas y cumplimiento | Error en ficha del cliente | 3,769 | 467 | 0.26 |
| Atención telefónica y digital | Información incorrecta al cliente | 4,736 | 414 | 0.23 |
| Operaciones de crédito | Garantía sin inscripción | 1,352 | 399 | 0.22 |


Total: **8,207 h** ≈ **4.6 FTE** si se eliminaran todos los reprocesos.

## 7. Escenarios 2027 (FTE requerido para dotación vs. FTE contractual actual)

| escenario_id | nombre_escenario | fte_requerido | fte_requerido_dotacion | fte_contractual_corte | brecha_dotacion_fte |
|---|---|---|---|---|---|
| ACTUAL | Situación actual (período base) | 260.7 | 292.6 | 295.0 | +2.4 |
| ESC-AUT | Automatización back office | 266.8 | 299.6 | 295.0 | -4.6 |
| ESC-BASE | Base 2027 | 271.1 | 304.3 | 295.0 | -9.3 |
| ESC-CRE | Crecimiento comercial | 279.1 | 313.3 | 295.0 | -18.3 |
| ESC-DIG | Migración digital | 259.1 | 290.8 | 295.0 | +4.2 |


Brecha de dotación positiva = exceso de FTE; negativa = faltante.

## 8. Calidad de datos

| regla | severidad | registros |
|---|---|---|
| V-02 | ERROR | 1 |
| V-04 | ERROR | 1 |
| V-07 | ADVERTENCIA | 1 |
| V-08 | ERROR | 1 |
| V-09 | ERROR | 1 |
| V-10 | ERROR | 1 |
| V-11 | ADVERTENCIA | 1 |
| V-15 | OK | 1 |
| V-16 | ADVERTENCIA | 2 |


Conciliación de dotación (V-15): inicial 300 + ingresos 22 − salidas 24 = 298 vs. corte 298 → **Conciliado**.
