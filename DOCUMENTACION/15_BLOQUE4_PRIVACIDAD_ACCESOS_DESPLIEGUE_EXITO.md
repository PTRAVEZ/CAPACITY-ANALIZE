# 15 · LOOP v2.1 — Bloque 4: Privacidad, accesos, despliegue y criterios de éxito

> **Contexto:** el usuario aprobó el Bloque 3 en el chat el 2026-11-20. Pasan a *Confirmado* RN-01 a RN-07, IND-01 a IND-21 y DEC-027 a DEC-029, y quedan aprobados para el piloto PAR-001, PAR-002, PAR-004 y PAR-005.
> Todo lo de este bloque queda *Propuesto* o *Supuesto*. La normativa citada es **referencial** y debe validarla Legal / Cumplimiento (regla 10 del LOOP). Este bloque describe **cómo opera** el producto; no amplía el análisis hacia la capacidad tecnológica.

## 4.1 Nivel de identificación y agregación

| ID | Estado | Descripción |
|---|---|---|
| DEC-030 | Propuesto | El producto trabaja con datos **seudonimizados** (DEC-025). Ninguna pantalla ni reporte muestra nombres ni cédulas. |
| DEC-031 | Propuesto | **Reportes:** solo se muestran agregados de unidad × cargo con al menos 3 personas (PAR-006). Los grupos menores se agregan al nivel superior (unidad o gerencia). |
| DEC-032 | Propuesto | El detalle por colaborador-mes (disponibilidad, ausencias, horas extra) solo lo consultan USR-01 (Capacity) y USR-04 (Talento Humano), para validar y conciliar. |
| PAR-006 | Propuesto (requiere aprobación) | Agregación mínima de 3 personas. |

## 4.2 Información confidencial y restricciones especiales

| Dato | Clasificación propuesta | Tratamiento |
|---|---|---|
| Ausencias por enfermedad y licencias | **Confidencial sensible** (relacionada con salud) | Solo horas por categoría, sin diagnóstico (DEC-026); se ve únicamente agregada fuera de USR-01 y USR-04 |
| Horas extra por persona | Confidencial | Agregada por unidad × cargo en los reportes |
| Movimientos (salidas y motivo) | Confidencial | Agregados; el motivo solo para Talento Humano |
| Carga, FTE y utilización por unidad | Interno | Según el alcance de cada perfil (4.4) |
| Escenarios 2027 | Interno restringido | Comité, Vicepresidencia y Capacity |
| Salarios y costos | **Excluido** del producto | Fuera de alcance (LOOP §1.1) |

## 4.3 Normativa y políticas (a validar)

| ID | Estado | Descripción |
|---|---|---|
| PEN-007 | Pendiente | Confirmar con Legal / Cumplimiento qué normativa aplica, por ejemplo la protección de datos personales en Ecuador (LOPDP) y las normas del supervisor bancario sobre seguridad de la información. Definir si se requiere una evaluación de impacto. Responsable: Oficial de Protección de Datos. |
| PEN-008 | Pendiente | Confirmar la política interna de clasificación de la información y los plazos de retención de los datos de capacidad. Responsable: Seguridad de la Información. |
| SUP-006 | Supuesto | Base legal del tratamiento: gestión de la relación laboral y planificación organizacional, con datos minimizados y seudonimizados. |

## 4.4 Matriz de permisos (C = consultar, R = registrar, M = modificar, V = validar, A = aprobar)

| Perfil | Alcance de datos | Fuentes del sistema | Volúmenes y reprocesos manuales | Catálogo de actividades y tiempos | Parámetros y escenarios | Resultados del período | Detalle por persona | Usuarios y configuración |
|---|---|---|---|---|---|---|---|---|
| USR-07 Administrador funcional | Configuración | — | — | — | — | — | — | C R M |
| USR-01 Analista de Capacity | Todo el piloto | C R M | C V | C R M | C R M (borrador) | C (calcula) | C | — |
| USR-04 Talento Humano | Todo el piloto | C R (dotación, ausentismo, horas extra, movimientos, vacantes) V (conciliación) | — | C | C | C | C | — |
| USR-02 Jefatura | Su unidad | C (su unidad) | C R M (hasta el cierre) | C V (su unidad) | — | C (su unidad) | — | — |
| USR-03 Gerente de área | Su gerencia | — | C | C | C | C V (su gerencia) | — | — |
| USR-05 Comité de Capacidad | Todo el piloto | — | — | C A (cambios del catálogo) | C A | C A (cierre del período) | — | — |
| USR-06 Consulta ejecutiva | Agregado | — | — | — | C | C (agregado) | — | — |

| ID | Estado | Descripción |
|---|---|---|
| DEC-033 | Propuesto | Se adopta la matriz de permisos anterior. Principios: mínimo privilegio y **segregación de funciones** (quien registra no aprueba lo mismo). |
| DEC-034 | Propuesto | Si una persona tiene dos perfiles (por ejemplo, gerente e integrante del Comité), no puede aprobar resultados de su propia gerencia: se abstiene en el Comité. |

## 4.5 Auditoría, trazabilidad y cierre de períodos

| ID | Estado | Descripción |
|---|---|---|
| DEC-035 | Propuesto | **Bitácora de auditoría** de cada alta, cambio o borrado: usuario, fecha y hora, objeto, valor anterior, valor nuevo y motivo. Es inmutable y se conserva según PEN-008. |
| DEC-036 | Propuesto | **Ciclo del período:** Abierto → Cargado → Validado (V-01 a V-16 sin errores bloqueantes) → Revisado por los gerentes → Aprobado por el Comité → **Cerrado y congelado**. Un período cerrado no se modifica; una corrección genera una nueva versión con su motivo. |
| DEC-037 | Propuesto | **Reproducibilidad:** cada período cerrado guarda una copia de los insumos, de los parámetros vigentes y de la versión del motor de cálculo, para reproducir sus resultados exactos. |
| DEC-038 | Propuesto | Se registra quién consulta el detalle por persona (DEC-032). |

