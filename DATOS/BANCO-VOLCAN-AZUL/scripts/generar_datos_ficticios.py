#!/usr/bin/env python3
"""
Generador de datos FICTICIOS de entrada para CAPACITY-ANALIZE.

Banco ficticio: "Banco Volcán Azul S.A." (no corresponde a ninguna entidad real).
Alcance piloto: Vicepresidencia de Operaciones y Canales
  - Gerencia de Operaciones Centralizadas (Quito)
  - Gerencia de Red de Agencias Sierra Norte/Centro (10 agencias)
  - Gerencia de Banca Telefónica y Digital (Centro de Contacto)

Período base: 2025-11 a 2026-10 (12 meses). Proyección: 2027.

Todos los datos se generan con semilla fija, por lo que el resultado es reproducible.
Se siembran a propósito algunas anomalías de calidad de datos (ver docs/anomalias_sembradas.md)
para probar las reglas de validación.

Uso:
    python scripts/generar_datos_ficticios.py
"""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20261120
rng = random.Random(SEED)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "input"

INICIO = date(2025, 11, 1)
FIN = date(2026, 10, 31)
HORAS_DIA = 8
FACTOR_NP = 0.10  # factor no productivo propuesto (PAR-002)


# --------------------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------------------
def periodos() -> list[str]:
    out, y, m = [], INICIO.year, INICIO.month
    while (y, m) <= (FIN.year, FIN.month):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


PERIODOS = periodos()


def escribir(nombre: str, filas: list[dict], campos: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / nombre, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in campos})
    print(f"  {nombre:<36} {len(filas):>6} filas")


def rand_fecha(a: date, b: date) -> date:
    return a + timedelta(days=rng.randint(0, (b - a).days))


# --------------------------------------------------------------------------------------
# 1. Calendario laboral (feriados nacionales referenciales)
# --------------------------------------------------------------------------------------
FERIADOS = {
    date(2025, 11, 3): "Independencia de Cuenca",
    date(2025, 12, 25): "Navidad",
    date(2026, 1, 1): "Año Nuevo",
    date(2026, 2, 16): "Carnaval",
    date(2026, 2, 17): "Carnaval",
    date(2026, 4, 3): "Viernes Santo",
    date(2026, 5, 1): "Día del Trabajo",
    date(2026, 5, 25): "Batalla de Pichincha (traslado referencial)",
    date(2026, 8, 10): "Primer Grito de Independencia",
    date(2026, 10, 9): "Independencia de Guayaquil",
}
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

calendario = []
d = INICIO
while d <= FIN:
    fer = FERIADOS.get(d, "")
    lab = d.weekday() < 5 and not fer
    calendario.append({
        "fecha": d.isoformat(), "periodo": f"{d.year}-{d.month:02d}",
        "dia_semana": DIAS[d.weekday()], "es_laborable": "S" if lab else "N", "feriado": fer,
    })
    d += timedelta(days=1)
LAB = {p: sum(1 for c in calendario if c["periodo"] == p and c["es_laborable"] == "S") for p in PERIODOS}
LAB_PROM = sum(LAB.values()) / len(LAB)

# --------------------------------------------------------------------------------------
# 2. Estructura organizacional
# --------------------------------------------------------------------------------------
AGENCIAS = [
    # id, nombre, ciudad, provincia, dotación
    ("AG-QMA", "Agencia Matriz Quito (Av. Amazonas)", "Quito", "Pichincha", 26),
    ("AG-QNO", "Agencia Quito Norte (El Condado)", "Quito", "Pichincha", 19),
    ("AG-QSU", "Agencia Quito Sur (Quitumbe)", "Quito", "Pichincha", 18),
    ("AG-VCH", "Agencia Valle de los Chillos", "Sangolquí", "Pichincha", 15),
    ("AG-CUM", "Agencia Cumbayá", "Quito", "Pichincha", 13),
    ("AG-IBA", "Agencia Ibarra", "Ibarra", "Imbabura", 15),
    ("AG-OTA", "Agencia Otavalo", "Otavalo", "Imbabura", 10),
    ("AG-LAT", "Agencia Latacunga", "Latacunga", "Cotopaxi", 12),
    ("AG-AMB", "Agencia Ambato", "Ambato", "Tungurahua", 17),
    ("AG-RIO", "Agencia Riobamba", "Riobamba", "Chimborazo", 14),
]
DEPTOS_BO = ["DEP-PAG", "DEP-CTA", "DEP-OCR", "DEP-TAR", "DEP-CAM"]
GERENCIAS = ["GER-OPC", "GER-RAS", "GER-CCC"]

