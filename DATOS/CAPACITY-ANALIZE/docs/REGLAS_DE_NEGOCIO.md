# Reglas de negocio y fórmulas iniciales

## 1. Principios
1. Unidad de cálculo primaria: actividad.
2. Unidad de asignación de capacidad: cargo / colaborador según granularidad disponible.
3. Unidad de gestión: departamento y dirección.
4. Toda métrica debe identificar período, fuente, versión y fecha de cálculo.
5. Parámetros en `parametros_modelo.csv` son ilustrativos, no políticas oficiales del banco.

## 2. Tiempo estándar
Calcular inicialmente por actividad y nivel de complejidad usando la mediana de observaciones válidas.
`Tiempo_estandar_min = mediana(tiempo_observado_min)`.
Debe mostrarse tamaño de muestra, dispersión y fecha de observación. No mezclar niveles de complejidad sin ponderación documentada.

## 3. Carga laboral
`Carga_horas = SUM(volumen_elegible * tiempo_estandar_min) / 60`.
La definición de volumen elegible debe ser explícita. Si el volumen procesado ya incluye reprocesos, no sumar reproceso nuevamente. Permitir escenarios:
- Base: volumen procesado como volumen de trabajo.
- Reproceso explícito: volumen procesado + reprocesos, solo si el dato no está incluido en procesado.

## 4. Disponibilidad efectiva
`Horas_efectivas_FTE = horas_contractuales_mes - vacaciones - ausentismo - capacitacion - reuniones - pausas`.
Validar que los descuentos sean mutuamente excluyentes y que no exista doble descuento. La disponibilidad mensual debe estar expresada por FTE.

## 5. FTE requerido
`FTE_requerido = carga_horas / horas_efectivas_FTE`.
Si horas efectivas son cero o negativas, bloquear el cálculo y generar alerta.

## 6. FTE disponible
`FTE_disponible = SUM(dedicacion_porcentaje / 100)` para colaboradores activos, con filtros de período, departamento y cargo.
El estado de licencia prolongada debe manejarse mediante regla explícita configurable; no asumir automáticamente disponibilidad total.

## 7. Brecha
`Brecha_FTE = FTE_requerido - FTE_disponible`.
- Positiva: déficit estimado.
- Negativa: excedente estimado.
- Cero: equilibrio matemático, no necesariamente equilibrio operativo.

## 8. Utilización
`Utilizacion = carga_horas / (FTE_disponible * horas_efectivas_FTE)`.
Mostrar como porcentaje y advertir si supera 100%.

## 9. Calidad y controles
- IDs únicos en dimensiones.
- Integridad referencial entre hechos y dimensiones.
- Períodos en formato YYYY-MM.
- Volúmenes enteros no negativos.
- Tiempos positivos.
- Dedicación entre 0 y 100.
- Conciliar colaboradores por estado y vacantes por estado.
- Identificar nulos, duplicados, valores atípicos y períodos faltantes.
- Registrar cualquier imputación o transformación.

## 10. Advertencias de uso
Los datos son sintéticos. Los umbrales y supuestos no constituyen normativa de Ecuador ni política bancaria. La aplicación debe permitir configurar parámetros y registrar quién los aprueba.
