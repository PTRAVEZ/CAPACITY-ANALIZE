# 09. Plan de desarrollo

> **Actualización de gobierno (2026-11-20):** el orden de definición vigente es el del LOOP v2.1: Bloque 1 (proceso, decisiones y usuarios), Bloque 2 (fuentes/datos), Bloque 3 (indicadores/fórmulas) y Bloque 4 (privacidad, accesos, operación y éxito). La implementación por fases descrita debajo queda condicionada al cierre de esas definiciones; el código y los archivos del kit no autorizan saltarse las puertas ni suponen que la tecnología esté aprobada. Para el ciclo actual, el paso activo es Bloque 1, Tema 1.1.

**Estado:** EN ANÁLISIS; la planificación de implementación depende de la definición funcional.

## Entregas y puertas

| Entrega | Objetivo y actividades | Dependencias | Archivos / resultado esperado | Pruebas y criterio de finalización |
|---|---|---|---|---|
| 0. Descubrimiento y auditoría | Reconstruir fuentes accesibles, inventariar el repositorio, documentar vacíos y preguntas. | Acceso actual al repositorio e historial disponible. | `DOCUMENTACION/00` a `10`, README; diagnóstico trazable. | Revisión de coherencia documental y de estado Git. Termina con preguntas de negocio explícitas; esta entrega queda documentada en este ciclo. |
| 1. Definición funcional | Confirmar usuario, proceso, entradas, salidas, reglas, restricciones y aceptación. | Respuestas del responsable y fuentes autorizadas. | Requerimientos, reglas, criterios y datos de ejemplo aprobados. | Cada requerimiento crítico tiene fuente y criterio verificable; aprobación del responsable. |
| 2. Diseño técnico | Comparar opciones según requisitos; definir arquitectura, modelo, interfaces, errores, seguridad y pruebas. | Entrega 1. | Arquitectura, modelo de datos y decisiones técnicas confirmadas. | Revisión contra requisitos, riesgos y entorno de despliegue. |
| 3. Base ejecutable | Configuración mínima, estructura modular, instalación, configuración y registros necesarios. | Entrega 2. | Código inicial, dependencias justificadas, guía reproducible. | Instalación y ejecución desde entorno limpio; pruebas de configuración. |
| 4. Funcionalidad central | Implementar el caso de uso confirmado con validación de entradas y manejo de errores. | Entregas 1–3. | Módulo funcional y documentación asociada. | Pruebas unitarias e integración con ejemplos aprobados; criterios de aceptación cumplidos. |
| 5. Procesamiento / análisis | Implementar únicamente transformaciones e indicadores definidos por reglas confirmadas. | Entrega 4 y reglas aceptadas. | Procesadores o motor de análisis, si se requieren. | Resultados comparados contra ejemplos esperados y casos límite aceptados. |
| 6. Interacción y reportes | Crear interfaz o reportes solo si están en alcance confirmado. | Requisitos de interacción y salidas. | Interfaz, API o reportes según decisión aprobada. | Pruebas funcionales y de aceptación de cada flujo. |
| 7. Seguridad y operación | Aplicar controles, empaquetado y despliegue acordes con clasificación y plataforma. | Diseño y restricciones de seguridad/operación. | Configuración operativa, guía de despliegue y soporte. | Verificaciones de seguridad, configuración y despliegue que se acuerden. |
| 8. Validación y entrega | Ejecutar regresión, revisar documentación y registrar incidencias y límites. | Entregas requeridas completadas. | QA final, manuales y README actualizados. | Proyecto instalable, ejecutable y pruebas obligatorias aprobadas; pendientes declarados. |

## Estado y regla de avance

Solo la entrega 0 puede avanzar sin conocer el dominio. La entrega 1 es el siguiente paso y está bloqueada por las respuestas de `03_REQUERIMIENTOS_FUNCIONALES.md`. Las entregas posteriores no se iniciarán hasta satisfacer sus dependencias y criterios.
