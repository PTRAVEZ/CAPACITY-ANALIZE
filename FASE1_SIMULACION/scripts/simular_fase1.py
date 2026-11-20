#!/usr/bin/env python3
"""
CAPACITY-ANALIZE · Simulación de la Fase 1 (piloto de 12 semanas) con datos FICTICIOS.

Recrea, de forma reproducible, lo que pasaría en el piloto con datos "reales" del Banco Volcán Azul (ficticio):
  1. Tres rondas de carga de las 14 fuentes, con los errores típicos de una primera entrega,
     revisadas con el validador de FASE1_ARRANQUE (esquema S-01..S-11 y reglas V-01..V-16).
  2. Estudio de tiempos de 5 actividades (incluida ACT-017, pendiente de medición) en el formulario oficial.
  3. Carga final con los nuevos tiempos estándar y cálculo con el motor del demostrador.
  4. Validación de los resultados con las jefaturas (criterio de salida: ≥ 95 % de coincidencia).
  5. Documentos del piloto con las cifras calculadas: bitácora de carga, estudio de tiempos,
     informe mensual 01, validación de jefaturas, acta del Comité sesión 2 y cierre de la fase.

Uso:  python FASE1_SIMULACION/scripts/simular_fase1.py
Todo lo que está en FASE1_SIMULACION/trabajo/ se regenera y no se versiona.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import time, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parent
DEMO = REPO / "DATOS" / "BANCO-VOLCAN-AZUL"
DEMO_IN = DEMO / "data" / "input"
DEMO_OUT = DEMO / "data" / "output"
ARRANQUE = REPO / "FASE1_ARRANQUE"
VALIDADOR = ARRANQUE / "scripts" / "validar_carga.py"
FORMULARIO = ARRANQUE / "plantillas" / "FORMULARIO_ESTUDIO_TIEMPOS.xlsx"
TRAB = BASE / "trabajo"          # cargas completas (se regeneran, no se versionan)
RES = BASE / "resultados"        # salidas pequeñas que sí se versionan
DOCS = BASE                      # documentos .md generados
SEMILLA = 20261123

sys.path.insert(0, str(DEMO / "src"))
import capacity_analize as ca  # noqa: E402

ACTIVIDADES_ESTUDIO = {  # actividad: (unidades donde se mide, sesgo real vs. estándar vigente)
    "ACT-017": (["AG-QMA", "AG-QNO", "AG-VCH"], None),
    "ACT-001": (["AG-QMA", "AG-QSU", "AG-AMB"], 1.09),
    "ACT-002": (["AG-QMA", "AG-CUM", "AG-RIO"], 1.02),
    "ACT-020": (["AG-QMA", "AG-QNO", "AG-AMB"], 1.12),
    "ACT-010": (["AG-QNO", "AG-LAT", "AG-IBA"], 0.96),
}
T_REAL_ACT017 = 21.5   # minutos por caso (valor "real" que el estudio debe descubrir)
UMBRAL_DISCREPANCIA = 0.02  # la jefatura discrepa si la utilización está a menos de 2 puntos de un umbral


# --------------------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------------------
def leer(d: Path, arch: str) -> pd.DataFrame:
    return pd.read_csv(d / arch, dtype=str, keep_default_na=False)


def guardar(df: pd.DataFrame, d: Path, arch: str):
    df.to_csv(d / arch, index=False)


def copiar(origen: Path, destino: Path):
    if destino.exists():
        shutil.rmtree(destino)
    shutil.copytree(origen, destino)


def validar(carpeta: Path, nombre: str) -> tuple[int, pd.DataFrame]:
    salida = RES / f"validacion_{nombre}.csv"
    p = subprocess.run([sys.executable, str(VALIDADOR), "--dir", str(carpeta), "--salida", str(salida)],
                       capture_output=True, text=True)
    return p.returncode, pd.read_csv(salida)


def resumen_val(rep: pd.DataFrame) -> dict:
    return {
        "esq_err": int(((rep.etapa == "Esquema") & (rep.severidad == "ERROR")).sum()),
        "reg_err": int(((rep.etapa == "Reglas") & (rep.severidad == "ERROR")).sum()),
        "adv": int((rep.severidad == "ADVERTENCIA").sum()),
    }


def md_tabla(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    filas = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        filas.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(filas)


def f1(x):
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def f0(x):
    return f"{x:,.0f}".replace(",", ".")


def sgn(x):
    return f"{x:+.1f}".replace(".", ",").replace("-", "−")


def pct(x):
    return f"{x * 100:.0f} %"


# --------------------------------------------------------------------------------------
# 1. Rondas de carga
# --------------------------------------------------------------------------------------
def ronda1(dest: Path, rng):
    """Primera entrega de los dueños de fuentes: datos crudos + errores típicos."""
    copiar(DEMO_IN, dest)
    col = leer(dest, "03_colaboradores.csv")
    col.insert(1, "cedula", [f"17{rng.integers(10**7, 10**8)}" for _ in range(len(col))])  # S-04: dato personal
    idx = col.index[col.modalidad == "Híbrida"][:6]
    col.loc[idx, "modalidad"] = "Hibrido"                                            # S-08: valor fuera de lista
    guardar(col, dest, "03_colaboradores.csv")
    aus = leer(dest, "10_ausentismo.csv")
    m = aus.periodo == "2026-09"
    aus.loc[m, "periodo"] = aus.loc[m, "periodo"].str.slice(5, 7) + "/" + aus.loc[m, "periodo"].str.slice(0, 4)  # S-06
    guardar(aus, dest, "10_ausentismo.csv")
    (dest / "13_vacantes.csv").unlink()                                              # S-01: fuente no entregada
    return {"cedula": len(col), "modalidad": len(idx), "periodo": int(m.sum())}


def ronda2(r1: Path, dest: Path):
    """Corrección de esquema: queda lo que solo detectan las reglas de negocio."""
    copiar(r1, dest)
    col = leer(dest, "03_colaboradores.csv").drop(columns=["cedula"])
    col["modalidad"] = col.modalidad.replace({"Hibrido": "Híbrida"})
    guardar(col, dest, "03_colaboradores.csv")
    aus = leer(dest, "10_ausentismo.csv")
    m = aus.periodo.str.contains("/")
    aus.loc[m, "periodo"] = aus.loc[m, "periodo"].str.slice(3, 7) + "-" + aus.loc[m, "periodo"].str.slice(0, 2)
    guardar(aus, dest, "10_ausentismo.csv")
    shutil.copy(DEMO_IN / "13_vacantes.csv", dest / "13_vacantes.csv")
    vol = leer(dest, "08_volumenes_mensuales.csv")
    n0 = len(vol)
    vol = vol[pd.to_numeric(vol.volumen) >= 0].drop_duplicates(["periodo", "unidad_id", "actividad_id"])
    guardar(vol, dest, "08_volumenes_mensuales.csv")
    return {"vol_filas_quitadas": n0 - len(vol)}


def ronda3(r2: Path, dest: Path):
    """Corrección de reglas por los dueños de fuentes + parámetros aprobados en los Bloques 3 y 4."""
    copiar(r2, dest)
    col = leer(dest, "03_colaboradores.csv")
    col = col[~col.colaborador_id.isin(["COL-9001", "COL-9002"])]       # registros de prueba de nómina
    guardar(col, dest, "03_colaboradores.csv")
    vol = leer(dest, "08_volumenes_mensuales.csv")
    vol = vol[vol.actividad_id != "ACT-999"]                             # código de prueba del core
    guardar(vol, dest, "08_volumenes_mensuales.csv")
    aus = leer(dest, "10_ausentismo.csv")
    m = (aus.colaborador_id == "COL-0150") & (aus.periodo == "2026-07")
    aus.loc[m, "horas_vacaciones"] = "88.0"                              # 220 h era el saldo acumulado
    guardar(aus, dest, "10_ausentismo.csv")
    par = leer(dest, "05_parametros.csv")
    par.loc[par.parametro_id.isin(["PAR-001", "PAR-002", "PAR-004", "PAR-005"]), "estado"] = "Aprobado (piloto)"
    par.loc[par.parametro_id == "PAR-006", "estado"] = "Aprobado"
    guardar(par, dest, "05_parametros.csv")


# --------------------------------------------------------------------------------------
# 2. Estudio de tiempos
# --------------------------------------------------------------------------------------
def estudio_tiempos(carga: Path, rng) -> tuple[pd.DataFrame, pd.DataFrame]:
    act = leer(carga, "07_actividades.csv").set_index("actividad_id")
    col = leer(carga, "03_colaboradores.csv")
    obs = []
    for a, (unidades, sesgo) in ACTIVIDADES_ESTUDIO.items():
        t_vig = float(act.loc[a, "tiempo_estandar_min"])
        t_real = T_REAL_ACT017 if sesgo is None else t_vig * sesgo
        cargo = act.loc[a, "cargo_id"]
        dia0 = datetime(2026, 12, 14)
        for i in range(32):
            u = unidades[i % 3]
            pool = col[(col.unidad_id == u) & (col.cargo_id == cargo) & (col.fecha_salida == "")].colaborador_id.tolist()
            unidades_trab = 1 if t_real >= 5 else int(rng.integers(3, 7))
            dur = max(t_real * unidades_trab * rng.lognormal(0, 0.18), 0.3)
            dia = dia0 + timedelta(days=int(i // 3 * 2 + (1 if (i // 3) % 5 == 4 else 0)))
            while dia.weekday() >= 5 or dia.strftime("%m-%d") in ("12-25", "01-01"):
                dia += timedelta(days=1)
            ini = datetime.combine(dia.date(), time(9, 0)) + timedelta(minutes=int(rng.integers(0, 420)), seconds=int(rng.integers(0, 60)))
            fin = ini + timedelta(seconds=round(dur * 60))
            obs.append({"fecha": dia.strftime("%Y-%m-%d"), "unidad_id": u, "actividad_id": a,
                        "observador": f"Jefatura {u}", "colaborador_id": pool[i % len(pool)],
                        "hora_inicio": ini.time(), "hora_fin": fin.time(),
                        "duracion_min": (fin - ini).total_seconds() / 60, "unidades": unidades_trab, "es_reproceso": "N"})
    obs = pd.DataFrame(obs)
    obs["min_por_unidad"] = obs.duracion_min / obs.unidades
    res = obs.groupby("actividad_id").min_por_unidad.agg(observaciones="count", promedio="mean", mediana="median").reset_index()
    res["nombre_actividad"] = res.actividad_id.map(act.nombre_actividad)
    res["estandar_vigente"] = res.actividad_id.map(lambda a: float(act.loc[a, "tiempo_estandar_min"]))
    res["estandar_nuevo"] = np.floor(res.mediana * 10 + 0.5) / 10   # redondeo comercial a 0,1 min
    res["variacion"] = np.where(res.estandar_vigente > 0, res.estandar_nuevo / res.estandar_vigente - 1, np.nan)
    res = res.set_index("actividad_id").loc[list(ACTIVIDADES_ESTUDIO)].reset_index()

    # Formulario oficial completado (las fórmulas del formulario recalculan al abrirlo)
    wb = load_workbook(FORMULARIO)
    ws = wb["Registro"]
    for i, r in obs.iterrows():
        f = i + 2
        ws.cell(f, 1, r.fecha); ws.cell(f, 2, r.unidad_id); ws.cell(f, 3, r.actividad_id)
        ws.cell(f, 4, r.observador); ws.cell(f, 5, r.colaborador_id)
        ws.cell(f, 6, r.hora_inicio); ws.cell(f, 7, r.hora_fin)
        ws.cell(f, 6).number_format = ws.cell(f, 7).number_format = "hh:mm:ss"
        ws.cell(f, 9, int(r.unidades)); ws.cell(f, 11, r.es_reproceso)
    rs = wb["Resumen"]
    for j, a in enumerate(ACTIVIDADES_ESTUDIO, start=2):
        rs.cell(j, 1, a)
    wb.save(RES / "FORMULARIO_ESTUDIO_TIEMPOS_completado.xlsx")
    obs.drop(columns=["hora_inicio", "hora_fin"]).round(3).to_csv(RES / "estudio_tiempos_observaciones.csv", index=False)
    res.round(4).to_csv(RES / "estudio_tiempos_resultado.csv", index=False)
    return obs, res


def carga_final(r3: Path, dest: Path, est: pd.DataFrame) -> int:
    copiar(r3, dest)
    act = leer(dest, "07_actividades.csv")
    for _, r in est.iterrows():
        m = act.actividad_id == r.actividad_id
        act.loc[m, "tiempo_estandar_min"] = f"{r.estandar_nuevo:.1f}"
        act.loc[m, "metodo_medicion"] = "Estudio de tiempos"
        act.loc[m, "fecha_medicion"] = "2027-01-08"
    guardar(act, dest, "07_actividades.csv")
    # ACT-017 ya se atendía en agencias, pero no se registraba: se incorpora su volumen (25 % de los reclamos en agencia)
    vol = leer(dest, "08_volumenes_mensuales.csv")
    rec = vol[vol.actividad_id == "ACT-015"].copy()
    rec["actividad_id"] = "ACT-017"
    rec["volumen"] = (pd.to_numeric(rec.volumen) * 0.25).round().astype(int).astype(str)
    rec["fuente"] = "Herramienta de gestión de redes sociales"
    vol = pd.concat([vol, rec], ignore_index=True)
    guardar(vol, dest, "08_volumenes_mensuales.csv")
    return int(pd.to_numeric(rec.volumen).sum())


# --------------------------------------------------------------------------------------
# 3. Validación con jefaturas
# --------------------------------------------------------------------------------------
def validacion_jefaturas(res: pd.DataFrame, P: dict) -> tuple[pd.DataFrame, float]:
    g = res[res.cumple_agregacion_minima == "S"].copy()
    alto, bajo = P["umbral_sobre"], P["umbral_sub"]
    cerca = (abs(g.utilizacion - alto) < UMBRAL_DISCREPANCIA) | (abs(g.utilizacion - bajo) < UMBRAL_DISCREPANCIA)

    def percepcion(r, es_cerca):
        if not es_cerca:
            return r.estado
        if abs(r.utilizacion - alto) < UMBRAL_DISCREPANCIA:
            return "Equilibrio" if r.estado == "Sobrecarga" else "Sobrecarga"
        return "Equilibrio" if r.estado == "Holgura" else "Holgura"

    g["percepcion_jefatura"] = [percepcion(r, c) for (_, r), c in zip(g.iterrows(), cerca)]
    g["coincide"] = np.where(g.percepcion_jefatura == g.estado, "Sí", "No")
    coincidencia = (g.coincide == "Sí").mean()
    g[["unidad_id", "nombre_unidad", "cargo_id", "nombre_cargo", "dotacion_corte", "utilizacion", "estado",
       "percepcion_jefatura", "coincide"]].round(4).to_csv(RES / "validacion_jefaturas.csv", index=False)
    return g, coincidencia


# --------------------------------------------------------------------------------------
# 4. Documentos
# --------------------------------------------------------------------------------------
def movimientos(ctx) -> list[str]:
    est = pd.read_csv(TRAB / "carga_final" / "01_estructura_organizacional.csv").set_index("unidad_id").nombre
    car = pd.read_csv(TRAB / "carga_final" / "02_cargos.csv").set_index("cargo_id").iloc[:, 0]
    n = lambda u: est.get(u, u).replace("Departamento de ", "").split(" (")[0]
    return [f"{f1(r.fte_movible)} FTE de {car.get(r.cargo_id, r.cargo_id)}: {n(r.unidad_origen)} ({pct(r.utilizacion_origen)}) "
            f"→ {n(r.unidad_destino)} ({pct(r.utilizacion_destino)})" for r in ctx["red"].itertuples()]


NOTA = "> **Simulación con datos ficticios.** Banco Volcán Azul S.A. no existe; fechas, personas y cifras son ilustrativas.\n"


def doc_bitacora(r, ctx):
    t = []
    for nombre, fecha, desc in [("ronda1", "2026-12-07", "Primera entrega de los dueños de fuentes"),
                                ("ronda2", "2026-12-11", "Correcciones de esquema"),
                                ("ronda3", "2026-12-16", "Correcciones de reglas de negocio y parámetros aprobados"),
                                ("final", "2027-01-12", "Nuevos tiempos estándar y volumen de ACT-017")]:
        v = r[nombre]
        t.append({"Ronda": nombre.replace("ronda", "Ronda ").replace("final", "Carga final"), "Fecha": fecha, "Qué cambió": desc,
                  "Errores esquema": v["esq_err"], "Errores reglas": v["reg_err"], "Advertencias": v["adv"],
                  "Resultado": "APTA" if v["codigo"] == 0 else "NO APTA"})
    adv = ctx["rep_final"][ctx["rep_final"].severidad == "ADVERTENCIA"][["regla", "archivo", "registro", "detalle"]]
    return f"""# 03 · Bitácora de carga de datos del piloto

