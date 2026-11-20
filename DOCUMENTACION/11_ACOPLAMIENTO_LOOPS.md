# 11. Acoplamiento de loops y registro vigente

**Versión:** 1.1
**Actualizado:** 2026-11-20
**Estado:** EN ANÁLISIS
**Fase activa:** LOOP de requerimientos v2 · Bloque 1 · Tema 1.1

## 1. Propósito de este documento

Este documento conecta el LOOP de descubrimiento y auditoría inicial, el LOOP de requerimientos v2 y el kit de datos/prototipo ubicado en `DATOS/CAPACITY-ANALIZE/`. Sirve como referencia de control para que el mismo término, dato o fórmula no cambie de significado entre conversaciones y archivos.

El adjunto “Pasted text #1” mencionado en la conversación no estuvo disponible en la ruta local indicada. Por tanto, este acoplamiento incorpora el LOOP v2 visible en la conversación y los artefactos accesibles del repositorio; no declara haber leído ni integrado reglas particulares del adjunto. Cuando se comparta su contenido en una ubicación accesible, se comparará contra este documento sin editar el snapshot de solo lectura.

## 2. Orden de autoridad y precedencia

Cuando dos fuentes difieran, se aplicará este orden:

1. Decisión explícita y validada por el usuario, con su ID en el registro.
2. LOOP de requerimientos v2 para orden de preguntas, estados, alcance, validación y puertas de avance.
3. Evidencia observable del repositorio, datos y código, descrita como hecho técnico y no como regla del negocio.
4. Documentación inicial del kit y su prompt maestro, tratados como propuestas hasta validación.
5. Hipótesis analítica del consultor, etiquetada como hipótesis/propuesta y nunca como requisito aprobado.

El usuario también pidió una reconstrucción histórica, auditoría técnica, documentación, trazabilidad y validación real antes de declarar éxito. Estas tareas se conservan, pero se ordenan con el proceso iterativo del LOOP v2. La solicitud anterior de “implementar” no elimina la puerta v2 que prohíbe programar funciones de negocio y seleccionar tecnologías antes de conocer las restricciones reales.

### Precedencia de instrucciones frente al kit

| Fuente | Aporte útil | Estado / límite |
|---|---|---|
| LOOP v2 del usuario | Define alcance de capacidad humana, los cuatro bloques, preguntas de una en una, estados y trazabilidad. | Guía funcional vigente. El avance por tema espera validación, salvo `CONTINUAR CON PENDIENTE`. |
| Prompt inicial de auditoría/reconstrucción | Exige inspección, documentación, control de cambios y evidencia de QA. | Vigente para el trabajo técnico, subordinado a las puertas funcionales del LOOP v2. |
| `DATOS/CAPACITY-ANALIZE/prompts/LOOP_MAESTRO_CODEX.md` | Propone fases de implementación, ingeniería y un stack Streamlit/Python. | Propuesta del kit, no autorización vigente para seleccionar tecnología o programar el producto. Su stack contradice la espera del Bloque 4; prevalece el LOOP v2. |
| `DATOS/CAPACITY-ANALIZE/docs/DEFINICION_FUNCIONAL.md` | Propone usuarios, módulos y flujo de trabajo. | Hipótesis/propuestas iniciales, no requerimientos confirmados. |
| `DATOS/CAPACITY-ANALIZE/docs/REGLAS_DE_NEGOCIO.md` y `src/calculations.py` | Proponen definiciones y codifican parte de las fórmulas. | Las fórmulas están implementadas parcialmente, pero no son política aprobada ni resultado validado. `RN-001` sigue Propuesto. |
| `DATOS/CAPACITY-ANALIZE/docs/CRITERIOS_ACEPTACION.md` | Lista criterios iniciales verificables. | Propuestos; deben recibir IDs `CA-`, meta, responsable y aprobación conforme al Bloque 4. |

## 3. Alcance consolidado

### Confirmado

- CAPACITY-ANALIZE busca analizar capacidad humana para un banco privado: trabajo, carga, actividades, volúmenes, tiempos, disponibilidad y necesidades de FTE.
- Los tres síntomas mencionados por el usuario coexisten: dificultad para justificar dotación/vacantes; poca visibilidad de distribución de carga; y planificación que no refleja bien cambios del trabajo.
- El usuario confirmó que todos los datos de `DATOS/` son sintéticos y que no existe un problema de identidad real en ellos.
- El límite de alcance del LOOP v2 permanece: no incorporar capacidad tecnológica, infraestructura, equipamiento, costos no laborales ni evaluación individual con fines disciplinarios.

### No confirmado / no debe inferirse

