# 10. Informe QA

**Estado:** NO INICIADO para validación del producto
**Fecha de revisión:** 2026-11-20

## Alcance de esta revisión

Se revisó estáticamente el inventario del kit sintético disponible bajo `DATOS/CAPACITY-ANALIZE/` y se alineó su estado con el LOOP v2. No se ejecutaron la aplicación, la instalación de dependencias ni las pruebas en este ciclo. No se atribuyen resultados aprobados o fallidos sin ejecución.

## Inventario y resultados

| Área | Hallazgo | Estado |
|---|---|---|
| Código | Existe una interfaz de demostración en `app.py` y un módulo parcial de cálculos en `src/calculations.py`. | Inspeccionado; no ejecutado |
| Pruebas | Existe `tests/test_calculations.py`. | Pendientes de ejecución |
| Datos | Hay 15 CSV y un libro XLSX; el usuario confirmó que son sintéticos. | Significado y relaciones pendientes de validación funcional |
| Reglas | El kit contiene fórmulas iniciales y parámetros ilustrativos. | No aprobados para uso real |
| Perfil de datos | El perfil declara cero nulos, mientras la inspección previa encontró 14 valores vacíos en `bridge_actividad_cargo.csv`, `vigente_hasta`. | Discrepancia pendiente de conciliar |
| Volúmenes y tiempos | El cálculo `workload_hours` exige `nivel_complejidad`, que no aparece en la tabla de volúmenes. | Incompatibilidad pendiente de definición |
| Referencias a agencias | La inspección preliminar encontró 110 filas de volumen y 110 de reproceso sin match bajo las relaciones inferidas. | Llaves/granularidad pendientes de validar; no declarar error definitivo |

## Pruebas ejecutadas

- Unitarias: ninguna.
- Integración: ninguna.
- Funcionales / aceptación: ninguna.
- Regresión: ninguna.
- Seguridad / rendimiento: ninguna.

No se declara el producto aprobado, funcional ni listo para producción. Tampoco se registran pruebas fallidas, porque no se ejecutaron.

## Incidencias abiertas

| ID | Hallazgo | Estado | Acción siguiente |
|---|---|---|---|
| QA-001 | Reglas y fórmulas del prototipo no están aprobadas. | Abierta | Validar en Bloque 3 antes de aceptar resultados. |
| QA-002 | El código y la suite no se han ejecutado. | Abierta | Ejecutar en una fase autorizada con criterios confirmados y registrar salida real. |
| QA-003 | Inconsistencia de nulos y referencias de datos. | Abierta | Confirmar definiciones, llaves y perfil con responsables en Bloque 2. |
| QA-004 | El cálculo de carga requiere complejidad que no está en la fuente de volúmenes. | Abierta | Resolver el origen o definición de complejidad antes de implementar ese flujo. |

## Estrategia de validación posterior

Al cerrar los requerimientos, derivar pruebas trazables a cada `CA-`: unitarias para reglas deterministas, integración para fuentes y componentes implementados, funcionales y de aceptación con ejemplos esperados aprobados, y regresión para cambios posteriores. Registrar configuraciones, entradas, salidas, errores y limitaciones reales. Agregar criterios de seguridad o rendimiento cuando las restricciones del Bloque 4 queden definidas.