{NOTA}
**Fuentes:** las 14 fuentes del piloto, entregadas por sus dueños (DEC-019 a DEC-026) y revisadas con
`FASE1_ARRANQUE/scripts/validar_carga.py`. Los reportes completos están en `resultados/validacion_*.csv`.

{md_tabla(pd.DataFrame(t))}

## Ronda 1 · Errores típicos de una primera entrega

| Hallazgo | Regla | Corrección pedida |
|---|---|---|
| Nómina incluyó la columna `cedula` ({ctx['r1']['cedula']} filas) | S-04 | Eliminarla: el piloto solo usa seudónimos (DEC-025) |
| {ctx['r1']['modalidad']} colaboradores con modalidad "Hibrido" | S-08 | Usar el valor de la lista: "Híbrida" |
| Ausentismo de septiembre con período "09/2026" ({ctx['r1']['periodo']} filas) | S-06 | Formato AAAA-MM |
| No se entregó `13_vacantes.csv` | S-01 | Talento Humano la envía |
| Un volumen negativo (−350) y un registro duplicado en el core | S-07, S-09 | Corregir en el origen |

## Ronda 2 · Lo que solo ven las reglas de negocio

| Hallazgo | Regla | Causa confirmada por el dueño de la fuente |
|---|---|---|
| COL-9001 en la unidad AG-QCE, que no existe | V-02 | Registro de prueba de nómina: se elimina |
| COL-9002 con salida anterior al ingreso | V-04 | Registro de prueba de nómina: se elimina |
| Volumen de la actividad ACT-999 | V-08 | Código de prueba del core: se elimina |
| COL-0150 con 220 h de vacaciones en julio | V-11 | Era el saldo acumulado; las horas reales son 88 |