- Que los nombres de países, bancos, ciudades o colaboradores que aparecen en archivos sintéticos reflejen una institución o regulación real.
- Que un cargo, proceso, unidad o estructura propuestos en el kit existan en el banco del usuario.
- Que una fórmula, valor de parámetro, umbral, proyección, escenario, usuario o permiso del kit sea política del banco.
- Que el prototipo Streamlit sea la tecnología objetivo o esté listo para producción.
- Que se autorice desplegar, acceder a sistemas reales o incurrir en costos.

## 4. Registro de definiciones conocido

Cada entrada mantiene fuente, estado y relación. Las fechas/turnos que no aparecen en el historial disponible se registrarán cuando se valide el siguiente mensaje, sin inventar una fecha histórica exacta.

| ID | Estado | Descripción | Fuente | Relacionados |
|---|---|---|---|---|
| DEC-001 | Confirmado | El objeto es analizar capacidad humana en un banco privado dentro de los límites del LOOP v2. | Usuario: prompt v2 | RF/RNF y bloques 1–4 por definir |
| DEC-002 | Confirmado | Los archivos aportados en `DATOS/` contienen datos sintéticos, sin identidad real. | Usuario: confirmación explícita | FTE-SRC y DAT por perfilar y validar |
| DEC-003 | Confirmado | Coexisten los síntomas A, B y C señalados por el usuario: justificación de dotación/vacantes, visibilidad de distribución de carga y planificación ante cambios de trabajo. | Usuario: respuesta “A, B, C” | PEN-001; temas 1.2–1.4 |
| RN-001 | Propuesto | Las fórmulas del kit, incluidos sus parámetros, no son reglas oficiales aprobadas; necesitan validación funcional y un aprobador. | Propuesta derivada del kit y LOOP v2 | Bloque 3; PAR/IND/RN |
| PEN-001 | Pendiente | Describir cómo se atienden hoy los tres problemas, con qué esfuerzo, qué falla y cuál es su impacto. Responsable sugerido: dueño del proceso / usuario. | Falta de respuesta de detalle en Tema 1.1 | DEC-003; tema 1.2 |
| RSK-001 | Pendiente de validación | En el perfil preliminar se registran 110 filas de volumen y 110 de reproceso que no encuentran agencia bajo las relaciones inferidas por los nombres de campos. La hipótesis de llave o cardinalidad puede ser incorrecta. | Perfil preliminar del kit; inferencia técnica no validada | FTE-SRC de volúmenes/reprocesos; DAT de llaves |

No se declara todavía un glosario `GLO-` confirmado, ni perfiles `USR-`, fuentes `FTE-SRC-`, campos `DAT-`, indicadores `IND-`, parámetros `PAR-`, requerimientos `RF-/RNF-` o criterios `CA-` confirmados. Deben generarse y validarse en el bloque correspondiente.

## 5. Estado de avance del proceso de preguntas

La respuesta “A, B, C” dejó registrado que coexisten los tres síntomas propuestos. No completa por sí sola el resto de 1.1. El primer tema del LOOP pide comprender el estado actual y sus fallas; siguen faltando:

- cómo se justifica actualmente una dotación o vacante;
- cómo se observa actualmente la distribución de carga;
- cómo se planifica frente a cambios de trabajo;
- qué esfuerzo y fallas ocurren y qué impacto generan.

El próximo turno de levantamiento debe hacer **una sola pregunta principal** que recoja ese detalle, con opciones breves si ayudan. Después se debe reflejar qué se entendió, señalar vacíos, proponer el registro con ID y esperar “Sí / Ajustar / Dejar pendiente”. No abrir el Tema 1.2 hasta su validación o hasta que el usuario indique `CONTINUAR CON PENDIENTE`.

Los comandos del LOOP v2 se conservan: `ESTADO`, `RESUMEN`, `NO SÉ`, `CONTINUAR CON PENDIENTE`, `SALTAR A X.Y`, `VOLVER A X.Y`, `CAMBIO DEC-xxx`, `PAUSA`, `RETOMAR` y `GENERAR DOCUMENTO`.

## 6. Inventario integrado de lo existente

