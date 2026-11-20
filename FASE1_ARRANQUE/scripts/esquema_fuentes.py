"""
Esquema oficial de las 14 fuentes de CAPACITY-ANALIZE (DEC-019 a DEC-021).

Es la ÚNICA definición de columnas, tipos y valores permitidos. La usan:
  - generar_plantillas.py  → crea las plantillas Excel de carga
  - validar_carga.py       → revisa una carga real antes del cálculo

Tipos: id | texto | fecha (AAAA-MM-DD) | periodo (AAAA-MM) | entero | decimal | sn (S/N) | lista
"""

ENUMS = {
    "nivel": ["Banco", "Dirección", "Gerencia", "Departamento", "Agencia"],
    "nivel_jerarquico": ["Gerencial", "Jefatura", "Supervisión", "Profesional", "Operativo"],
    "tipo_rol": ["Gestión", "Supervisión", "Operativo", "Comercial", "Soporte"],
    "tipo_contrato": ["Indefinido", "Eventual", "Otro"],
    "modalidad": ["Presencial", "Híbrida", "Remota"],
    "estado_parametro": ["Supuesto", "Propuesto", "Aprobado (piloto)", "Aprobado"],
    "metodo_medicion": ["Estudio de tiempos", "Registro de sistema", "Muestreo de trabajo",
                        "Estimación experta", "Bitácora de gestión", "Pendiente de medición"],
    "tipo_actividad": ["Core", "Soporte", "Gestión"],
    "tipo_movimiento": ["INGRESO", "SALIDA"],
    "motivo_vacante": ["Reemplazo", "Nueva posición"],
    "estado_vacante": ["Abierta", "Cubierta", "Cancelada"],
    "ambito_tipo": ["GLOBAL", "PROCESO", "ACTIVIDAD"],
    "variable_escenario": ["volumen_pct", "tiempo_pct"],
    "estado_escenario": ["Supuesto", "Propuesto", "Aprobado"],
}


def c(nombre, tipo, req=True, desc="", ejemplo="", lista=None, minimo=None, maximo=None):
    return {"nombre": nombre, "tipo": tipo, "requerido": req, "descripcion": desc,
            "ejemplo": ejemplo, "lista": lista, "min": minimo, "max": maximo}