En la ronda 3 también se registran como aprobados los parámetros PAR-001, 002, 004 y 005 (piloto) y PAR-006.

## Carga final · Advertencias que quedan (no impiden calcular)

{md_tabla(adv) if len(adv) else "Sin advertencias."}

Las advertencias V-16 corresponden a meses con una vacante abierta: la carga existió y la cubrió otra persona.
Se informan al Comité como observación.

**Lección:** sin el validador, la primera entrega habría producido resultados con datos personales,
una persona inexistente y volúmenes de prueba. Con él, la carga quedó apta en 3 rondas y 7 días hábiles.
"""


def doc_estudio(est, obs, ctx):
    t = est.copy()
    t["Actividad"] = t.actividad_id + " · " + t.nombre_actividad
    t["Obs."] = t.observaciones
    t["Estándar vigente (min)"] = t.estandar_vigente.map(lambda x: "Sin medir" if x == 0 else f1(x))
    t["Mediana medida (min)"] = t.mediana.map(f1)
    t["Nuevo estándar (min)"] = t.estandar_nuevo.map(f1)
    t["Variación"] = t.variacion.map(lambda x: "Nueva" if pd.isna(x) else f"{x * 100:+.0f} %")
    return f"""# 04 · Estudio de tiempos

{NOTA}
**Período de medición:** 14-dic-2026 al 08-ene-2027 · **Observadores:** jefaturas de agencia (3 h cada una, como se acordó).
**Instrumento:** `FASE1_ARRANQUE/plantillas/FORMULARIO_ESTUDIO_TIEMPOS.xlsx`. El formulario completado está en
`resultados/FORMULARIO_ESTUDIO_TIEMPOS_completado.xlsx` ({len(obs)} observaciones, solo con seudónimos).

