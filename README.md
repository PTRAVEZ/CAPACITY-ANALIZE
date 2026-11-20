# CAPACITY-ANALIZE

## Propósito y alcance

El proyecto busca apoyar el análisis de capacidad humana en un banco privado: carga de trabajo, actividades, volúmenes, tiempos, disponibilidad y necesidades de FTE. El usuario confirmó que las tres dificultades identificadas coexisten: justificar dotación o vacantes, entender la distribución de carga y planificar ante cambios del trabajo.

El alcance no incluye capacidad tecnológica, infraestructura, equipamiento, costos no laborales ni evaluación disciplinaria individual. Los archivos entregados bajo [DATOS/CAPACITY-ANALIZE](./DATOS/CAPACITY-ANALIZE/) son sintéticos, según confirmación expresa del usuario. Esto no aprueba su modelo ni sus fórmulas para uso real.

## Estado actual

El repositorio contiene documentación de diagnóstico y un kit sintético con una interfaz de demostración, funciones parciales de cálculo, un diccionario y pruebas aún no ejecutadas. El objetivo y alcance general están definidos; la definición funcional detallada sigue el LOOP v2 y está en el Bloque 1, Tema 1.1. Faltan datos sobre cómo se realiza hoy el proceso, el esfuerzo involucrado y sus fallas concretas.

No se deben iniciar nuevas funcionalidades de negocio ni fijar la arquitectura de producción hasta cerrar las definiciones necesarias del LOOP v2. La existencia de Streamlit y de fórmulas en el kit describe el prototipo entregado, no una selección tecnológica ni políticas aprobadas.

## Cómo continuar

1. Usar [DOCUMENTACION/11_ACOPLAMIENTO_LOOPS.md](./DOCUMENTACION/11_ACOPLAMIENTO_LOOPS.md) como guía de precedencia, estado integrado y registro de definiciones.
2. Continuar el levantamiento desde Bloque 1, Tema 1.1, sin saltar al siguiente tema hasta validar el registro o indicar `CONTINUAR CON PENDIENTE`.
3. Revisar [DOCUMENTACION/00_ESTADO_DEL_PROYECTO.md](./DOCUMENTACION/00_ESTADO_DEL_PROYECTO.md) para el tablero y [DOCUMENTACION/01_RECONSTRUCCION_HISTORICA.md](./DOCUMENTACION/01_RECONSTRUCCION_HISTORICA.md) y [DOCUMENTACION/02_AUDITORIA_TECNICA.md](./DOCUMENTACION/02_AUDITORIA_TECNICA.md) para las fuentes revisadas y los hallazgos.
4. Tratar las definiciones, reglas, criterios y tecnologías del kit como propuestas hasta que el usuario las valide conforme al loop.

## Documentación

- [Acoplamiento de loops y registro actual](./DOCUMENTACION/11_ACOPLAMIENTO_LOOPS.md)
- [Tablero del proyecto](./DOCUMENTACION/00_ESTADO_DEL_PROYECTO.md)
- [Reconstrucción histórica](./DOCUMENTACION/01_RECONSTRUCCION_HISTORICA.md)
- [Auditoría técnica](./DOCUMENTACION/02_AUDITORIA_TECNICA.md)
- [Requerimientos funcionales](./DOCUMENTACION/03_REQUERIMIENTOS_FUNCIONALES.md)
- [Reglas de negocio](./DOCUMENTACION/04_REGLAS_DE_NEGOCIO.md)
- [Criterios de aceptación](./DOCUMENTACION/05_CRITERIOS_DE_ACEPTACION.md)
- [Arquitectura](./DOCUMENTACION/06_ARQUITECTURA.md)
- [Modelo de datos](./DOCUMENTACION/07_MODELO_DE_DATOS.md)
- [Decisiones técnicas](./DOCUMENTACION/08_DECISIONES_TECNICAS.md)
- [Plan de desarrollo](./DOCUMENTACION/09_PLAN_DE_DESARROLLO.md)
- [Informe QA](./DOCUMENTACION/10_INFORME_QA.md)

## Pruebas y ejecución

Hay código de demostración y una suite bajo `DATOS/CAPACITY-ANALIZE/`, pero no se han ejecutado en este ciclo. Sus resultados y limitaciones están descritos en el informe QA. No se declara el producto listo para uso.
