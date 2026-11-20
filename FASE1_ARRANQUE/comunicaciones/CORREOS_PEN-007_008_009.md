# Borradores de correos · PEN-007, PEN-008, PEN-009

> **Borradores para revisar y enviar desde su propia cuenta.** No se envió ningún correo. Reemplace los textos entre corchetes y adjunte los documentos indicados.

---

## Correo 1 · Legal / Oficial de Protección de Datos (PEN-007)

**Para:** [Oficial de Protección de Datos]; [Gerencia Legal]
**Asunto:** Consulta sobre el tratamiento de datos personales en el piloto CAPACITY-ANALIZE

Estimado/a [nombre]:

La Vicepresidencia de Operaciones y Canales iniciará el piloto de **CAPACITY-ANALIZE**, una herramienta para medir la carga laboral y la capacidad disponible en FTE de unas 300 posiciones, con el fin de sustentar decisiones de dotación y vacantes.

El tratamiento previsto es el siguiente:

- **Datos:** dotación, fechas de ingreso y salida, jornada, horas de ausencia por categoría (vacaciones, enfermedad, permisos, licencias), capacitación, horas extra y movimientos de personal.
- **Medidas ya definidas:** seudonimización (la tabla que vincula seudónimo e identidad se queda en Talento Humano); sin nombres, cédulas, salarios ni diagnósticos médicos; reportes solo para grupos de 3 personas o más; detalle individual restringido a Capacity y Talento Humano; bitácora de auditoría.

Le solicitamos su criterio sobre:

1. ¿Qué normativa aplica (por ejemplo, la Ley Orgánica de Protección de Datos Personales y las normas internas o del supervisor)?
2. ¿Es suficiente la base legal de "gestión de la relación laboral y planificación organizacional" (SUP-006)?
3. ¿Se requiere una evaluación de impacto o un registro adicional del tratamiento?
4. ¿Debemos informar a los colaboradores? ¿Con qué texto?
5. ¿Hay alguna restricción para tratar las horas de ausencia por enfermedad, aunque se registren sin diagnóstico?

Adjunto: `DOCUMENTACION/15_BLOQUE4_PRIVACIDAD_ACCESOS_DESPLIEGUE_EXITO.md` (secciones 4.1 a 4.5).

Agradeceríamos su respuesta hasta el [fecha], para no retrasar el cronograma del piloto.

Saludos cordiales,
[Firma]

---

## Correo 2 · Seguridad de la Información (PEN-008)

**Para:** [Oficial de Seguridad de la Información]
**Asunto:** Clasificación y retención de datos para el piloto CAPACITY-ANALIZE

Estimado/a [nombre]:

Como parte del piloto de CAPACITY-ANALIZE (medición de la capacidad humana de la Vicepresidencia de Operaciones y Canales), necesitamos su orientación sobre:

1. **Clasificación** de la información. Nuestra propuesta es: horas de ausencia por enfermedad como "Confidencial sensible"; horas extra y movimientos por persona como "Confidencial"; resultados agregados por unidad como "Interno". ¿Es correcta según la política del banco?
2. **Plazo de retención** de los datos por colaborador-mes, de los resultados y de la bitácora de auditoría.
3. **Almacenamiento y transferencia** permitidos durante la fase 1, que trabaja con archivos CSV y Excel: ¿qué carpetas o repositorios están autorizados?
4. **Controles mínimos** para la fase 2 (aplicación web): autenticación, cifrado y registros de acceso.

Adjuntos: matriz de permisos y controles propuestos (documento 15, §4.4 y §4.5).

Quedo atento/a a su respuesta hasta el [fecha].

Saludos cordiales,
[Firma]

---

## Correo 3 · Tecnología / Arquitectura (PEN-009)

**Para:** [Gerencia de Tecnología]; [Arquitectura Empresarial]
**Asunto:** Restricciones de infraestructura para el futuro producto CAPACITY-ANALIZE

Estimado/a [nombre]:

El piloto de CAPACITY-ANALIZE (fase 1) funcionará con archivos y scripts de Python en modo de lotes. Para diseñar la **fase 2** (una aplicación web mínima, con unos 4 meses de desarrollo estimado) necesitamos conocer las restricciones de infraestructura **antes de elegir tecnología**.

1. ¿El producto debe ejecutarse en servidores propios o en una nube aprobada? ¿Cuál?
2. ¿Qué bases de datos relacionales están homologadas?
3. ¿Cuál es la política sobre librerías de código abierto (por ejemplo Python, pandas o frameworks web)?
4. ¿Está disponible el inicio de sesión único con el directorio institucional para aplicaciones internas? ¿Con qué protocolo?
5. ¿Hay restricciones de acceso desde fuera de la red o requisitos de VPN?
6. ¿Cuál es el proceso y el tiempo para aprobar una nueva aplicación interna?
7. ¿Existen sistemas de origen (core, nómina, centro de contacto) con extracciones automáticas disponibles para alimentar las fuentes?

Adjuntos: requerimientos no funcionales RNF-01 a RNF-12 y arquitectura funcional (documento 16, §15 y §18).

Agradeceríamos una reunión de 45 minutos antes del [fecha].

Saludos cordiales,
[Firma]