**Actividades medidas:** ACT-017, que estaba pendiente de medición, y 4 actividades de agencia de alta carga cuyo estándar
supera los 12 meses de antigüedad o fue cuestionado por las jefaturas. ACT-100 (llamadas) no se mide porque su tiempo sale del sistema del centro de contacto.

{md_tabla(t[["Actividad", "Obs.", "Estándar vigente (min)", "Mediana medida (min)", "Nuevo estándar (min)", "Variación"]])}

**Criterio:** se adopta la mediana de al menos 30 observaciones como nuevo tiempo estándar (DEC-024).

## Hallazgos

- **ACT-017, quejas por redes sociales:** ya se atendían en agencia, pero no tenían tiempo estándar ni volumen registrado.
  Era carga invisible: {f0(ctx['vol017'])} casos al año, unas {f0(ctx['h017'])} horas (≈ {f1(ctx['h017'] / ctx['H_PROD'])} FTE).
- **ACT-020, crédito de consumo:** toma más de lo estimado, por el nuevo formulario de ingresos del cliente.
- **ACT-001, depósitos:** sube por la validación adicional de billetes; ACT-010 baja por la apertura digital asistida.
"""


def doc_informe(ctx):
    base, fin = ctx["ger_base"], ctx["ger_fin"]
    rb, rf = ctx["res_base"], ctx["res_fin"]
    k = ["unidad_id", "cargo_id"]
    m = rf.merge(rb[k + ["utilizacion", "brecha_fte"]], on=k, suffixes=("", "_base"))
    m = m[m.cumple_agregacion_minima == "S"]
    m["grupo"] = m.nombre_cargo + " · " + m.nombre_unidad
    sob = m[m.estado == "Sobrecarga"].sort_values("utilizacion", ascending=False)
    hol = m[m.estado == "Holgura"].sort_values("utilizacion")

    def tabla(df):
        x = pd.DataFrame({"Unidad y cargo": df.grupo, "Dotación": df.dotacion_corte,
                          "FTE disponible": df.fte_disponible.map(f1), "FTE requerido": df.fte_requerido.map(f1),
                          "Brecha FTE": df.brecha_fte.map(sgn),
                          "Utilización": df.utilizacion.map(pct), "Línea base": df.utilizacion_base.map(pct)})
        return md_tabla(x)
    g = pd.DataFrame({"Gerencia": fin.gerencia_id, "FTE disponible": fin.fte_disponible.map(f1),
                      "FTE requerido": fin.fte_requerido.map(f1),
                      "Brecha FTE": fin.brecha_fte.map(sgn),
                      "Utilización": fin.utilizacion.map(pct),
                      "Línea base": fin.gerencia_id.map(base.set_index("gerencia_id").utilizacion).map(pct)})
    red = ctx["red"]
    rt = pd.DataFrame({"Desde": red.unidad_origen, "Hacia": red.unidad_destino, "Cargo": red.cargo_id,
                       "FTE": red.fte_movible.map(f1), "Utilización origen → destino":
                       red.utilizacion_origen.map(pct) + " → " + red.utilizacion_destino.map(pct)})
    par = ctx["par"].head(5)
    pt = pd.DataFrame({"Proceso": par.nombre_proceso, "Causa": par.causa_principal, "Horas": par.horas_reproceso.map(f0),
                       "% acumulado": par.pct_acumulado.map(pct)})
    return f"""# 05 · Informe mensual de capacidad · N.º 01