estructura = [
    {"unidad_id": "BVA", "nombre": "Banco Volcán Azul S.A. (ficticio)", "nivel": "Banco", "unidad_padre_id": "", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Corporativo"},
    {"unidad_id": "VP-OPC", "nombre": "Vicepresidencia de Operaciones y Canales", "nivel": "Dirección", "unidad_padre_id": "BVA", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Dirección"},
    {"unidad_id": "GER-OPC", "nombre": "Gerencia de Operaciones Centralizadas", "nivel": "Gerencia", "unidad_padre_id": "VP-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "GER-RAS", "nombre": "Gerencia de Red de Agencias Sierra", "nivel": "Gerencia", "unidad_padre_id": "VP-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Red de agencias"},
    {"unidad_id": "GER-CCC", "nombre": "Gerencia de Banca Telefónica y Digital", "nivel": "Gerencia", "unidad_padre_id": "VP-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Centro de contacto"},
    {"unidad_id": "DEP-PAG", "nombre": "Departamento de Pagos y Transferencias", "nivel": "Departamento", "unidad_padre_id": "GER-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "DEP-CTA", "nombre": "Departamento de Cuentas y Servicios", "nivel": "Departamento", "unidad_padre_id": "GER-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "DEP-OCR", "nombre": "Departamento de Operaciones de Crédito", "nivel": "Departamento", "unidad_padre_id": "GER-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "DEP-TAR", "nombre": "Departamento de Tarjetas y Reclamos", "nivel": "Departamento", "unidad_padre_id": "GER-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "DEP-CAM", "nombre": "Departamento de Cámara de Compensación y Valores", "nivel": "Departamento", "unidad_padre_id": "GER-OPC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Back office"},
    {"unidad_id": "DEP-CCT", "nombre": "Centro de Contacto", "nivel": "Departamento", "unidad_padre_id": "GER-CCC", "ciudad": "Quito", "provincia": "Pichincha", "tipo_unidad": "Centro de contacto"},
]
for aid, nom, ciu, prov, _ in AGENCIAS:
    estructura.append({"unidad_id": aid, "nombre": nom, "nivel": "Agencia", "unidad_padre_id": "GER-RAS",
                       "ciudad": ciu, "provincia": prov, "tipo_unidad": "Agencia"})

# --------------------------------------------------------------------------------------
# 3. Cargos
# --------------------------------------------------------------------------------------
cargos = [
    ("CAR-GER", "Gerente de Área", "Gestión", "Gerencial", "Gestión"),
    ("CAR-AGE", "Asistente de Gerencia", "Soporte administrativo", "Operativo", "Soporte"),
    ("CAR-JDP", "Jefe de Departamento", "Gestión", "Jefatura", "Gestión"),
    ("CAR-ASR", "Analista Senior de Operaciones", "Operaciones", "Profesional", "Operativo"),
    ("CAR-ANO", "Analista Operativo", "Operaciones", "Profesional", "Operativo"),
    ("CAR-AST", "Asistente Operativo", "Operaciones", "Operativo", "Operativo"),
    ("CAR-JAG", "Jefe de Agencia", "Red de agencias", "Jefatura", "Gestión"),
    ("CAR-SOP", "Supervisor Operativo de Agencia", "Red de agencias", "Supervisión", "Supervisión"),
    ("CAR-CAJ", "Cajero", "Red de agencias", "Operativo", "Operativo"),
    ("CAR-ASV", "Asesor de Servicios", "Red de agencias", "Operativo", "Operativo"),
    ("CAR-ANG", "Asesor de Negocios", "Red de agencias", "Profesional", "Comercial"),
    ("CAR-SCC", "Supervisor de Centro de Contacto", "Centro de contacto", "Supervisión", "Supervisión"),
    ("CAR-ACC", "Agente de Centro de Contacto", "Centro de contacto", "Operativo", "Operativo"),
    ("CAR-ACA", "Analista de Calidad de Servicio", "Centro de contacto", "Profesional", "Operativo"),
]
cargos_rows = [{"cargo_id": c[0], "nombre_cargo": c[1], "familia": c[2], "nivel_jerarquico": c[3], "tipo_rol": c[4]} for c in cargos]

# --------------------------------------------------------------------------------------
# 4. Plan de dotación (posiciones)
# --------------------------------------------------------------------------------------
plan: dict[str, list[tuple[str, int]]] = {
    "GER-OPC": [("CAR-GER", 1), ("CAR-AGE", 1)],
    "GER-RAS": [("CAR-GER", 1), ("CAR-AGE", 1)],
    "GER-CCC": [("CAR-GER", 1)],
    "DEP-PAG": [("CAR-JDP", 1), ("CAR-ASR", 3), ("CAR-ANO", 14), ("CAR-AST", 4)],
    "DEP-CTA": [("CAR-JDP", 1), ("CAR-ASR", 2), ("CAR-ANO", 16), ("CAR-AST", 5)],
    "DEP-OCR": [("CAR-JDP", 1), ("CAR-ASR", 3), ("CAR-ANO", 14), ("CAR-AST", 3)],
    "DEP-TAR": [("CAR-JDP", 1), ("CAR-ASR", 2), ("CAR-ANO", 12), ("CAR-AST", 3)],
    "DEP-CAM": [("CAR-JDP", 1), ("CAR-ASR", 1), ("CAR-ANO", 8), ("CAR-AST", 4)],
    "DEP-CCT": [("CAR-SCC", 3), ("CAR-ACC", 32), ("CAR-ACA", 2)],
}
for aid, _, _, _, n in AGENCIAS:
    resto = n - 1
    comp = [("CAR-JAG", 1)]
    if n >= 13:
        comp.append(("CAR-SOP", 1))
        resto -= 1
    caj = round(resto * 0.40)
    neg = round((resto - caj) * 0.50)
    srv = resto - caj - neg
    comp += [("CAR-CAJ", caj), ("CAR-ANG", neg), ("CAR-ASV", srv)]
    plan[aid] = comp

posiciones = []  # (unidad, cargo, jornada_semanal)
for u, comp in plan.items():
    for cargo, n in comp:
        for i in range(n):
            jornada = 20 if (cargo == "CAR-ACC" and i >= 26) else 40  # 6 agentes a medio tiempo
            posiciones.append({"unidad_id": u, "cargo_id": cargo, "jornada": jornada})

# --------------------------------------------------------------------------------------
# 5. Colaboradores, movimientos y vacantes
# --------------------------------------------------------------------------------------
colaboradores, movimientos, vacantes = [], [], []
seq = [0]
vac_seq = [0]


def nuevo_id() -> str:
    seq[0] += 1
    return f"COL-{seq[0]:04d}"


def antiguedad_fecha(cargo: str) -> date:
    if cargo in ("CAR-GER", "CAR-JDP", "CAR-JAG"):
        return rand_fecha(date(2006, 1, 1), date(2019, 12, 31))
    if cargo in ("CAR-ACC", "CAR-CAJ"):
        return rand_fecha(date(2017, 1, 1), date(2025, 9, 30))
    return rand_fecha(date(2010, 1, 1), date(2025, 6, 30))


def alta(pos: dict, ingreso: date, salida: date | None = None) -> str:
    cid = nuevo_id()
    colaboradores.append({
        "colaborador_id": cid, "unidad_id": pos["unidad_id"], "cargo_id": pos["cargo_id"],
        "fecha_ingreso": ingreso.isoformat(), "fecha_salida": salida.isoformat() if salida else "",
        "tipo_contrato": "Eventual" if (pos["cargo_id"] == "CAR-ACC" and rng.random() < 0.15) else "Indefinido",
        "jornada_horas_semana": pos["jornada"], "modalidad": "Presencial" if pos["unidad_id"].startswith("AG-") else rng.choice(["Presencial", "Presencial", "Híbrida"]),
    })
    if ingreso >= INICIO:
        movimientos.append({"movimiento_id": "", "colaborador_id": cid, "tipo_movimiento": "INGRESO", "fecha": ingreso.isoformat(),
                            "unidad_id": pos["unidad_id"], "cargo_id": pos["cargo_id"], "motivo": pos.get("motivo_ingreso", "Reemplazo")})
    if salida:
        movimientos.append({"movimiento_id": "", "colaborador_id": cid, "tipo_movimiento": "SALIDA", "fecha": salida.isoformat(),
                            "unidad_id": pos["unidad_id"], "cargo_id": pos["cargo_id"], "motivo": rng.choice(["Renuncia voluntaria", "Renuncia voluntaria", "Renuncia voluntaria", "Terminación de relación laboral", "Jubilación"])})
    return cid


rotables = [i for i, p in enumerate(posiciones) if p["cargo_id"] in ("CAR-CAJ", "CAR-ACC", "CAR-ASV", "CAR-ANO", "CAR-ANG", "CAR-AST")]
pesos = [3 if posiciones[i]["cargo_id"] in ("CAR-CAJ", "CAR-ACC") else 1 for i in rotables]
rotan: set[int] = set()
while len(rotan) < 24:
    rotan.add(rng.choices(rotables, weights=pesos)[0])

for i, pos in enumerate(posiciones):
    ingreso = antiguedad_fecha(pos["cargo_id"])
    if i not in rotan:
        alta(pos, ingreso)
        continue
    salida = rand_fecha(date(2025, 11, 20), date(2026, 9, 30))
    alta(pos, ingreso, salida)
    vac_seq[0] += 1
    vid = f"VAC-{vac_seq[0]:03d}"
    reemplazo = salida + timedelta(days=rng.randint(20, 85))
    cubierta = reemplazo <= FIN
    if cubierta:
        alta(pos, reemplazo)
    vacantes.append({"vacante_id": vid, "unidad_id": pos["unidad_id"], "cargo_id": pos["cargo_id"], "motivo": "Reemplazo",
                     "fecha_apertura": (salida + timedelta(days=1)).isoformat(),
                     "fecha_cierre": reemplazo.isoformat() if cubierta else "", "estado": "Cubierta" if cubierta else "Abierta"})

# Dos posiciones nuevas aprobadas en DEP-CTA por acumulación de trabajo (KYC)
for k in range(2):
    pos = {"unidad_id": "DEP-CTA", "cargo_id": "CAR-ANO", "jornada": 40, "motivo_ingreso": "Nueva posición"}
    ingreso = date(2026, 3, 2) if k == 0 else date(2026, 4, 6)
    vac_seq[0] += 1
    vacantes.append({"vacante_id": f"VAC-{vac_seq[0]:03d}", "unidad_id": "DEP-CTA", "cargo_id": "CAR-ANO", "motivo": "Nueva posición",
                     "fecha_apertura": "2026-01-12", "fecha_cierre": ingreso.isoformat(), "estado": "Cubierta"})
    alta(pos, ingreso)

movimientos.sort(key=lambda r: r["fecha"])
for n, m in enumerate(movimientos, 1):
    m["movimiento_id"] = f"MOV-{n:03d}"

# Licencias de maternidad y paternidad (asignadas a colaboradores vigentes todo el período)
vigentes = [c for c in colaboradores if not c["fecha_salida"] and c["fecha_ingreso"] < "2025-06-01"]
maternidad = rng.sample(vigentes, 3)
paternidad = rng.sample([c for c in vigentes if c not in maternidad], 3)

# Anomalías sembradas en colaboradores (registros extra, no forman parte de la dotación real)
colaboradores.append({"colaborador_id": "COL-9001", "unidad_id": "AG-QCE", "cargo_id": "CAR-CAJ", "fecha_ingreso": "2024-02-01",
                      "fecha_salida": "", "tipo_contrato": "Indefinido", "jornada_horas_semana": 40, "modalidad": "Presencial"})
colaboradores.append({"colaborador_id": "COL-9002", "unidad_id": "DEP-OCR", "cargo_id": "CAR-ANO", "fecha_ingreso": "2026-05-04",
                      "fecha_salida": "2026-03-31", "tipo_contrato": "Indefinido", "jornada_horas_semana": 40, "modalidad": "Híbrida"})

# --------------------------------------------------------------------------------------
# 6. Procesos y actividades
# --------------------------------------------------------------------------------------
procesos = [
    ("P-CAJ", "Atención en caja", "Canales presenciales", "CAR-JAG", "caja"),
    ("P-SER", "Servicios al cliente en agencia", "Canales presenciales", "CAR-JAG", "servicios"),
    ("P-NEG", "Negocios y colocación en agencia", "Canales presenciales", "CAR-JAG", "negocios"),
    ("P-GAG", "Gestión y control de agencia", "Canales presenciales", "CAR-GER", "gestion"),
    ("P-GER", "Dirección y gestión de gerencia", "Gestión", "CAR-GER", "gestion"),
    ("P-PAG", "Pagos y transferencias", "Operaciones centralizadas", "CAR-JDP", "pagos"),
    ("P-CTA", "Gestión de cuentas y cumplimiento", "Operaciones centralizadas", "CAR-JDP", "cuentas"),
    ("P-OCR", "Operaciones de crédito", "Operaciones centralizadas", "CAR-JDP", "credito"),
    ("P-TAR", "Tarjetas y reclamos", "Operaciones centralizadas", "CAR-JDP", "tarjetas"),
    ("P-CAM", "Cámara de compensación y valores", "Operaciones centralizadas", "CAR-JDP", "camara"),
    ("P-JDP", "Jefatura de departamento", "Gestión", "CAR-GER", "gestion"),
    ("P-CCT", "Atención telefónica y digital", "Canales remotos", "CAR-GER", "contact"),
]
procesos_rows = [{"proceso_id": p[0], "nombre_proceso": p[1], "macroproceso": p[2], "cargo_dueno_proceso": p[3], "grupo_estacional": p[4]} for p in procesos]
GRUPO = {p[0]: p[4] for p in procesos}

# id, proceso, nombre, cargo, unidad_trabajo, t_std(min), t_rep(min), método, ámbito, tipo, peso, tasa_reproceso
A = [
    ("ACT-001", "P-CAJ", "Depósito en efectivo o cheque", "CAR-CAJ", "transacción", 2.1, 1.5, "Estudio de tiempos", "AGENCIA", "Core", 30, 0.010),
    ("ACT-002", "P-CAJ", "Retiro en ventanilla", "CAR-CAJ", "transacción", 2.3, 1.5, "Estudio de tiempos", "AGENCIA", "Core", 22, 0.008),
    ("ACT-003", "P-CAJ", "Pago de servicios básicos y recaudaciones", "CAR-CAJ", "transacción", 1.8, 1.2, "Estudio de tiempos", "AGENCIA", "Core", 18, 0.006),
    ("ACT-004", "P-CAJ", "Pago de impuestos SRI y matriculación vehicular", "CAR-CAJ", "transacción", 2.8, 2.0, "Estudio de tiempos", "AGENCIA", "Core", 7, 0.020),
    ("ACT-005", "P-CAJ", "Cobro de cheques", "CAR-CAJ", "transacción", 3.2, 2.0, "Estudio de tiempos", "AGENCIA", "Core", 8, 0.012),
    ("ACT-006", "P-CAJ", "Pago del Bono de Desarrollo Humano", "CAR-CAJ", "transacción", 2.5, 1.5, "Estimación experta", "AGENCIA", "Core", 6, 0.005),
    ("ACT-007", "P-CAJ", "Cuadre y cierre de caja diario", "CAR-CAJ", "cierre", 25.0, 15.0, "Estimación experta", "AGENCIA", "Soporte", 9, 0.030),
    ("ACT-010", "P-SER", "Apertura de cuenta de ahorros", "CAR-ASV", "cuenta", 32.0, 20.0, "Estudio de tiempos", "AGENCIA", "Core", 20, 0.080),
    ("ACT-011", "P-SER", "Apertura de cuenta corriente", "CAR-ASV", "cuenta", 48.0, 25.0, "Estudio de tiempos", "AGENCIA", "Core", 6, 0.100),
    ("ACT-012", "P-SER", "Entrega y activación de tarjeta de débito", "CAR-ASV", "tarjeta", 12.0, 8.0, "Estudio de tiempos", "AGENCIA", "Core", 12, 0.020),
    ("ACT-013", "P-SER", "Actualización de datos del cliente (KYC)", "CAR-ASV", "actualización", 15.0, 10.0, "Estudio de tiempos", "AGENCIA", "Core", 18, 0.050),
    ("ACT-014", "P-SER", "Emisión de certificados y estados de cuenta", "CAR-ASV", "certificado", 6.0, 4.0, "Registro de sistema", "AGENCIA", "Core", 8, 0.010),
    ("ACT-015", "P-SER", "Registro de reclamos en agencia", "CAR-ASV", "reclamo", 18.0, 10.0, "Estimación experta", "AGENCIA", "Core", 14, 0.040),
    ("ACT-016", "P-SER", "Bloqueo, desbloqueo y reseteo de claves de banca digital", "CAR-ASV", "solicitud", 9.0, 5.0, "Registro de sistema", "AGENCIA", "Core", 14, 0.020),
    ("ACT-017", "P-SER", "Atención de quejas recibidas por redes sociales", "CAR-ASV", "caso", 0.0, 0.0, "Pendiente de medición", "AGENCIA", "Core", 0, 0.0),
    ("ACT-020", "P-NEG", "Asesoría y solicitud de crédito de consumo", "CAR-ANG", "solicitud", 55.0, 25.0, "Estudio de tiempos", "AGENCIA", "Core", 25, 0.120),
    ("ACT-021", "P-NEG", "Solicitud de microcrédito con evaluación en campo", "CAR-ANG", "solicitud", 95.0, 30.0, "Estimación experta", "AGENCIA", "Core", 18, 0.100),
    ("ACT-022", "P-NEG", "Apertura de depósito a plazo fijo", "CAR-ANG", "póliza", 35.0, 15.0, "Estudio de tiempos", "AGENCIA", "Core", 12, 0.030),
    ("ACT-023", "P-NEG", "Venta de tarjeta de crédito", "CAR-ANG", "solicitud", 28.0, 15.0, "Estudio de tiempos", "AGENCIA", "Core", 12, 0.090),
    ("ACT-024", "P-NEG", "Visita comercial a cliente", "CAR-ANG", "visita", 80.0, 0.0, "Estimación experta", "AGENCIA", "Core", 15, 0.0),
    ("ACT-025", "P-NEG", "Seguimiento de cartera y cobranza temprana", "CAR-ANG", "gestión", 12.0, 0.0, "Registro de sistema", "AGENCIA", "Core", 18, 0.0),
    ("ACT-030", "P-GAG", "Supervisión, coaching y control del equipo", "CAR-JAG", "hora", 60.0, 0.0, "Bitácora de gestión", "AGENCIA", "Gestión", 35, 0.0),
    ("ACT-031", "P-GAG", "Comités, reportes y gestión comercial de agencia", "CAR-JAG", "hora", 60.0, 0.0, "Bitácora de gestión", "AGENCIA", "Gestión", 40, 0.0),
    ("ACT-032", "P-GAG", "Atención de casos escalados de clientes", "CAR-JAG", "caso", 20.0, 0.0, "Estimación experta", "AGENCIA", "Gestión", 25, 0.0),
    ("ACT-033", "P-GAG", "Aprobaciones y autorizaciones operativas", "CAR-SOP", "autorización", 4.0, 0.0, "Registro de sistema", "AGENCIA", "Soporte", 30, 0.0),
    ("ACT-034", "P-GAG", "Arqueo, control de bóveda y abastecimiento de efectivo", "CAR-SOP", "arqueo", 45.0, 20.0, "Estudio de tiempos", "AGENCIA", "Soporte", 25, 0.020),
    ("ACT-035", "P-GAG", "Apoyo en caja en horas pico", "CAR-SOP", "transacción", 2.3, 1.5, "Estudio de tiempos", "AGENCIA", "Core", 25, 0.008),
    ("ACT-036", "P-GAG", "Control operativo y cuadre de agencia", "CAR-SOP", "hora", 60.0, 0.0, "Bitácora de gestión", "AGENCIA", "Soporte", 20, 0.0),
    ("ACT-040", "P-GER", "Dirección, planificación y seguimiento de indicadores", "CAR-GER", "hora", 60.0, 0.0, "Bitácora de gestión", "GERENCIA", "Gestión", 55, 0.0),
    ("ACT-041", "P-GER", "Comités institucionales y reportes a Vicepresidencia", "CAR-GER", "hora", 60.0, 0.0, "Bitácora de gestión", "GERENCIA", "Gestión", 45, 0.0),
    ("ACT-042", "P-GER", "Gestión administrativa y agenda de gerencia", "CAR-AGE", "hora", 60.0, 0.0, "Bitácora de gestión", "GERENCIA", "Soporte", 55, 0.0),
    ("ACT-043", "P-GER", "Consolidación de reportes de gestión", "CAR-AGE", "reporte", 45.0, 20.0, "Estimación experta", "GERENCIA", "Soporte", 45, 0.050),
    ("ACT-050", "P-PAG", "Revisión manual de transferencias interbancarias SPI observadas", "CAR-ANO", "transferencia", 3.5, 3.0, "Registro de sistema", "DEP-PAG", "Core", 30, 0.030),
    ("ACT-051", "P-PAG", "Gestión de transferencias rechazadas y devoluciones", "CAR-ANO", "caso", 14.0, 8.0, "Estudio de tiempos", "DEP-PAG", "Core", 18, 0.060),
    ("ACT-052", "P-PAG", "Procesamiento de pagos masivos a proveedores (cash management)", "CAR-ANO", "lote", 28.0, 15.0, "Estudio de tiempos", "DEP-PAG", "Core", 15, 0.070),
    ("ACT-053", "P-PAG", "Procesamiento de pagos de nómina de empresas", "CAR-ANO", "lote", 32.0, 15.0, "Estudio de tiempos", "DEP-PAG", "Core", 12, 0.050),
    ("ACT-054", "P-PAG", "Conciliación diaria SPI y cuentas puente", "CAR-ASR", "conciliación", 95.0, 40.0, "Estimación experta", "DEP-PAG", "Core", 40, 0.020),
    ("ACT-055", "P-PAG", "Atención de requerimientos de agencias y clientes corporativos", "CAR-AST", "requerimiento", 10.0, 0.0, "Registro de sistema", "DEP-PAG", "Soporte", 50, 0.0),
    ("ACT-056", "P-PAG", "Archivo y digitalización de soportes", "CAR-AST", "soporte", 3.0, 0.0, "Estudio de tiempos", "DEP-PAG", "Soporte", 50, 0.0),
    ("ACT-057", "P-PAG", "Control de calidad y cuadre de transferencias", "CAR-ASR", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-PAG", "Soporte", 60, 0.0),
    ("ACT-060", "P-CTA", "Verificación documental de aperturas de cuenta", "CAR-ANO", "expediente", 14.0, 10.0, "Estudio de tiempos", "DEP-CTA", "Core", 32, 0.110),
    ("ACT-061", "P-CTA", "Validación en listas restrictivas y debida diligencia", "CAR-ANO", "consulta", 7.0, 4.0, "Registro de sistema", "DEP-CTA", "Core", 20, 0.020),
    ("ACT-062", "P-CTA", "Procesamiento de embargos y retenciones judiciales", "CAR-ANO", "oficio", 24.0, 15.0, "Estudio de tiempos", "DEP-CTA", "Core", 18, 0.040),
    ("ACT-063", "P-CTA", "Respuesta a requerimientos de organismos de control y autoridades", "CAR-ASR", "requerimiento", 50.0, 25.0, "Estimación experta", "DEP-CTA", "Core", 45, 0.050),
    ("ACT-064", "P-CTA", "Cierre y cancelación de cuentas", "CAR-ANO", "cuenta", 18.0, 10.0, "Estudio de tiempos", "DEP-CTA", "Core", 14, 0.030),
    ("ACT-065", "P-CTA", "Gestión de cuentas inactivas", "CAR-ANO", "cuenta", 6.0, 0.0, "Registro de sistema", "DEP-CTA", "Core", 8, 0.0),
    ("ACT-066", "P-CTA", "Archivo y custodia de expedientes", "CAR-AST", "expediente", 4.0, 0.0, "Estudio de tiempos", "DEP-CTA", "Soporte", 60, 0.0),
    ("ACT-067", "P-CTA", "Ingreso de actualizaciones masivas", "CAR-AST", "registro", 2.0, 1.5, "Registro de sistema", "DEP-CTA", "Soporte", 40, 0.040),
    ("ACT-068", "P-CTA", "Revisión de calidad de expedientes (muestreo)", "CAR-ASR", "expediente", 10.0, 0.0, "Estimación experta", "DEP-CTA", "Soporte", 55, 0.0),
    ("ACT-070", "P-OCR", "Revisión y validación de expedientes de crédito", "CAR-ANO", "expediente", 38.0, 20.0, "Estudio de tiempos", "DEP-OCR", "Core", 30, 0.120),
    ("ACT-071", "P-OCR", "Desembolso de operaciones de crédito", "CAR-ANO", "operación", 18.0, 10.0, "Estudio de tiempos", "DEP-OCR", "Core", 25, 0.040),
    ("ACT-072", "P-OCR", "Constitución y registro de garantías (hipotecas y prendas)", "CAR-ANO", "garantía", 65.0, 30.0, "Estimación experta", "DEP-OCR", "Core", 15, 0.080),
    ("ACT-073", "P-OCR", "Cancelación de créditos y levantamiento de garantías", "CAR-ANO", "operación", 35.0, 15.0, "Estudio de tiempos", "DEP-OCR", "Core", 12, 0.050),
    ("ACT-074", "P-OCR", "Registro de novedades y reestructuraciones", "CAR-ANO", "novedad", 22.0, 12.0, "Estudio de tiempos", "DEP-OCR", "Core", 18, 0.060),
    ("ACT-075", "P-OCR", "Control de calidad y conciliación de cartera", "CAR-ASR", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-OCR", "Soporte", 60, 0.0),
    ("ACT-076", "P-OCR", "Seguimiento de documentación pendiente con agencias", "CAR-ASR", "caso", 15.0, 0.0, "Estimación experta", "DEP-OCR", "Soporte", 40, 0.0),
    ("ACT-077", "P-OCR", "Archivo de pagarés y expedientes", "CAR-AST", "expediente", 5.0, 0.0, "Estudio de tiempos", "DEP-OCR", "Soporte", 100, 0.0),
    ("ACT-080", "P-TAR", "Gestión de contracargos con marcas", "CAR-ANO", "caso", 32.0, 20.0, "Estudio de tiempos", "DEP-TAR", "Core", 25, 0.080),
    ("ACT-081", "P-TAR", "Resolución de reclamos de tarjetas", "CAR-ANO", "reclamo", 26.0, 15.0, "Estudio de tiempos", "DEP-TAR", "Core", 35, 0.070),
    ("ACT-082", "P-TAR", "Emisión y reposición de tarjetas", "CAR-AST", "tarjeta", 6.0, 4.0, "Registro de sistema", "DEP-TAR", "Core", 50, 0.030),
    ("ACT-083", "P-TAR", "Conciliación con procesador y marcas", "CAR-ASR", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-TAR", "Soporte", 50, 0.0),
    ("ACT-084", "P-TAR", "Análisis de alertas de posible fraude", "CAR-ANO", "alerta", 9.0, 0.0, "Registro de sistema", "DEP-TAR", "Core", 25, 0.0),
    ("ACT-085", "P-TAR", "Distribución de tarjetas a agencias", "CAR-AST", "envío", 15.0, 0.0, "Estimación experta", "DEP-TAR", "Soporte", 50, 0.0),
    ("ACT-086", "P-TAR", "Respuesta a reclamos en segunda instancia (organismo de control)", "CAR-ASR", "caso", 70.0, 30.0, "Estimación experta", "DEP-TAR", "Core", 50, 0.060),
    ("ACT-090", "P-CAM", "Procesamiento de cheques en cámara de compensación", "CAR-ANO", "cheque", 1.4, 1.0, "Registro de sistema", "DEP-CAM", "Core", 45, 0.010),
    ("ACT-091", "P-CAM", "Gestión de cheques devueltos y protestos", "CAR-ANO", "cheque", 11.0, 6.0, "Estudio de tiempos", "DEP-CAM", "Core", 25, 0.030),
    ("ACT-092", "P-CAM", "Custodia y control de valores y garantías físicas", "CAR-ANO", "movimiento", 14.0, 0.0, "Estimación experta", "DEP-CAM", "Core", 30, 0.0),
    ("ACT-093", "P-CAM", "Clasificación y envío de valijas", "CAR-AST", "valija", 18.0, 0.0, "Estudio de tiempos", "DEP-CAM", "Soporte", 60, 0.0),
    ("ACT-094", "P-CAM", "Digitalización de cheques", "CAR-AST", "cheque", 0.8, 0.5, "Registro de sistema", "DEP-CAM", "Soporte", 40, 0.020),
    ("ACT-095", "P-CAM", "Cuadre de cámara y reportes", "CAR-ASR", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-CAM", "Soporte", 100, 0.0),
    ("ACT-098", "P-JDP", "Supervisión y planificación del departamento", "CAR-JDP", "hora", 60.0, 0.0, "Bitácora de gestión", "DEPTO", "Gestión", 55, 0.0),
    ("ACT-099", "P-JDP", "Atención de escalamientos y aprobaciones", "CAR-JDP", "caso", 25.0, 0.0, "Estimación experta", "DEPTO", "Gestión", 45, 0.0),
    ("ACT-100", "P-CCT", "Atención de llamadas de consulta", "CAR-ACC", "llamada", 4.2, 0.0, "Registro de sistema", "DEP-CCT", "Core", 45, 0.0),
    ("ACT-101", "P-CCT", "Atención de reclamos telefónicos", "CAR-ACC", "llamada", 8.5, 6.0, "Registro de sistema", "DEP-CCT", "Core", 18, 0.060),
    ("ACT-102", "P-CCT", "Bloqueo de tarjetas y reportes de fraude", "CAR-ACC", "llamada", 5.0, 0.0, "Registro de sistema", "DEP-CCT", "Core", 10, 0.0),
    ("ACT-103", "P-CCT", "Atención por chat y WhatsApp", "CAR-ACC", "conversación", 6.5, 4.0, "Registro de sistema", "DEP-CCT", "Core", 17, 0.030),
    ("ACT-104", "P-CCT", "Llamadas salientes de cobranza preventiva", "CAR-ACC", "llamada", 5.5, 0.0, "Registro de sistema", "DEP-CCT", "Core", 10, 0.0),
    ("ACT-105", "P-CCT", "Monitoreo y calibración de calidad de llamadas", "CAR-ACA", "evaluación", 16.0, 0.0, "Estudio de tiempos", "DEP-CCT", "Soporte", 70, 0.0),
    ("ACT-106", "P-CCT", "Reportería de calidad de servicio", "CAR-ACA", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-CCT", "Soporte", 30, 0.0),
    ("ACT-107", "P-CCT", "Supervisión de piso y gestión de turnos", "CAR-SCC", "hora", 60.0, 0.0, "Bitácora de gestión", "DEP-CCT", "Gestión", 60, 0.0),
    ("ACT-108", "P-CCT", "Atención de llamadas escaladas", "CAR-SCC", "llamada", 12.0, 6.0, "Registro de sistema", "DEP-CCT", "Core", 40, 0.040),
]
actividades_rows = []
for a in A:
    actividades_rows.append({
        "actividad_id": a[0], "proceso_id": a[1], "nombre_actividad": a[2], "cargo_id": a[3], "unidad_trabajo": a[4],
        "tiempo_estandar_min": a[5], "tiempo_reproceso_min": a[6], "metodo_medicion": a[7],
        "fecha_medicion": "" if a[7] == "Pendiente de medición" else rand_fecha(date(2025, 3, 1), date(2025, 9, 30)).isoformat(),
        "ambito": a[8], "tipo_actividad": a[9],
    })


def unidades_de_ambito(amb: str) -> list[str]:
    if amb == "AGENCIA":
        return [a[0] for a in AGENCIAS]
    if amb == "GERENCIA":
        return GERENCIAS
    if amb == "DEPTO":
        return DEPTOS_BO
    return [amb]


# --------------------------------------------------------------------------------------
# 7. Volúmenes (calibrados contra una utilización objetivo por unidad y cargo)
# --------------------------------------------------------------------------------------
EST = {  # índice estacional por mes calendario
    "caja":      {11: 1.00, 12: 1.22, 1: 0.95, 2: 0.90, 3: 1.00, 4: 1.08, 5: 1.00, 6: 0.97, 7: 0.98, 8: 1.12, 9: 1.06, 10: 1.00},
    "servicios": {11: 1.00, 12: 1.08, 1: 1.05, 2: 0.92, 3: 1.02, 4: 1.05, 5: 1.00, 6: 0.98, 7: 0.96, 8: 1.04, 9: 1.06, 10: 1.00},
    "negocios":  {11: 1.05, 12: 1.10, 1: 0.85, 2: 0.90, 3: 1.02, 4: 1.04, 5: 1.03, 6: 1.00, 7: 0.98, 8: 1.08, 9: 1.05, 10: 1.02},
    "gestion":   {m: 1.0 for m in range(1, 13)},
    "pagos":     {11: 1.02, 12: 1.25, 1: 0.95, 2: 0.92, 3: 1.00, 4: 1.12, 5: 1.00, 6: 0.98, 7: 0.97, 8: 1.15, 9: 1.02, 10: 1.00},
    "cuentas":   {11: 1.00, 12: 0.95, 1: 1.08, 2: 0.95, 3: 1.05, 4: 1.04, 5: 1.02, 6: 1.00, 7: 0.98, 8: 1.02, 9: 1.08, 10: 1.03},
    "credito":   {11: 1.06, 12: 1.12, 1: 0.82, 2: 0.90, 3: 1.00, 4: 1.03, 5: 1.04, 6: 1.02, 7: 1.00, 8: 1.06, 9: 1.04, 10: 1.03},
    "tarjetas":  {11: 1.08, 12: 1.25, 1: 1.12, 2: 0.92, 3: 0.95, 4: 0.98, 5: 1.00, 6: 0.97, 7: 0.98, 8: 1.02, 9: 1.03, 10: 1.00},
    "camara":    {11: 1.06, 12: 1.18, 1: 1.00, 2: 0.96, 3: 0.98, 4: 0.97, 5: 0.95, 6: 0.94, 7: 0.92, 8: 0.95, 9: 0.91, 10: 0.90},
    "contact":   {11: 1.02, 12: 1.20, 1: 1.10, 2: 0.94, 3: 0.98, 4: 1.04, 5: 0.98, 6: 0.96, 7: 0.97, 8: 1.06, 9: 1.02, 10: 1.00},
}
U_OBJ = {
    ("AG-QMA", "CAR-CAJ"): 1.16, ("AG-QMA", "CAR-ASV"): 1.08, ("AG-QNO", "CAR-CAJ"): 1.06,
    ("AG-AMB", "CAR-ANG"): 1.10, ("DEP-CTA", "CAR-ANO"): 1.15, ("DEP-TAR", "CAR-ANO"): 1.09,
    ("DEP-CCT", "CAR-ACC"): 1.03, ("AG-OTA", "CAR-CAJ"): 0.66, ("AG-OTA", "CAR-ASV"): 0.70,
    ("DEP-CAM", "CAR-ANO"): 0.63, ("DEP-CAM", "CAR-AST"): 0.70, ("AG-CUM", "CAR-CAJ"): 0.74,
}
# Horas productivas aproximadas de 1 FTE al mes (solo para calibrar volúmenes)
H_PROD_FTE = LAB_PROM * HORAS_DIA * (1 - FACTOR_NP) * 0.92

fte_base: dict[tuple[str, str], float] = {}
for p in posiciones:
    k = (p["unidad_id"], p["cargo_id"])
    fte_base[k] = fte_base.get(k, 0) + p["jornada"] / 40

FUENTE = {"Registro de sistema": "Core bancario / sistema transaccional", "Estudio de tiempos": "Core bancario / sistema transaccional",
          "Estimación experta": "Registro manual de la unidad", "Bitácora de gestión": "Bitácora de gestión (horas)"}

volumenes, reprocesos = [], []
CAUSAS = {
    "P-CAJ": ["Error de digitación", "Billete falso o en mal estado", "Reverso por cuenta errada"],
    "P-SER": ["Documentación incompleta", "Firma no coincide", "Información inconsistente del cliente"],
    "P-NEG": ["Documentación incompleta", "Información de ingresos no verificable", "Error en la simulación"],
    "P-GAG": ["Diferencia en arqueo", "Error de registro"],
    "P-GER": ["Información de entrada errónea"],
    "P-PAG": ["Datos del beneficiario errados", "Rechazo del sistema SPI", "Archivo de carga con formato inválido"],
    "P-CTA": ["Documentación incompleta desde agencia", "Error en ficha del cliente", "Oficio ilegible o incompleto"],
    "P-OCR": ["Expediente incompleto desde agencia", "Error en datos de la operación", "Garantía sin inscripción"],
    "P-TAR": ["Evidencia insuficiente", "Plazo de marca vencido", "Error en registro del reclamo"],
    "P-CAM": ["Imagen de cheque ilegible", "Error de cuadre"],
    "P-CCT": ["Información incorrecta al cliente", "Caso mal tipificado"],
}

for a in A:
    aid, proc, _, cargo, _, t, trep, metodo, amb, _, peso, tasa = a
    if t <= 0 or peso <= 0:
        continue
    for u in unidades_de_ambito(amb):
        fte = fte_base.get((u, cargo), 0)
        if fte == 0:
            continue
        acts_cargo = [x for x in A if x[3] == cargo and u in unidades_de_ambito(x[8]) and x[5] > 0]
        share = peso / sum(x[10] for x in acts_cargo)
        u_obj = U_OBJ.get((u, cargo), rng.uniform(0.84, 0.98))
        # se fija la utilización objetivo una sola vez por (unidad, cargo)
        U_OBJ[(u, cargo)] = u_obj
        horas_mes = u_obj * fte * H_PROD_FTE * share / (1 + tasa * (trep / t if t else 0))
        vol_base = horas_mes * 60 / t
        for per in PERIODOS:
            mes = int(per[5:])
            f = EST[GRUPO[proc]][mes] * (LAB[per] / LAB_PROM) * rng.gauss(1, 0.04)
            vol = max(0, round(vol_base * f))
            volumenes.append({"periodo": per, "unidad_id": u, "actividad_id": aid, "volumen": vol,
                               "fuente": "Plataforma del centro de contacto" if (u == "DEP-CCT" and metodo != "Bitácora de gestión") else FUENTE[metodo]})
            if tasa > 0 and vol > 0:
                cant = round(vol * tasa * rng.uniform(0.75, 1.25))
                if cant > 0:
                    reprocesos.append({"periodo": per, "unidad_id": u, "actividad_id": aid, "cantidad_reprocesos": cant,
                                       "causa_principal": rng.choice(CAUSAS[proc])})

# Anomalías sembradas en volúmenes
volumenes.append(dict(volumenes[100]))                       # duplicado exacto
volumenes.append({"periodo": "2026-03", "unidad_id": "AG-RIO", "actividad_id": "ACT-002", "volumen": -350,
                  "fuente": "Registro manual de la unidad"})   # volumen negativo (fila adicional)
volumenes.append({"periodo": "2026-06", "unidad_id": "DEP-PAG", "actividad_id": "ACT-999", "volumen": 420,
                  "fuente": "Registro manual de la unidad"})   # actividad inexistente

# --------------------------------------------------------------------------------------
# 8. Ausentismo, capacitación y horas extra por colaborador-mes
# --------------------------------------------------------------------------------------
def dias_activos(c: dict, per: str) -> int:
    ing = date.fromisoformat(c["fecha_ingreso"])
    sal = date.fromisoformat(c["fecha_salida"]) if c["fecha_salida"] else FIN
    return sum(1 for x in calendario if x["periodo"] == per and x["es_laborable"] == "S" and ing <= date.fromisoformat(x["fecha"]) <= sal)


PESO_VAC = {11: 0.5, 12: 1.6, 1: 1.3, 2: 0.6, 3: 0.5, 4: 0.9, 5: 0.5, 6: 0.6, 7: 1.8, 8: 2.0, 9: 0.9, 10: 0.5}
ausentismo, horas_extra = [], []
reales = [c for c in colaboradores if not c["colaborador_id"].startswith("COL-9")]
for c in reales:
    fte = int(c["jornada_horas_semana"]) / 40
    hdia = HORAS_DIA * fte
    activos = {p: dias_activos(c, p) for p in PERIODOS}
    meses_act = [p for p in PERIODOS if activos[p] > 0]
    if not meses_act:
        continue
    # vacaciones: 15 días hábiles por año completo, prorrateado; 1-2 bloques
    dias_vac = round(15 * len(meses_act) / 12)
    vac = {p: 0 for p in PERIODOS}
    if dias_vac >= 3:
        bloques = [dias_vac] if dias_vac < 10 or rng.random() < 0.5 else [dias_vac // 2, dias_vac - dias_vac // 2]
        for b in bloques:
            mes = rng.choices(meses_act, weights=[PESO_VAC[int(p[5:])] for p in meses_act])[0]
            vac[mes] += b
    lic = {p: 0 for p in PERIODOS}
    if c in maternidad:
        ini = rng.randint(1, 8)
        for k, dias in enumerate([12, 21, 21, 6]):  # ≈ 12 semanas
            if ini + k < len(PERIODOS):
                lic[PERIODOS[ini + k]] += dias
    perm_pat = {p: 0 for p in PERIODOS}
    if c in paternidad:
        perm_pat[rng.choice(meses_act)] = 8
    primer_mes = meses_act[0] if date.fromisoformat(c["fecha_ingreso"]) >= INICIO else None
    for p in meses_act:
        disp = activos[p]
        d_vac = min(vac[p], disp)
        d_lic = min(lic[p], disp - d_vac)
        d_enf = 0
        r = rng.random()
        if r < 0.012:
            d_enf = rng.randint(5, 12)
        elif r < 0.14:
            d_enf = rng.randint(1, 3)
        d_enf = min(d_enf, disp - d_vac - d_lic)
        h_perm = perm_pat[p] * hdia + (rng.choice([2, 3, 4, 4, 6, 8]) * fte if rng.random() < 0.16 else 0)
        h_perm = min(h_perm, (disp - d_vac - d_lic - d_enf) * hdia)
        h_cap = 40 * fte if p == primer_mes else rng.choice([0, 2, 2, 4, 4, 6, 8]) * fte
        h_cap = max(0, min(h_cap, (disp - d_vac - d_lic - d_enf) * hdia - h_perm))
        ausentismo.append({
            "colaborador_id": c["colaborador_id"], "periodo": p,
            "horas_vacaciones": round(d_vac * hdia, 1), "horas_enfermedad": round(d_enf * hdia, 1),
            "horas_permisos": round(h_perm, 1), "horas_licencias": round(d_lic * hdia, 1),
            "horas_capacitacion": round(h_cap, 1),
        })
        u_obj = U_OBJ.get((c["unidad_id"], c["cargo_id"]), 0.9)
        mes = int(p[5:])
        pico = mes in (12, 8, 4)
        prob = 0.65 if u_obj > 1.02 else (0.25 if u_obj > 0.95 else 0.06)
        if pico:
            prob = min(0.9, prob + 0.15)
        if c["cargo_id"] in ("CAR-GER", "CAR-JDP", "CAR-JAG"):
            prob = 0  # personal de dirección y confianza: no registra horas extra
        if rng.random() < prob:
            sup = rng.randint(3, 22 if u_obj > 1.02 else 10)
            ext = rng.randint(0, 8) if (pico or u_obj > 1.05) else 0
            horas_extra.append({"colaborador_id": c["colaborador_id"], "periodo": p,
                                "horas_suplementarias": sup, "horas_extraordinarias": ext})

# Anomalía sembrada: ausencias que superan las horas nominales del mes
for r in ausentismo:
    if r["colaborador_id"] == "COL-0150" and r["periodo"] == "2026-07":
        r["horas_vacaciones"] = 220.0

# --------------------------------------------------------------------------------------
# 9. Parámetros y escenarios
# --------------------------------------------------------------------------------------
parametros = [
    {"parametro_id": "PAR-001", "nombre": "horas_jornada_diaria", "valor": 8, "unidad": "horas/día", "estado": "Aprobado (piloto)",
     "descripcion": "Horas de una jornada completa (40 h semanales). Referencial; validar con política interna y normativa laboral vigente.", "aprobador_sugerido": "Gerencia de Talento Humano"},
    {"parametro_id": "PAR-002", "nombre": "factor_no_productivo", "valor": FACTOR_NP, "unidad": "proporción", "estado": "Aprobado (piloto)",
     "descripcion": "Proporción del tiempo presente no dedicada a actividades medidas (reuniones generales, pausas activas, traslados internos). EXCLUYE capacitación y ausencias, que se toman de datos reales.", "aprobador_sugerido": "Comité de Capacity Management"},
    {"parametro_id": "PAR-003", "nombre": "dias_vacaciones_anuales", "valor": 15, "unidad": "días hábiles/año", "estado": "Supuesto",
     "descripcion": "Días de vacaciones usados para generar datos ficticios. Validar con normativa y política interna (días adicionales por antigüedad no modelados).", "aprobador_sugerido": "Gerencia de Talento Humano"},
    {"parametro_id": "PAR-004", "nombre": "umbral_sobrecarga", "valor": 1.05, "unidad": "utilización", "estado": "Aprobado (piloto)",
     "descripcion": "Utilización por encima de la cual una unidad-cargo se clasifica en Sobrecarga.", "aprobador_sugerido": "Comité de Capacity Management"},
    {"parametro_id": "PAR-005", "nombre": "umbral_subutilizacion", "valor": 0.80, "unidad": "utilización", "estado": "Aprobado (piloto)",
     "descripcion": "Utilización por debajo de la cual una unidad-cargo se clasifica en Holgura.", "aprobador_sugerido": "Comité de Capacity Management"},
    {"parametro_id": "PAR-006", "nombre": "agregacion_minima_reporte", "valor": 3, "unidad": "personas", "estado": "Aprobado (piloto)",
     "descripcion": "Número mínimo de personas en un grupo para mostrar indicadores sin exponer información individual.", "aprobador_sugerido": "Oficial de Protección de Datos"},
    {"parametro_id": "PAR-007", "nombre": "periodo_base_inicio", "valor": PERIODOS[0], "unidad": "AAAA-MM", "estado": "Supuesto", "descripcion": "Primer mes del período base.", "aprobador_sugerido": "Comité de Capacity Management"},
    {"parametro_id": "PAR-008", "nombre": "periodo_base_fin", "valor": PERIODOS[-1], "unidad": "AAAA-MM", "estado": "Supuesto", "descripcion": "Último mes del período base.", "aprobador_sugerido": "Comité de Capacity Management"},
    {"parametro_id": "PAR-009", "nombre": "fecha_corte_dotacion", "valor": FIN.isoformat(), "unidad": "fecha", "estado": "Supuesto", "descripcion": "Fecha de corte para dotación actual.", "aprobador_sugerido": "Gerencia de Talento Humano"},
]

escenarios = [
    ("ESC-BASE", "Base 2027", "Crecimiento orgánico del negocio", "GLOBAL", "", "volumen_pct", 0.04),
    ("ESC-DIG", "Migración digital", "Crecimiento base + migración de transacciones a canales digitales", "GLOBAL", "", "volumen_pct", 0.04),
    ("ESC-DIG", "Migración digital", "Menos transacciones en caja", "PROCESO", "P-CAJ", "volumen_pct", -0.18),
    ("ESC-DIG", "Migración digital", "Menos servicios presenciales", "PROCESO", "P-SER", "volumen_pct", -0.12),
    ("ESC-DIG", "Migración digital", "Más atención digital en centro de contacto", "ACTIVIDAD", "ACT-103", "volumen_pct", 0.35),
    ("ESC-AUT", "Automatización back office", "Crecimiento base", "GLOBAL", "", "volumen_pct", 0.04),
    ("ESC-AUT", "Automatización back office", "Validación automática de transferencias SPI", "ACTIVIDAD", "ACT-050", "tiempo_pct", -0.40),
    ("ESC-AUT", "Automatización back office", "Lectura automática (OCR) de documentos de apertura", "ACTIVIDAD", "ACT-060", "tiempo_pct", -0.30),
    ("ESC-AUT", "Automatización back office", "Robot de conciliación SPI", "ACTIVIDAD", "ACT-054", "tiempo_pct", -0.50),
    ("ESC-CRE", "Crecimiento comercial", "Crecimiento base", "GLOBAL", "", "volumen_pct", 0.04),
    ("ESC-CRE", "Crecimiento comercial", "Plan comercial agresivo en crédito", "PROCESO", "P-NEG", "volumen_pct", 0.15),
    ("ESC-CRE", "Crecimiento comercial", "Más operaciones de crédito a procesar", "PROCESO", "P-OCR", "volumen_pct", 0.12),
]
escenarios_rows = [{"escenario_id": e[0], "nombre_escenario": e[1], "descripcion_ajuste": e[2], "ambito_tipo": e[3],
                    "ambito_id": e[4], "variable": e[5], "valor": e[6], "estado": "Supuesto"} for e in escenarios]

# --------------------------------------------------------------------------------------
# Escritura
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generando datos ficticios en {OUT.relative_to(ROOT)}/ (semilla {SEED})")
    escribir("01_estructura_organizacional.csv", estructura, ["unidad_id", "nombre", "nivel", "unidad_padre_id", "ciudad", "provincia", "tipo_unidad"])
    escribir("02_cargos.csv", cargos_rows, ["cargo_id", "nombre_cargo", "familia", "nivel_jerarquico", "tipo_rol"])
    escribir("03_colaboradores.csv", colaboradores, ["colaborador_id", "unidad_id", "cargo_id", "fecha_ingreso", "fecha_salida", "tipo_contrato", "jornada_horas_semana", "modalidad"])
    escribir("04_calendario_laboral.csv", calendario, ["fecha", "periodo", "dia_semana", "es_laborable", "feriado"])
    escribir("05_parametros.csv", parametros, ["parametro_id", "nombre", "valor", "unidad", "estado", "descripcion", "aprobador_sugerido"])
    escribir("06_procesos.csv", procesos_rows, ["proceso_id", "nombre_proceso", "macroproceso", "cargo_dueno_proceso", "grupo_estacional"])
    escribir("07_actividades.csv", actividades_rows, ["actividad_id", "proceso_id", "nombre_actividad", "cargo_id", "unidad_trabajo", "tiempo_estandar_min", "tiempo_reproceso_min", "metodo_medicion", "fecha_medicion", "ambito", "tipo_actividad"])
    escribir("08_volumenes_mensuales.csv", volumenes, ["periodo", "unidad_id", "actividad_id", "volumen", "fuente"])
    escribir("09_reprocesos.csv", reprocesos, ["periodo", "unidad_id", "actividad_id", "cantidad_reprocesos", "causa_principal"])
    escribir("10_ausentismo.csv", ausentismo, ["colaborador_id", "periodo", "horas_vacaciones", "horas_enfermedad", "horas_permisos", "horas_licencias", "horas_capacitacion"])
    escribir("11_horas_extra.csv", horas_extra, ["colaborador_id", "periodo", "horas_suplementarias", "horas_extraordinarias"])
    escribir("12_movimientos_personal.csv", movimientos, ["movimiento_id", "colaborador_id", "tipo_movimiento", "fecha", "unidad_id", "cargo_id", "motivo"])
    escribir("13_vacantes.csv", vacantes, ["vacante_id", "unidad_id", "cargo_id", "motivo", "fecha_apertura", "fecha_cierre", "estado"])
    escribir("14_escenarios_2027.csv", escenarios_rows, ["escenario_id", "nombre_escenario", "descripcion_ajuste", "ambito_tipo", "ambito_id", "variable", "valor", "estado"])
    print(f"Posiciones del piloto: {len(posiciones)} | Colaboradores (incl. reemplazos): {len(reales)}")