## 4.6 Condiciones de operación (sin elegir tecnología todavía)

| ID | Estado | Descripción |
|---|---|---|
| DEC-039 | Propuesto | Aplicación **web** con acceso por navegador; sin instalación en los equipos de los usuarios. |
| DEC-040 | Propuesto | Autenticación con la **identidad institucional** (inicio de sesión único con el directorio del banco) y asignación de perfiles por grupos del directorio. |
| DEC-041 | Propuesto | Importación de las fuentes en CSV o Excel con validación automática; exportación de resultados a Excel; tableros y reportes según 3.4. |
| DEC-042 | Propuesto | Base de datos relacional para las fuentes, los resultados, la bitácora y las versiones de los períodos. |
| PEN-009 | Pendiente | Restricciones reales de infraestructura: ¿servidor propio del banco o nube aprobada?, ¿bases de datos permitidas?, ¿política de librerías de código abierto?, ¿acceso desde fuera de la red? Responsable: Tecnología / Arquitectura. **La tecnología se selecciona solo cuando esto se resuelva** (regla 6 del LOOP). |
| SUP-007 | Supuesto | El prototipo Streamlit existente y el motor demostrativo en Python sirven para **validar la metodología**, no como decisión de tecnología para producción. |

## 4.7 Criterios de éxito y aceptación (CA-)

| ID | Criterio | Métrica y método de verificación | Meta propuesta | Prueba automática en el demo |
|---|---|---|---|---|
| CA-01 | Exactitud de la carga | Recalcular Σ volumen × tiempo + reprocesos con un cálculo independiente | Diferencia 0 (tolerancia ±0,01 h) | `test_ca01` ✔ |
| CA-02 | Conciliación de dotación | Dotación inicial + ingresos − salidas = dotación a la fecha de corte (V-15) | 100 % conciliado | `test_ca02` ✔ |
| CA-03 | Sin doble conteo de ausencias | FTE disponible = FTE contractual × (1 − tasa de indisponibilidad) | Identidad exacta | `test_ca03` ✔ |
| CA-04 | Integridad de las horas | Ausencias + capacitación ≤ horas nominales; horas disponibles ≥ 0 | 100 % de los registros | `test_ca04` ✔ |
| CA-05 | Detección de errores de datos | Las anomalías sembradas se detectan | 7 de 7 | `test_ca05` ✔ |
| CA-06 | Coherencia de agregación | La suma por gerencia es igual a la suma por unidad × cargo | Diferencia 0 | `test_ca06` ✔ |
| CA-07 | Trazabilidad | Cada indicador publicado se rastrea hasta sus filas de origen y su versión de parámetros | 100 % de una muestra de 20 | Manual |
| CA-08 | Identificación de brechas | El sistema identifica las unidad × cargo con sobrecarga ≥ 6 meses del año | Coincide con la revisión del analista en ≥ 95 % | Manual |
| CA-09 | Reducción del trabajo manual | Horas-persona del ciclo de planificación frente a la línea base SUP-001 (≈ 400 h) | −50 % el primer año | Medición del piloto |
| CA-10 | Oportunidad | Resultados del mes disponibles | Día hábil 10 (DEC-018) | Medición del piloto |
| CA-11 | Facilidad de uso | Encuesta a jefaturas y gerentes (escala SUS) | ≥ 70 puntos | Encuesta |
| CA-12 | Cumplimiento de permisos | Pruebas de acceso por perfil (cada perfil intenta ver datos fuera de su alcance) | 0 accesos indebidos | Prueba de seguridad |
| CA-13 | Reproducibilidad | Recalcular un período cerrado da los mismos resultados | Diferencia 0 | Prueba automática (fase 2) |
| CA-14 | Tiempo de decisión de vacantes | Días desde la solicitud hasta la decisión frente a SUP-002 (≈ 45) | ≤ 20 días | Medición del piloto |

| ID | Estado | Descripción |
|---|---|---|
| DEC-043 | Propuesto | Se adoptan CA-01 a CA-14. Las metas son propuestas y debe aprobarlas el Comité de Capacidad. |

---

## Resumen del Bloque 4

- ✅ **Confirmado (Bloque 3):** RN-01 a RN-07, IND-01 a IND-21, DEC-027 a DEC-029, y PAR-001, 002, 004 y 005 aprobados para el piloto.
- 💡 **Propuesto:** DEC-030 a DEC-043, la matriz de permisos y CA-01 a CA-14.
- ⚠️ **Supuestos:** SUP-006 (base legal) y SUP-007 (el prototipo no es la tecnología final).
- ⏳ **Pendiente:** PEN-004 (Comité), PEN-005 y 006 (mediciones), PEN-007 (normativa), PEN-008 (retención) y PEN-009 (infraestructura).
- 🔗 **Impacto:** con este bloque, las cuatro definiciones del LOOP quedan completas y se puede generar el **Documento de Definición de Requerimientos**.
- 🧾 **Decisiones que el usuario debe aprobar:** seudonimización y agregación mínima (DEC-030 a 032, PAR-006), matriz de permisos (DEC-033 y 034), auditoría y cierre de períodos (DEC-035 a 038), condiciones de operación (DEC-039 a 042) y criterios de aceptación (DEC-043).

**Verificación de coherencia:** la matriz de permisos respeta los roles R/V/A/C del Bloque 1 (DEC-015). La privacidad respeta DEC-025 y 026. Los criterios CA-01 a 06 ya se verifican con las pruebas automáticas del demostrador.