{NOTA}
**Período analizado:** nov-2025 a oct-2026 (línea base del piloto) · **Entregado:** 14-ene-2027, día hábil 9 (meta: día hábil 10).
**Alcance:** Vicepresidencia de Operaciones y Canales · {ctx['dot']} personas · solo grupos de 3 personas o más (PAR-006).

## 1. Resumen

| Indicador | Demostrador (Fase 0) | Piloto · informe 01 |
|---|---|---|
| FTE disponible | {f1(base.fte_disponible.sum())} | {f1(fin.fte_disponible.sum())} |
| FTE requerido | {f1(base.fte_requerido.sum())} | {f1(fin.fte_requerido.sum())} |
| Brecha FTE | {sgn(base.brecha_fte.sum())} | {sgn(fin.brecha_fte.sum())} |
| Utilización global | {pct(base.fte_requerido.sum() / base.fte_disponible.sum())} | {pct(fin.fte_requerido.sum() / fin.fte_disponible.sum())} |
| Grupos en sobrecarga | {ctx['n_sob_base']} | {ctx['n_sob']} |
| Grupos con holgura | {ctx['n_hol_base']} | {ctx['n_hol']} |

**Qué cambió frente al demostrador:** la carga sube {f1(ctx['delta_fte'])} FTE: {f1(ctx['h017'] / ctx['H_PROD'])} por las quejas de redes
sociales (ACT-017), que se atendían pero no se registraban, y {f1(round(ctx['delta_fte'], 1) - round(ctx['h017'] / ctx['H_PROD'], 1))} por los nuevos tiempos estándar.
{"En total, la carga ya supera ligeramente la capacidad disponible" if fin.fte_requerido.sum() > fin.fte_disponible.sum() else "La capacidad sigue siendo suficiente en total"}, y el desbalance entre unidades se mantiene: las mayores brechas siguen en los mismos grupos.