FUENTES = {
    "01_estructura_organizacional.csv": {
        "id": "FTE-SRC-01", "titulo": "Estructura organizacional", "dueno": "Talento Humano / Organización y Métodos",
        "llave": ["unidad_id"],
        "columnas": [
            c("unidad_id", "id", desc="Código único de la unidad", ejemplo="DEP-PAG"),
            c("nombre", "texto", desc="Nombre de la unidad", ejemplo="Departamento de Pagos y Transferencias"),
            c("nivel", "lista", desc="Nivel organizacional", ejemplo="Departamento", lista="nivel"),
            c("unidad_padre_id", "id", req=False, desc="Unidad de la que depende (vacío solo para el nivel Banco)", ejemplo="GER-OPC"),
            c("ciudad", "texto", desc="Ciudad", ejemplo="Quito"),
            c("provincia", "texto", desc="Provincia", ejemplo="Pichincha"),
            c("tipo_unidad", "texto", desc="Back office, Agencia, Centro de contacto, etc.", ejemplo="Back office"),
        ]},
    "02_cargos.csv": {
        "id": "FTE-SRC-02", "titulo": "Catálogo de cargos", "dueno": "Talento Humano", "llave": ["cargo_id"],
        "columnas": [
            c("cargo_id", "id", desc="Código único del cargo", ejemplo="CAR-CAJ"),
            c("nombre_cargo", "texto", desc="Nombre del cargo", ejemplo="Cajero"),
            c("familia", "texto", desc="Familia de puestos", ejemplo="Red de agencias"),
            c("nivel_jerarquico", "lista", desc="Nivel jerárquico", ejemplo="Operativo", lista="nivel_jerarquico"),
            c("tipo_rol", "lista", desc="Tipo de rol", ejemplo="Operativo", lista="tipo_rol"),
        ]},
    "03_colaboradores.csv": {
        "id": "FTE-SRC-03", "titulo": "Colaboradores (SEUDONIMIZADOS)", "dueno": "Talento Humano (nómina)", "llave": ["colaborador_id"],
        "columnas": [
            c("colaborador_id", "id", desc="Seudónimo. NUNCA cédula ni nombre (DEC-025)", ejemplo="COL-0001"),
            c("unidad_id", "id", desc="Unidad asignada (debe existir en 01)", ejemplo="AG-QMA"),
            c("cargo_id", "id", desc="Cargo (debe existir en 02)", ejemplo="CAR-CAJ"),
            c("fecha_ingreso", "fecha", desc="Primer día en el cargo y la unidad", ejemplo="2019-03-01"),
            c("fecha_salida", "fecha", req=False, desc="Último día laborado; vacío si está activo", ejemplo=""),
            c("tipo_contrato", "lista", desc="Tipo de contrato", ejemplo="Indefinido", lista="tipo_contrato"),
            c("jornada_horas_semana", "decimal", desc="Horas contractuales por semana (40 = completa)", ejemplo="40", minimo=1, maximo=40),
            c("modalidad", "lista", desc="Modalidad de trabajo", ejemplo="Presencial", lista="modalidad"),
        ]},
    "04_calendario_laboral.csv": {
        "id": "FTE-SRC-04", "titulo": "Calendario laboral", "dueno": "Talento Humano", "llave": ["fecha"],
        "columnas": [
            c("fecha", "fecha", desc="Día calendario (todos los días del período)", ejemplo="2027-01-04"),
            c("periodo", "periodo", desc="Mes AAAA-MM", ejemplo="2027-01"),
            c("dia_semana", "texto", desc="Nombre del día", ejemplo="lunes"),
            c("es_laborable", "sn", desc="S = día hábil", ejemplo="S"),
            c("feriado", "texto", req=False, desc="Nombre del feriado oficial, si aplica", ejemplo=""),
        ]},
    "05_parametros.csv": {
        "id": "FTE-SRC-05", "titulo": "Parámetros", "dueno": "Comité de Capacidad", "llave": ["parametro_id"],
        "columnas": [
            c("parametro_id", "id", desc="Identificador PAR-", ejemplo="PAR-001"),
            c("nombre", "texto", desc="Nombre técnico (no cambiar los existentes)", ejemplo="horas_jornada_diaria"),
            c("valor", "texto", desc="Valor", ejemplo="8"),
            c("unidad", "texto", desc="Unidad", ejemplo="horas/día"),
            c("estado", "lista", desc="Estado de aprobación", ejemplo="Aprobado (piloto)", lista="estado_parametro"),
            c("descripcion", "texto", desc="Significado", ejemplo="Horas de jornada completa"),
            c("aprobador_sugerido", "texto", desc="Quién aprueba", ejemplo="Comité de Capacidad"),
        ]},
    "06_procesos.csv": {
        "id": "FTE-SRC-06", "titulo": "Procesos", "dueno": "Procesos y Calidad", "llave": ["proceso_id"],
        "columnas": [
            c("proceso_id", "id", desc="Código del proceso", ejemplo="P-CAJ"),
            c("nombre_proceso", "texto", desc="Nombre", ejemplo="Atención en caja"),
            c("macroproceso", "texto", desc="Agrupación superior", ejemplo="Canales presenciales"),
            c("cargo_dueno_proceso", "id", desc="Cargo responsable (debe existir en 02)", ejemplo="CAR-JAG"),
            c("grupo_estacional", "texto", req=False, desc="Patrón estacional (referencial)", ejemplo="caja"),
        ]},
    "07_actividades.csv": {
        "id": "FTE-SRC-07", "titulo": "Actividades y tiempos estándar", "dueno": "Capacity Management (validan jefaturas)", "llave": ["actividad_id"],
        "columnas": [
            c("actividad_id", "id", desc="Código único de la actividad", ejemplo="ACT-001"),
            c("proceso_id", "id", desc="Proceso (uno solo, RN-04)", ejemplo="P-CAJ"),
            c("nombre_actividad", "texto", desc="Descripción", ejemplo="Depósito en efectivo o cheque"),
            c("cargo_id", "id", desc="Cargo que la ejecuta (uno solo, RN-04)", ejemplo="CAR-CAJ"),
            c("unidad_trabajo", "texto", desc="Qué se cuenta: transacción, expediente, llamada, hora...", ejemplo="transacción"),
            c("tiempo_estandar_min", "decimal", desc="Minutos por unidad, SIN reprocesos", ejemplo="2.1", minimo=0, maximo=10000),
            c("tiempo_reproceso_min", "decimal", desc="Minutos adicionales por unidad reprocesada", ejemplo="1.5", minimo=0, maximo=10000),
            c("metodo_medicion", "lista", desc="Cómo se obtuvo el tiempo (DEC-024)", ejemplo="Estudio de tiempos", lista="metodo_medicion"),
            c("fecha_medicion", "fecha", req=False, desc="Fecha de la medición", ejemplo="2027-02-15"),
            c("ambito", "texto", desc="AGENCIA, GERENCIA, DEPTO o un unidad_id", ejemplo="AGENCIA"),
            c("tipo_actividad", "lista", desc="Core, Soporte o Gestión", ejemplo="Core", lista="tipo_actividad"),
        ]},
    "08_volumenes_mensuales.csv": {
        "id": "FTE-SRC-08", "titulo": "Volúmenes mensuales", "dueno": "Operaciones / Centro de Contacto / jefaturas",
        "llave": ["periodo", "unidad_id", "actividad_id"],
        "columnas": [
            c("periodo", "periodo", desc="Mes AAAA-MM", ejemplo="2027-01"),
            c("unidad_id", "id", desc="Unidad que ejecutó el trabajo", ejemplo="AG-QMA"),
            c("actividad_id", "id", desc="Actividad (debe existir en 07)", ejemplo="ACT-001"),
            c("volumen", "entero", desc="Unidades de trabajo DE PRIMERA VEZ (sin reprocesos, RN-03)", ejemplo="12033", minimo=0),
            c("fuente", "texto", desc="Origen del dato", ejemplo="Core bancario / sistema transaccional"),
        ]},
    "09_reprocesos.csv": {
        "id": "FTE-SRC-09", "titulo": "Reprocesos", "dueno": "Jefaturas", "llave": ["periodo", "unidad_id", "actividad_id"],
        "columnas": [
            c("periodo", "periodo", desc="Mes AAAA-MM", ejemplo="2027-01"),
            c("unidad_id", "id", desc="Unidad", ejemplo="AG-QMA"),
            c("actividad_id", "id", desc="Actividad", ejemplo="ACT-001"),
            c("cantidad_reprocesos", "entero", desc="Unidades rehechas (≤ volumen del mes)", ejemplo="106", minimo=0),
            c("causa_principal", "texto", desc="Causa más frecuente del mes", ejemplo="Error de digitación"),
        ]},
    "10_ausentismo.csv": {
        "id": "FTE-SRC-10", "titulo": "Ausentismo y capacitación (SIN diagnósticos)", "dueno": "Talento Humano", "llave": ["colaborador_id", "periodo"],
        "columnas": [
            c("colaborador_id", "id", desc="Seudónimo", ejemplo="COL-0001"),
            c("periodo", "periodo", desc="Mes AAAA-MM", ejemplo="2027-01"),
            c("horas_vacaciones", "decimal", desc="Horas de vacaciones gozadas", ejemplo="0", minimo=0, maximo=744),
            c("horas_enfermedad", "decimal", desc="Horas de ausencia por enfermedad (sin diagnóstico, DEC-026)", ejemplo="0", minimo=0, maximo=744),
            c("horas_permisos", "decimal", desc="Horas de permisos", ejemplo="0", minimo=0, maximo=744),
            c("horas_licencias", "decimal", desc="Horas de licencias prolongadas", ejemplo="0", minimo=0, maximo=744),
            c("horas_capacitacion", "decimal", desc="Horas de capacitación institucional", ejemplo="4", minimo=0, maximo=744),
        ]},
    "11_horas_extra.csv": {
        "id": "FTE-SRC-11", "titulo": "Horas extra", "dueno": "Talento Humano (nómina)", "llave": ["colaborador_id", "periodo"],
        "columnas": [
            c("colaborador_id", "id", desc="Seudónimo", ejemplo="COL-0002"),
            c("periodo", "periodo", desc="Mes AAAA-MM", ejemplo="2027-01"),
            c("horas_suplementarias", "decimal", desc="Horas adicionales en días laborables", ejemplo="3", minimo=0, maximo=200),
            c("horas_extraordinarias", "decimal", desc="Horas en días de descanso o feriados", ejemplo="4", minimo=0, maximo=200),
        ]},
    "12_movimientos_personal.csv": {
        "id": "FTE-SRC-12", "titulo": "Movimientos de personal", "dueno": "Talento Humano", "llave": ["movimiento_id"],
        "columnas": [
            c("movimiento_id", "id", desc="Identificador", ejemplo="MOV-001"),
            c("colaborador_id", "id", desc="Seudónimo", ejemplo="COL-0142"),
            c("tipo_movimiento", "lista", desc="INGRESO o SALIDA (traslados: RF-24, futuro)", ejemplo="SALIDA", lista="tipo_movimiento"),
            c("fecha", "fecha", desc="Fecha del movimiento", ejemplo="2027-01-30"),
            c("unidad_id", "id", desc="Unidad", ejemplo="DEP-CCT"),
            c("cargo_id", "id", desc="Cargo", ejemplo="CAR-ACC"),
            c("motivo", "texto", desc="Motivo (sin datos sensibles)", ejemplo="Renuncia voluntaria"),
        ]},
    "13_vacantes.csv": {
        "id": "FTE-SRC-13", "titulo": "Vacantes", "dueno": "Talento Humano (selección)", "llave": ["vacante_id"],
        "columnas": [
            c("vacante_id", "id", desc="Identificador", ejemplo="VAC-001"),
            c("unidad_id", "id", desc="Unidad", ejemplo="DEP-OCR"),
            c("cargo_id", "id", desc="Cargo", ejemplo="CAR-ANO"),
            c("motivo", "lista", desc="Reemplazo o Nueva posición", ejemplo="Reemplazo", lista="motivo_vacante"),
            c("fecha_apertura", "fecha", desc="Fecha de apertura", ejemplo="2027-02-15"),
            c("fecha_cierre", "fecha", req=False, desc="Fecha de cobertura (vacío si sigue abierta)", ejemplo=""),
            c("estado", "lista", desc="Estado", ejemplo="Abierta", lista="estado_vacante"),
        ]},
    "14_escenarios_2027.csv": {
        "id": "FTE-SRC-14", "titulo": "Escenarios", "dueno": "Planificación / Capacity", "llave": ["escenario_id", "ambito_tipo", "ambito_id", "variable"],
        "columnas": [
            c("escenario_id", "id", desc="Escenario", ejemplo="ESC-BASE"),
            c("nombre_escenario", "texto", desc="Nombre", ejemplo="Base"),
            c("descripcion_ajuste", "texto", desc="Qué representa el ajuste", ejemplo="Crecimiento orgánico"),
            c("ambito_tipo", "lista", desc="GLOBAL, PROCESO o ACTIVIDAD", ejemplo="GLOBAL", lista="ambito_tipo"),
            c("ambito_id", "id", req=False, desc="proceso_id o actividad_id (vacío si GLOBAL)", ejemplo=""),
            c("variable", "lista", desc="volumen_pct o tiempo_pct", ejemplo="volumen_pct", lista="variable_escenario"),
            c("valor", "decimal", desc="Proporción: 0.04 = +4 %; -0.18 = -18 %", ejemplo="0.04", minimo=-1, maximo=2),
            c("estado", "lista", desc="Estado", ejemplo="Supuesto", lista="estado_escenario"),
        ]},
}

# Columnas o patrones que nunca deben aparecer (privacidad, DEC-025/026/030)
COLUMNAS_PROHIBIDAS = ["nombre_colaborador", "nombres", "apellidos", "cedula", "cédula", "identificacion",
                       "salario", "sueldo", "remuneracion", "diagnostico", "diagnóstico", "email", "correo", "telefono"]