| Artefacto / hallazgo | Evidencia actual | Tratamiento en el loop |
|---|---|---|
| Datos de entrada | 15 CSV bajo `DATOS/CAPACITY-ANALIZE/data/input/` y un libro XLSX consolidado; se presentan como sintéticos. | Bloque 2: inspeccionar estructura, nulos, duplicados, unidades, granularidad y llaves; registrar fichas `FTE-SRC-` y `DAT-`. No asumir que el diccionario preliminar ya está validado. |
| Diccionario de datos | `data/reference/diccionario_datos.csv`; las definiciones de campo se marcan como pendientes de validación. | Borrador de hipótesis para revisión del dueño de datos; no convertir sus descripciones en semántica confirmada. |
| Perfil de calidad | `data/reference/perfil_inicial_datos.csv` declara cero nulos en todos los archivos. El análisis previo detectó 14 valores vacíos en `bridge_actividad_cargo.csv`, campo `vigente_hasta`, por lo que existe una discrepancia que debe conciliarse. | Incidencia de calidad pendiente; no ocultar ni resolver por imputación sin aprobación. |
| Volúmenes y tiempos | `workload_hours` exige `nivel_complejidad`; esa columna no aparece en `fact_volumenes_mensuales.csv`. | Incompatibilidad técnica/dato pendiente de definición: aclarar si falta la variable, si debe derivarse o si el método de cálculo debe cambiar. No inventar el vínculo. |
| Relaciones con agencias | Se reportaron 110 filas sin correspondencia al unir según las claves que parecen sugerir los nombres de campo. | `RSK-001`: validar primero llaves y cardinalidad con el responsable; no clasificar automáticamente como defectos del dato. |
| Código existente | `app.py` muestra un panel de demostración; `src/calculations.py` implementa funciones parciales para tiempo estándar, carga, horas efectivas, FTE requerido y brecha. | Se conserva como prototipo. No asumir cobertura de todos los indicadores, reglas o flujos descritos en el kit. |
| Pruebas existentes | Existe `tests/test_calculations.py`. | No se han ejecutado en este ciclo; resultado: pendiente, no aprobado ni fallido. |
| Interfaz / stack | El prototipo usa Streamlit y pandas, con dependencias en `requirements.txt`. | Hecho técnico existente; decisión de producción pendiente del Bloque 4. |
| Parámetros | `parametros_modelo.csv` contiene parámetros descritos como ilustrativos. | No usar como valores aprobados; cada uno requiere `PAR-`, unidad, responsable y confirmación. |
| País y regulación | El README del kit menciona Ecuador como contexto ficticio. | No asumir jurisdicción aplicable. Consultar país y políticas aplicables en Bloque 4 y dejar validación con Legal/Cumplimiento cuando corresponda. |
| Git | Al comenzar este ciclo, la rama `main` tenía dos commits locales por delante de `origin/main`; `DATOS/` aparecía sin seguimiento. | Se preserva todo el contenido. No ejecutar limpieza, reset, borrado ni commit de los datos del usuario sin revisar el alcance. |

## 7. Puertas de avance

| Puerta | Condición de salida |
|---|---|
| Cerrar Tema 1.1 | Método actual, esfuerzo, fallas e impacto registrados; respuesta validada o marcada Pendiente explícitamente. |
| Cerrar Bloque 1 | Proceso, decisiones, usuarios/roles, niveles, levantamiento y periodicidad confirmados o pendientes con responsable. |
| Cerrar Bloque 2 | Cada variable prioritaria tiene fuente o método de recolección, llave, calidad y significado validado/propuesto claramente distinguido. |
| Cerrar Bloque 3 | Taxonomía de tiempo y anti-doble-conteo validadas; fichas de indicadores y parámetros con aprobadores. |
| Cerrar Bloque 4 | Privacidad, accesos, operación y criterios de éxito definidos o asignados como pendientes con responsable. |
| Iniciar diseño técnico / desarrollo | Requerimientos y restricciones relevantes confirmados; tecnología elegida con justificación; criterios de aceptación disponibles. |
| Declarar producto validado | Instalación/ejecución y pruebas requeridas realmente ejecutadas; fallos e incidencias registrados; no quedan requisitos críticos sin resolver. |

## 8. Actividades pendientes y decisiones de usuario

1. Compartir el texto del adjunto “Pasted text #1” en el chat o en una ruta que esté disponible al espacio de trabajo, para integrar sus instrucciones específicas.
2. Completar Tema 1.1 con la descripción de cómo se trabaja hoy, esfuerzo, fallas e impacto, y validar el registro resultante.
3. Más adelante, cuando el LOOP alcance Bloque 4, definir jurisdicción/políticas, privacidad, permisos y restricciones de despliegue; no hace falta decidir tecnología en esta etapa.

## 9. Historial de acoplamiento

| Versión | Cambio |
|---|---|
| 1.0 | Integrados el LOOP v2 visible, decisiones confirmadas en conversación, inventario del kit sintético, precedencia entre documentos, discrepancias conocidas y puertas de avance. El adjunto externo sigue pendiente de lectura. |
| 1.1 | Añadida una nota de precedencia al prompt maestro existente del kit, que lo subordina al proceso v2 y marca el stack como propuesta. |