## 2. Por gerencia

{md_tabla(g)}

## 3. Grupos en sobrecarga (más de 105 %)

{tabla(sob)}

## 4. Grupos con holgura (menos de 80 %)

{tabla(hol)}

## 5. Oportunidades antes de contratar

**Redistribución posible:** {f1(red.fte_movible.sum())} FTE entre unidades del mismo cargo y gerencia.

{md_tabla(rt)}

**Reprocesos:** {f0(ctx['h_rep'])} horas al año (≈ {f1(ctx['h_rep'] / ctx['H_PROD'])} FTE). Principales combinaciones proceso-causa:

{md_tabla(pt)}

## 6. Recomendaciones para el Comité

1. **Aprobar los 5 nuevos tiempos estándar** del estudio de tiempos (documento 04).
2. **Evaluar los apoyos temporales entre unidades** (sección 5), revisando distancias y competencias:
{chr(10).join("   - " + m for m in movimientos(ctx))}
3. **Cajeros de la Agencia Matriz Quito:** aun con apoyo, la brecha persiste; Talento Humano analiza una vacante.
4. **Reprocesos:** plan con agencias para reducir documentación incompleta e ingresos no verificables (lista de verificación en la apertura).
5. **Observaciones de datos:** cerrar las advertencias V-16 con Talento Humano.

Detalle completo: `trabajo/salidas/*.csv` (se regenera con el script).
"""


def doc_jefaturas(g, coinc):
    dis = g[g.coincide == "No"]
    dt = pd.DataFrame({"Unidad y cargo": dis.nombre_cargo + " · " + dis.nombre_unidad,
                       "Utilización": dis.utilizacion.map(pct), "Herramienta": dis.estado,
                       "Jefatura": dis.percepcion_jefatura})
    return f"""# 06 · Validación de resultados con las jefaturas

{NOTA}
**Fecha:** 18 al 22-ene-2027 · **Método:** cada jefatura revisó la clasificación de sus grupos (sobrecarga, equilibrio u holgura)
sin ver antes la utilización calculada, y luego se compararon. Detalle: `resultados/validacion_jefaturas.csv`.

| Resultado | Valor |
|---|---|
| Grupos revisados | {len(g)} |
| Coinciden | {(g.coincide == 'Sí').sum()} |
| No coinciden | {len(dis)} |
| **Coincidencia** | **{f1(coinc * 100)} %** (meta: 95 %) |

## Discrepancias

{md_tabla(dt) if len(dis) else "No hubo discrepancias."}

**Resultado:** {"se cumple" if coinc >= 0.95 else "no se cumple"} la meta de 95 %.

Todas las discrepancias están en grupos a menos de 2 puntos de un umbral: la jefatura y la herramienta ven lo mismo,
pero lo clasifican distinto por estar en el límite. Fuera de esa franja, la coincidencia es de 100 %
({len(g) - len(dis)} de {len(g) - len(dis)} grupos).

**Propuesta:** en el informe, marcar como "en el límite" los grupos a ±2 puntos de un umbral, en lugar de forzar una
clasificación, y volver a medir la coincidencia en el informe 02.
"""


def doc_comite2(ctx):
    return f"""# 07 · Comité de Capacidad · Acta de la sesión 2

{NOTA}
**Fecha:** 27-ene-2027 · **Preside:** Vicepresidente de Operaciones y Canales (patrocinador)
**Asisten:** Gerencias de Operaciones Centralizadas, Red de Agencias y Centro de Contacto; Talento Humano; Capacity Management (secretaría).

## Agenda

1. Informe mensual 01 (documento 05)
2. Nuevos tiempos estándar (documento 04)
3. Resultado de la validación con jefaturas (documento 06)
4. Decisiones de dotación

## Decisiones

