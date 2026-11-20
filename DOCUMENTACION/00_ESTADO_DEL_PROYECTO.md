# 00. Estado del proyecto

**Estado general:** EN ANÁLISIS
**Fase actual:** LOOP v2 · Bloque 1 · Tema 1.1
**Última actualización:** 2026-11-20

## Tablero

| Área | Estado | Evidencia / condición |
|---|---|---|
| Reconstrucción histórica accesible | APROBADO | Sesiones y fuentes efectivamente accesibles revisadas; límites documentados en `01`. El adjunto más reciente no está accesible en la ruta provista y no se presume leído. |
| Auditoría de repositorio y kit | EN VALIDACIÓN | Se identificó el paquete sintético bajo `DATOS/CAPACITY-ANALIZE/`; ver `02`. El directorio `DATOS/` estaba sin seguimiento por Git y se preserva. |
| Propósito y alcance general | APROBADO | El usuario confirmó análisis de capacidad humana en banca privada y que los tres síntomas identificados coexisten; ver `11`. |
| Definición funcional detallada | EN ANÁLISIS | Bloque 1, Tema 1.1 abierto. Falta describir el proceso actual, esfuerzo y fallas concretas antes de avanzar a 1.2. |
| Datos / diccionario | PENDIENTE DE DEFINICIÓN | Hay 15 CSV y un libro Excel sintéticos; definiciones de columnas, relaciones y calidad deben validarse. |
| Reglas de negocio y fórmulas | PENDIENTE DE DEFINICIÓN | Fórmulas y parámetros del kit son iniciales/ilustrativos; `RN-001` permanece Propuesto. |
| Arquitectura de producción y despliegue | PENDIENTE DE DEFINICIÓN | Hay un prototipo Streamlit existente, pero la tecnología, operación, permisos y despliegue no han sido aprobados. Completar Bloque 4 antes de seleccionarlos. |
| Implementación de negocio | NO INICIADO | No iniciar nuevas funciones de negocio hasta las puertas de definición y aceptación. El código de demostración no equivale a producto aprobado. |
| QA y validación integral | NO INICIADO | La suite existe, pero no se ejecutó en este ciclo. |
| Documentación de integración | EN VALIDACIÓN | `11` alinea el LOOP v2 con el diagnóstico y el kit; falta leer el adjunto indicado para cerrar la comparación completa. |

## Registro del LOOP v2

| ID | Estado | Descripción breve |
|---|---|---|
| DEC-001 | Confirmado | Producto de análisis de capacidad humana para un banco privado, dentro del alcance del LOOP v2. |
| DEC-002 | Confirmado | El usuario confirmó que los datos de `DATOS/` son sintéticos y no identifican personas reales. |
| DEC-003 | Confirmado | Coexisten los síntomas A, B y C: justificar dotación/vacantes; visibilidad de distribución de carga; planificación que no refleja bien cambios del trabajo. |
| PEN-001 | Pendiente | Cómo se atienden hoy estos problemas, esfuerzo y fallas/impacto concretos; responsable sugerido: dueño del proceso / usuario. |
| RN-001 | Propuesto | Las fórmulas del kit no son reglas oficiales aprobadas; requieren validación y aprobador. |
| RSK-001 | Pendiente de validación | Hay 110 registros en volúmenes y 110 en reprocesos sin correspondencia con agencias bajo las relaciones inferidas. Confirmar claves y granularidad antes de tratarlos como errores definitivos. |

## Pruebas

- Ejecutadas en este ciclo: ninguna.
- Aprobadas: ninguna.
- Fallidas: ninguna registrada.
- Existe `DATOS/CAPACITY-ANALIZE/tests/test_calculations.py`; sus casos y ejecución se documentarán al llegar a la fase de validación.

## Bloqueos e incidencias

1. **Definición funcional:** falta completar y validar el Tema 1.1. No avanzar a 1.2 sin validar el registro o indicar `CONTINUAR CON PENDIENTE`.
2. **Adjunto no accesible:** “Pasted text #1” no está disponible en la ruta del entorno actual. Se integra el LOOP v2 visible, pero no se presume el contenido del adjunto.
3. **Datos y reglas:** el diccionario y las fórmulas del kit son preliminares; no constituyen aprobación funcional ni regulatoria.

## Próximas actividades

1. Recibir el texto del adjunto en el chat o en una ubicación accesible y compararlo con `11`.
2. Completar el Tema 1.1 describiendo el método actual, esfuerzo y fallas/impactos; registrar propuesta y esperar validación.
3. Al cerrar 1.1, seguir el orden del Bloque 1 y conservar trazabilidad entre decisiones, fuentes, datos, reglas, indicadores y criterios.
4. No iniciar implementación nueva hasta satisfacer las puertas funcionales y técnicas correspondientes.
