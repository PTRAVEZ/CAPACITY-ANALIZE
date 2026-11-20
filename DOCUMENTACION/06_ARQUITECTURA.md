# 06. Arquitectura

> **Actualización (2026-11-20):** hay un prototipo de interfaz Streamlit bajo `DATOS/CAPACITY-ANALIZE/` y dependencias declaradas en `requirements.txt`. Eso describe artefactos existentes, pero no una arquitectura de producción aprobada. El LOOP v2 aplaza la selección tecnológica hasta conocer las restricciones del Bloque 4; se preserva el prototipo sin extenderlo por ahora.

**Estado:** PENDIENTE DE DEFINICIÓN

## Decisión actual

No se aprueba una arquitectura de producción, lenguaje, framework, almacenamiento, interfaz o plataforma. Existe un prototipo Streamlit en el kit; es un artefacto existente y no la selección de arquitectura del producto. El propósito general está confirmado, pero alcance detallado, operación y restricciones siguen pendientes.

## Información necesaria para el diseño

- Tipo, tamaño, calidad y frecuencia de actualización de los datos.
- Usuarios y forma de interacción requerida.
- Cálculos y tiempos de respuesta esperados.
- Necesidad de persistencia, auditoría y retención.
- Sensibilidad de los datos, autenticación y permisos.
- Entorno de despliegue, disponibilidad, presupuesto y soporte.

## Criterios de selección

Cuando se definan los requerimientos, comparar la solución más simple que los satisfaga con alternativas pertinentes considerando complejidad, rendimiento, escalabilidad, mantenimiento, seguridad, despliegue, costo y compatibilidad con las fuentes. No se incorpora una tecnología por preferencia sin necesidad demostrada.

## Componentes, flujo e interfaces

Pendientes. No se fija un flujo de procesamiento ni se presupone que el producto deba tener interfaz web, API, línea de comandos o procesamiento por lotes. La gestión de errores, seguridad e integraciones se especificará cuando se confirme el modo de uso y los datos.