| N.º | Decisión | Responsable | Fecha |
|---|---|---|---|
| CC-02-01 | Se aprueba el informe mensual 01 como primer período oficial del piloto. | Comité | 27-ene-2027 |
| CC-02-02 | Se aprueban los 5 nuevos tiempos estándar; ACT-017 entra al cálculo con {f1(ctx['t017'])} min por caso. | Capacity Management | 29-ene-2027 |
| CC-02-03 | Apoyos temporales por 3 meses, previa revisión de competencias y distancias: {"; ".join(movimientos(ctx))}. | Gerencias de Operaciones Centralizadas y de Red de Agencias | 15-feb-2027 |
| CC-02-04 | Cajeros de la Agencia Matriz: Talento Humano analiza una vacante, porque la brecha persiste aun con el apoyo. | Talento Humano | 15-feb-2027 |
| CC-02-05 | Plan de reducción de reprocesos en apertura de cuentas: lista de verificación documental en agencias. Meta: −20 % de horas de reproceso en 6 meses. | Gerencia de Red de Agencias | 28-feb-2027 |
| CC-02-06 | La coincidencia con jefaturas fue {f1(ctx['coinc'] * 100)} %, por debajo de la meta de 95 %. Como todas las discrepancias están en el límite, desde el informe 02 los grupos a ±2 puntos de un umbral se informarán como "en el límite" y la coincidencia se medirá de nuevo. | Capacity Management | Informe 02 |

**Recordatorio del Comité:** las holguras se usan para apoyar a otras unidades o absorber crecimiento, no para recortar
personal (respaldo de Talento Humano confirmado antes del piloto).

**Próxima sesión:** 24-feb-2027 (informe mensual 02).
"""


def doc_cierre(ctx):
    crit = [
        ("Trazabilidad de cada cifra hasta su fuente", "Cumple", "Bitácora de carga, reportes del validador y salidas del motor versionados"),
        ("Coincidencia con la validación de jefaturas ≥ 95 %", "Cumple" if ctx["coinc"] >= 0.95 else "Cumple parcialmente",
         f"{f1(ctx['coinc'] * 100)} %; todas las discrepancias en el límite de un umbral (documento 06)"),
        ("Resultados disponibles hasta el día hábil 10", "Cumple", "Informe 01 entregado el día hábil 9"),
        ("Primer período aprobado por el Comité", "Cumple", "Decisión CC-02-01"),
        ("Privacidad: sin datos personales y grupos de 3 o más", "Cumple", "Columna cédula rechazada en la ronda 1 (S-04); PAR-006 aplicado"),
        ("Esfuerzo de las jefaturas dentro de lo acordado", "Cumple", "3 h de medición y 30 min de revisión por jefatura"),
    ]
    ct = pd.DataFrame(crit, columns=["Criterio de salida", "Resultado", "Evidencia"])
    return f"""# 08 · Cierre de la Fase 1 (piloto)

{NOTA}
**Fecha:** 12-feb-2027 · **Duración real:** 12 semanas (23-nov-2026 al 12-feb-2027).

## Criterios de salida

{md_tabla(ct)}

## Resultados del piloto

- Carga de las 14 fuentes apta en 3 rondas; el validador detectó {ctx['n_err_total']} errores antes de calcular.
- 5 tiempos estándar actualizados y una actividad invisible (ACT-017) incorporada: +{f1(ctx['delta_fte'])} FTE de carga
  ({f1(ctx['h017'] / ctx['H_PROD'])} por ACT-017 y {f1(round(ctx['delta_fte'], 1) - round(ctx['h017'] / ctx['H_PROD'], 1))} por los nuevos estándares).
- Primer informe mensual aprobado y 6 decisiones del Comité, ninguna de reducción de personal.
- Oportunidades identificadas antes de contratar: {f1(ctx['fte_red'])} FTE redistribuibles y {f1(ctx['h_rep'] / ctx['H_PROD'])} FTE en reprocesos.

## Lecciones aprendidas

1. La primera entrega de datos siempre trae errores: hay que reservar al menos 2 semanas para las rondas de carga.
2. El estudio de tiempos encontró carga invisible: vale la pena medir las actividades "pendientes" antes de concluir.
3. Los grupos en el límite generan discusión: conviene informarlos como "en el límite".
4. El mensaje del patrocinador al inicio evitó el temor a despidos.

## Recomendación

**Pasar a la Fase 2 (aplicación web, ≈ 4 meses)** manteniendo el informe mensual con el proceso actual mientras se construye.
{"" if ctx["coinc"] >= 0.95 else "La aprobación queda **condicionada** a que el informe 02, ya con la franja «en el límite», alcance al menos 95 % de coincidencia con las jefaturas. "}Requisitos para iniciarla: designar al equipo de Tecnología (PEN-009) y confirmar el respaldo de Seguridad de la Información (PEN-008).

| Decisión pedida al patrocinador | Estado |
|---|---|
| Aprobar el cierre de la Fase 1 | Aprobado (simulado) · 12-feb-2027 |
| Aprobar el inicio de la Fase 2 | {"Pendiente de presupuesto de Tecnología" if ctx["coinc"] >= 0.95 else "Condicionado al informe 02 y al presupuesto de Tecnología"} |
"""


# --------------------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(SEMILLA)
    TRAB.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
    r = {}
    ctx = {}
    ctx["r1"] = ronda1(TRAB / "carga_ronda1", rng)
    ctx["r2"] = ronda2(TRAB / "carga_ronda1", TRAB / "carga_ronda2")
    ronda3(TRAB / "carga_ronda2", TRAB / "carga_ronda3")
    for n in ("ronda1", "ronda2", "ronda3"):
        cod, rep = validar(TRAB / f"carga_{n}", n)
        r[n] = {**resumen_val(rep), "codigo": cod}
    obs, est = estudio_tiempos(TRAB / "carga_ronda3", rng)
    ctx["vol017"] = carga_final(TRAB / "carga_ronda3", TRAB / "carga_final", est)
    cod, rep = validar(TRAB / "carga_final", "final")
    r["final"] = {**resumen_val(rep), "codigo": cod}
    ctx["rep_final"] = rep
    if cod != 0:
        raise SystemExit("La carga final no quedó apta: revise resultados/validacion_final.csv")

    out = ca.ejecutar(TRAB / "carga_final", TRAB / "salidas", TRAB / "reportes")
    P, res, H_PROD = out["P"], out["res"], out["H_PROD"]
    ctx.update(H_PROD=H_PROD, res_fin=res, ger_fin=out["ger"], par=out["par"])
    ctx["res_base"] = pd.read_csv(DEMO_OUT / "04_resumen_anual_unidad_cargo.csv")
    ctx["ger_base"] = pd.read_csv(DEMO_OUT / "06_resumen_anual_gerencia.csv")
    ctx["red"] = pd.read_csv(TRAB / "salidas" / "09_oportunidades_redistribucion.csv")
    act = pd.read_csv(TRAB / "salidas" / "07_carga_anual_por_actividad.csv")
    ctx["h017"] = act[act.actividad_id == "ACT-017"].horas_carga.sum()
    ctx["t017"] = float(est.set_index("actividad_id").loc["ACT-017", "estandar_nuevo"])
    ctx["h_rep"] = pd.read_csv(TRAB / "salidas" / "08_reprocesos_por_causa.csv").horas_reproceso.sum()
    ctx["dot"] = int(out["conc"]["dotacion_corte"])
    vis = lambda d: d[d.cumple_agregacion_minima == "S"]
    ctx["n_sob"], ctx["n_hol"] = (vis(res).estado == "Sobrecarga").sum(), (vis(res).estado == "Holgura").sum()
    ctx["n_sob_base"], ctx["n_hol_base"] = (vis(ctx["res_base"]).estado == "Sobrecarga").sum(), (vis(ctx["res_base"]).estado == "Holgura").sum()
    g, coinc = validacion_jefaturas(res, P)
    ctx["coinc"] = coinc
    ctx["delta_fte"] = out["ger"].fte_requerido.sum() - ctx["ger_base"].fte_requerido.sum()
    ctx["fte_red"] = ctx["red"].fte_movible.sum()
    ctx["n_err_total"] = r["ronda1"]["esq_err"] + r["ronda2"]["reg_err"]

    res.round(4).to_csv(RES / "resumen_unidad_cargo_piloto.csv", index=False)
    out["ger"].round(4).to_csv(RES / "resumen_gerencia_piloto.csv", index=False)

    docs = {"03_BITACORA_CARGA_DATOS.md": doc_bitacora(r, ctx),
            "04_ESTUDIO_TIEMPOS.md": doc_estudio(est, obs, ctx),
            "05_INFORME_MENSUAL_01.md": doc_informe(ctx),
            "06_VALIDACION_JEFATURAS.md": doc_jefaturas(g, coinc),
            "07_COMITE_SESION_02.md": doc_comite2(ctx),
            "08_CIERRE_FASE1.md": doc_cierre(ctx)}
    for n, t in docs.items():
        (DOCS / n).write_text(t, encoding="utf-8")

    print("CAPACITY-ANALIZE · Simulación de la Fase 1 (datos ficticios)")
    for n, v in r.items():
        print(f"  Carga {n:<7} esquema {v['esq_err']:>2} err | reglas {v['reg_err']:>2} err | {v['adv']:>2} adv | {'APTA' if v['codigo'] == 0 else 'NO APTA'}")
    print(f"  FTE disponible {out['ger'].fte_disponible.sum():.1f} | requerido {out['ger'].fte_requerido.sum():.1f} | "
          f"carga nueva vs. demostrador {ctx['delta_fte']:+.1f} FTE")
    print(f"  Coincidencia con jefaturas: {f1(coinc * 100)} % ({len(g)} grupos)")
    print(f"  Documentos generados: {', '.join(docs)}")


if __name__ == "__main__":
    main()
