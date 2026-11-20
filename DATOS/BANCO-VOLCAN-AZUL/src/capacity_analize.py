#!/usr/bin/env python3
"""
CAPACITY-ANALIZE — Motor demostrativo de validación y cálculo de capacidad humana.

IMPORTANTE
- Este script es un DEMOSTRADOR METODOLÓGICO que trabaja con datos FICTICIOS.
- Las fórmulas implementadas son PROPUESTAS (ver docs/metodologia_calculo.md);
  no son fórmulas oficiales de ningún banco hasta que se aprueben formalmente.

Flujo:
  1. Carga de fuentes (data/input/*.csv)
  2. Validación de calidad de datos (reglas V-01 … V-16) → reporte_validacion.csv
  3. Disponibilidad efectiva por colaborador-mes
  4. Carga laboral por actividad (volumen × tiempo estándar + reprocesos)
  5. Capacidad por unidad × cargo × mes (FTE requerido, disponible, brecha, utilización)
  6. Resúmenes anuales, reprocesos, oportunidades de redistribución
  6b. IND-17 productividad, IND-18 estacionalidad, IND-19 dispersión, IND-20 Pareto
  7. Escenarios 2027
  8. Resumen ejecutivo en Markdown (reports/resumen_resultados.md)

Uso:
    python src/capacity_analize.py [--input data/input] [--output data/output] [--reportes reports]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

ARCHIVOS = {
    "estructura": "01_estructura_organizacional.csv",
    "cargos": "02_cargos.csv",
    "colaboradores": "03_colaboradores.csv",
    "calendario": "04_calendario_laboral.csv",
    "parametros": "05_parametros.csv",
    "procesos": "06_procesos.csv",
    "actividades": "07_actividades.csv",
    "volumenes": "08_volumenes_mensuales.csv",
    "reprocesos": "09_reprocesos.csv",
    "ausentismo": "10_ausentismo.csv",
    "horas_extra": "11_horas_extra.csv",
    "movimientos": "12_movimientos_personal.csv",
    "vacantes": "13_vacantes.csv",
    "escenarios": "14_escenarios_2027.csv",
}


# ======================================================================================
# 1. Carga
# ======================================================================================
def cargar(dir_in: Path) -> dict[str, pd.DataFrame]:
    dfs = {}
    for k, f in ARCHIVOS.items():
        dfs[k] = pd.read_csv(dir_in / f, dtype=str, keep_default_na=False)
    num = {
        "colaboradores": ["jornada_horas_semana"],
        "actividades": ["tiempo_estandar_min", "tiempo_reproceso_min"],
        "volumenes": ["volumen"],
        "reprocesos": ["cantidad_reprocesos"],
        "ausentismo": ["horas_vacaciones", "horas_enfermedad", "horas_permisos", "horas_licencias", "horas_capacitacion"],
        "horas_extra": ["horas_suplementarias", "horas_extraordinarias"],
        "escenarios": ["valor"],
    }
    for k, cols in num.items():
        for c in cols:
            dfs[k][c] = pd.to_numeric(dfs[k][c], errors="coerce")
    for c in ("fecha_ingreso", "fecha_salida"):
        dfs["colaboradores"][c] = pd.to_datetime(dfs["colaboradores"][c].replace("", None))
    dfs["calendario"]["fecha"] = pd.to_datetime(dfs["calendario"]["fecha"])
    return dfs


def parametros(dfs) -> dict:
    p = dict(zip(dfs["parametros"]["nombre"], dfs["parametros"]["valor"]))
    return {
        "horas_dia": float(p["horas_jornada_diaria"]),
        "f_np": float(p["factor_no_productivo"]),
        "umbral_sobre": float(p["umbral_sobrecarga"]),
        "umbral_sub": float(p["umbral_subutilizacion"]),
        "agreg_min": int(float(p["agregacion_minima_reporte"])),
        "per_ini": p["periodo_base_inicio"],
        "per_fin": p["periodo_base_fin"],
        "corte": pd.Timestamp(p["fecha_corte_dotacion"]),
    }


# ======================================================================================
# 2. Validación
# ======================================================================================
class Bitacora:
    def __init__(self):
        self.filas = []

    def add(self, regla, severidad, archivo, registro, detalle, accion):
        self.filas.append({"regla": regla, "severidad": severidad, "archivo": archivo,
                           "registro": registro, "detalle": detalle, "accion": accion})

    def df(self):
        return pd.DataFrame(self.filas, columns=["regla", "severidad", "archivo", "registro", "detalle", "accion"])


def validar(dfs, P, log: Bitacora) -> dict[str, pd.DataFrame]:
    d = {k: v.copy() for k, v in dfs.items()}
    unidades = set(d["estructura"]["unidad_id"])
    cargos = set(d["cargos"]["cargo_id"])
    procesos = set(d["procesos"]["proceso_id"])
    periodos = sorted(d["calendario"]["periodo"].unique())

    # V-01 jerarquía organizacional
    e = d["estructura"]
    for _, r in e[(e.unidad_padre_id != "") & (~e.unidad_padre_id.isin(unidades))].iterrows():
        log.add("V-01", "ERROR", ARCHIVOS["estructura"], r.unidad_id, f"Unidad padre {r.unidad_padre_id} no existe", "Revisar estructura")

    # V-02..V-05 colaboradores
    c = d["colaboradores"]
    malos = pd.Series(False, index=c.index)
    for i, r in c.iterrows():
        if r.unidad_id not in unidades:
            log.add("V-02", "ERROR", ARCHIVOS["colaboradores"], r.colaborador_id, f"Unidad {r.unidad_id} no existe en la estructura", "Excluido del cálculo")
            malos[i] = True
        if r.cargo_id not in cargos:
            log.add("V-03", "ERROR", ARCHIVOS["colaboradores"], r.colaborador_id, f"Cargo {r.cargo_id} no existe en el catálogo", "Excluido del cálculo")
            malos[i] = True
        if pd.notna(r.fecha_salida) and r.fecha_salida < r.fecha_ingreso:
            log.add("V-04", "ERROR", ARCHIVOS["colaboradores"], r.colaborador_id, "Fecha de salida anterior a la fecha de ingreso", "Excluido del cálculo")
            malos[i] = True
    dup = c.duplicated("colaborador_id", keep="first")
    for _, r in c[dup].iterrows():
        log.add("V-05", "ERROR", ARCHIVOS["colaboradores"], r.colaborador_id, "Identificador duplicado", "Se conserva el primer registro")
    d["colaboradores"] = c[~malos & ~dup].copy()

    # V-06, V-07 actividades
    a = d["actividades"]
    malos = (~a.cargo_id.isin(cargos)) | (~a.proceso_id.isin(procesos))
    for _, r in a[malos].iterrows():
        log.add("V-06", "ERROR", ARCHIVOS["actividades"], r.actividad_id, "Cargo o proceso inexistente", "Excluida del cálculo")
    sin_t = a.tiempo_estandar_min.isna() | (a.tiempo_estandar_min <= 0)
    for _, r in a[sin_t & ~malos].iterrows():
        log.add("V-07", "ADVERTENCIA", ARCHIVOS["actividades"], r.actividad_id,
                f"Sin tiempo estándar válido (método: {r.metodo_medicion})", "Su carga no se calcula; requiere medición")
    d["actividades"] = a[~malos & ~sin_t].copy()
    acts = set(d["actividades"]["actividad_id"])

    # V-08..V-10, V-14 volúmenes
    v = d["volumenes"]
    m_act = ~v.actividad_id.isin(acts)
    m_uni = ~v.unidad_id.isin(unidades)
    m_neg = v.volumen.isna() | (v.volumen < 0)
    m_per = ~v.periodo.isin(periodos)
    for _, r in v[m_act].iterrows():
        sev = "ADVERTENCIA" if r.actividad_id in set(a.actividad_id) else "ERROR"
        log.add("V-08", sev, ARCHIVOS["volumenes"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}", "Actividad inexistente o excluida", "Excluido del cálculo")
    for _, r in v[m_uni].iterrows():
        log.add("V-08", "ERROR", ARCHIVOS["volumenes"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}", "Unidad inexistente", "Excluido del cálculo")
    for _, r in v[m_neg].iterrows():
        log.add("V-09", "ERROR", ARCHIVOS["volumenes"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}", f"Volumen inválido ({r.volumen})", "Excluido del cálculo")
    for _, r in v[m_per].iterrows():
        log.add("V-14", "ERROR", ARCHIVOS["volumenes"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}", "Período fuera del período base", "Excluido del cálculo")
    v = v[~(m_act | m_uni | m_neg | m_per)]
    dup = v.duplicated(["periodo", "unidad_id", "actividad_id"], keep="first")
    for _, r in v[dup].iterrows():
        log.add("V-10", "ERROR", ARCHIVOS["volumenes"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}", "Registro duplicado", "Se conserva el primer registro")
    d["volumenes"] = v[~dup].copy()

    # V-13 reprocesos
    rp = d["reprocesos"].merge(d["volumenes"][["periodo", "unidad_id", "actividad_id", "volumen"]],
                               on=["periodo", "unidad_id", "actividad_id"], how="left")
    m = rp.volumen.isna() | (rp.cantidad_reprocesos > rp.volumen) | (rp.cantidad_reprocesos < 0)
    for _, r in rp[m].iterrows():
        log.add("V-13", "ERROR", ARCHIVOS["reprocesos"], f"{r.periodo}|{r.unidad_id}|{r.actividad_id}",
                "Reprocesos sin volumen asociado o mayores al volumen", "Excluido del cálculo")
    d["reprocesos"] = rp[~m].drop(columns="volumen").copy()

    # V-12 ausentismo / horas extra de colaboradores inexistentes
    ids = set(d["colaboradores"]["colaborador_id"])
    for k in ("ausentismo", "horas_extra"):
        t = d[k]
        for _, r in t[~t.colaborador_id.isin(ids)].iterrows():
            log.add("V-12", "ERROR", ARCHIVOS[k], f"{r.colaborador_id}|{r.periodo}", "Colaborador inexistente o excluido", "Excluido del cálculo")
        d[k] = t[t.colaborador_id.isin(ids)].copy()

    return d


# ======================================================================================
# 3. Disponibilidad por colaborador-mes
# ======================================================================================
def disponibilidad(d, P, log: Bitacora) -> pd.DataFrame:
    cal = d["calendario"]
    lab = cal[cal.es_laborable == "S"][["fecha", "periodo"]]
    col = d["colaboradores"].copy()
    col["salida_eff"] = col.fecha_salida.fillna(cal.fecha.max())
    x = col[["colaborador_id", "fecha_ingreso", "salida_eff"]].merge(lab, how="cross")
    x = x[(x.fecha >= x.fecha_ingreso) & (x.fecha <= x.salida_eff)]
    dias = x.groupby(["colaborador_id", "periodo"]).size().rename("dias_laborables_activos").reset_index()

    df = dias.merge(col[["colaborador_id", "unidad_id", "cargo_id", "jornada_horas_semana", "fecha_ingreso", "fecha_salida"]], on="colaborador_id")
    df["fte_contrato"] = df.jornada_horas_semana / 40
    df["horas_nominales"] = df.dias_laborables_activos * P["horas_dia"] * df.fte_contrato

    au = d["ausentismo"]
    chk = au.merge(df[["colaborador_id", "periodo"]], how="left", indicator=True)
    for _, r in chk[chk._merge == "left_only"].iterrows():
        log.add("V-12", "ERROR", ARCHIVOS["ausentismo"], f"{r.colaborador_id}|{r.periodo}", "Ausencias en un mes sin días activos", "Excluido del cálculo")
    df = df.merge(au, on=["colaborador_id", "periodo"], how="left")
    cols_aus = ["horas_vacaciones", "horas_enfermedad", "horas_permisos", "horas_licencias"]
    df[cols_aus + ["horas_capacitacion"]] = df[cols_aus + ["horas_capacitacion"]].fillna(0)
    df["horas_ausencias"] = df[cols_aus].sum(axis=1)

    # V-11: ausencias + capacitación no pueden superar horas nominales
    exceso = (df.horas_ausencias + df.horas_capacitacion) > df.horas_nominales + 1e-9
    for _, r in df[exceso].iterrows():
        log.add("V-11", "ADVERTENCIA", ARCHIVOS["ausentismo"], f"{r.colaborador_id}|{r.periodo}",
                f"Ausencias+capacitación ({r.horas_ausencias + r.horas_capacitacion:.1f} h) superan horas nominales ({r.horas_nominales:.1f} h)",
                "Se ajustan proporcionalmente al tope de horas nominales")
    fac = np.where(exceso, df.horas_nominales / (df.horas_ausencias + df.horas_capacitacion).replace(0, np.nan), 1.0)
    for ccol in cols_aus + ["horas_capacitacion", "horas_ausencias"]:
        df[ccol] = df[ccol] * fac

    df["horas_presentes"] = df.horas_nominales - df.horas_ausencias
    base_np = df.horas_presentes - df.horas_capacitacion
    df["horas_no_productivas"] = base_np * P["f_np"]
    df["horas_disponibles"] = base_np - df.horas_no_productivas

    fin_mes = pd.to_datetime(df.periodo + "-01") + pd.offsets.MonthEnd(0)
    df["activo_fin_mes"] = ((df.fecha_ingreso <= fin_mes) & (df.fecha_salida.isna() | (df.fecha_salida >= fin_mes))).astype(int)

    he = d["horas_extra"].copy()
    he["horas_extra"] = he.horas_suplementarias.fillna(0) + he.horas_extraordinarias.fillna(0)
    df = df.merge(he[["colaborador_id", "periodo", "horas_suplementarias", "horas_extraordinarias", "horas_extra"]],
                  on=["colaborador_id", "periodo"], how="left")
    df[["horas_suplementarias", "horas_extraordinarias", "horas_extra"]] = df[["horas_suplementarias", "horas_extraordinarias", "horas_extra"]].fillna(0)
    return df.drop(columns=["fecha_ingreso", "fecha_salida"])


# ======================================================================================
# 4. Carga laboral
# ======================================================================================
def carga(d) -> pd.DataFrame:
    v = d["volumenes"].merge(d["actividades"][["actividad_id", "proceso_id", "cargo_id", "tiempo_estandar_min", "tiempo_reproceso_min"]], on="actividad_id")
    v = v.merge(d["reprocesos"][["periodo", "unidad_id", "actividad_id", "cantidad_reprocesos"]], on=["periodo", "unidad_id", "actividad_id"], how="left")
    v["cantidad_reprocesos"] = v.cantidad_reprocesos.fillna(0)
    v["horas_estandar"] = v.volumen * v.tiempo_estandar_min / 60
    v["horas_reproceso"] = v.cantidad_reprocesos * v.tiempo_reproceso_min / 60
    v["horas_carga"] = v.horas_estandar + v.horas_reproceso
    return v


# ======================================================================================
# 5. Capacidad por unidad × cargo × mes
# ======================================================================================
def capacidad_mensual(disp, cg, d, P, log: Bitacora) -> pd.DataFrame:
    cal = d["calendario"]
    lab_m = cal[cal.es_laborable == "S"].groupby("periodo").size().rename("dias_laborables")
    k = ["periodo", "unidad_id", "cargo_id"]
    da = disp.groupby(k).agg(
        dotacion_fin_mes=("activo_fin_mes", "sum"), personas_en_mes=("colaborador_id", "nunique"),
        horas_nominales=("horas_nominales", "sum"), horas_ausencias=("horas_ausencias", "sum"),
        horas_capacitacion=("horas_capacitacion", "sum"), horas_no_productivas=("horas_no_productivas", "sum"),
        horas_disponibles=("horas_disponibles", "sum"), horas_extra=("horas_extra", "sum")).reset_index()
    ca = cg.groupby(k).agg(horas_estandar=("horas_estandar", "sum"), horas_reproceso=("horas_reproceso", "sum"),
                           horas_carga=("horas_carga", "sum")).reset_index()
    m = da.merge(ca, on=k, how="outer").fillna(0)
    m = m.merge(lab_m, left_on="periodo", right_index=True)
    m["horas_por_fte_nominal"] = m.dias_laborables * P["horas_dia"]
    m["horas_por_fte_productivo"] = m.horas_por_fte_nominal * (1 - P["f_np"])
    m["fte_contractual"] = m.horas_nominales / m.horas_por_fte_nominal
    m["fte_disponible"] = m.horas_disponibles / m.horas_por_fte_productivo
    m["fte_requerido"] = m.horas_carga / m.horas_por_fte_productivo
    m["brecha_fte"] = m.fte_disponible - m.fte_requerido
    m["utilizacion"] = np.where(m.horas_disponibles > 0, m.horas_carga / m.horas_disponibles.replace(0, np.nan), np.nan)
    m["fte_equivalente_horas_extra"] = m.horas_extra / m.horas_por_fte_productivo
    m["estado"] = np.select(
        [m.horas_disponibles <= 0, m.utilizacion > P["umbral_sobre"], m.utilizacion < P["umbral_sub"]],
        ["Carga sin personal", "Sobrecarga", "Holgura"], default="Equilibrio")
    for _, r in m[(m.horas_disponibles <= 0) & (m.horas_carga > 0)].iterrows():
        log.add("V-16", "ADVERTENCIA", "cálculo", f"{r.periodo}|{r.unidad_id}|{r.cargo_id}",
                f"Carga de {r.horas_carga:.1f} h sin personal disponible del cargo", "Revisar asignación de actividad o vacante")
    return m.sort_values(k).reset_index(drop=True)


# ======================================================================================
# 6. Resúmenes
# ======================================================================================
def fte_corte(d, P) -> pd.DataFrame:
    c = d["colaboradores"]
    act = c[(c.fecha_ingreso <= P["corte"]) & (c.fecha_salida.isna() | (c.fecha_salida >= P["corte"]))].copy()
    act["fte"] = act.jornada_horas_semana / 40
    return act.groupby(["unidad_id", "cargo_id"]).agg(dotacion_corte=("colaborador_id", "count"), fte_contractual_corte=("fte", "sum")).reset_index()


def resumen_anual(cap, d, P) -> pd.DataFrame:
    k = ["unidad_id", "cargo_id"]
    s = cap.groupby(k).agg(
        horas_nominales=("horas_nominales", "sum"), horas_ausencias=("horas_ausencias", "sum"),
        horas_capacitacion=("horas_capacitacion", "sum"), horas_disponibles=("horas_disponibles", "sum"),
        horas_estandar=("horas_estandar", "sum"), horas_reproceso=("horas_reproceso", "sum"),
        horas_carga=("horas_carga", "sum"), horas_extra=("horas_extra", "sum"),
        sum_h_nom=("horas_por_fte_nominal", "sum"), sum_h_prod=("horas_por_fte_productivo", "sum"),
        meses_sobrecarga=("estado", lambda x: int((x == "Sobrecarga").sum()))).reset_index()
    # sum_h_* se suma sobre los meses presentes de cada grupo; se normaliza a 12 meses del período base
    cal = d["calendario"]
    lab = cal[cal.es_laborable == "S"].groupby("periodo").size()
    H_NOM = float((lab * P["horas_dia"]).sum())
    H_PROD = H_NOM * (1 - P["f_np"])
    s["fte_contractual_promedio"] = s.horas_nominales / H_NOM
    s["fte_disponible"] = s.horas_disponibles / H_PROD
    s["fte_requerido"] = s.horas_carga / H_PROD
    s["brecha_fte"] = s.fte_disponible - s.fte_requerido
    s["utilizacion"] = s.horas_carga / s.horas_disponibles.replace(0, np.nan)
    s["tasa_indisponibilidad"] = (s.horas_ausencias + s.horas_capacitacion) / s.horas_nominales.replace(0, np.nan)
    s["fte_requerido_dotacion"] = s.fte_requerido / (1 - s.tasa_indisponibilidad.fillna(0))
    s["pct_reproceso"] = s.horas_reproceso / s.horas_carga.replace(0, np.nan)
    s["fte_equivalente_horas_extra"] = s.horas_extra / H_PROD
    s = s.merge(fte_corte(d, P), on=k, how="left").fillna({"dotacion_corte": 0, "fte_contractual_corte": 0})
    s["brecha_dotacion_fte"] = s.fte_contractual_corte - s.fte_requerido_dotacion
    s["estado"] = np.select([s.utilizacion > P["umbral_sobre"], s.utilizacion < P["umbral_sub"]], ["Sobrecarga", "Holgura"], default="Equilibrio")
    s["cumple_agregacion_minima"] = np.where(s.dotacion_corte >= P["agreg_min"], "S", "N")
    s = s.drop(columns=["sum_h_nom", "sum_h_prod"])
    e = d["estructura"].set_index("unidad_id")
    s.insert(1, "nombre_unidad", s.unidad_id.map(e.nombre))
    s.insert(2, "gerencia_id", s.unidad_id.map(gerencia_de(d)))
    s.insert(4, "nombre_cargo", s.cargo_id.map(d["cargos"].set_index("cargo_id").nombre_cargo))
    return s.sort_values(["gerencia_id", "unidad_id", "cargo_id"]).reset_index(drop=True), H_NOM, H_PROD


def gerencia_de(d) -> dict:
    e = d["estructura"].set_index("unidad_id")
    out = {}
    for u in e.index:
        x = u
        while x and e.loc[x, "nivel"] not in ("Gerencia",) and e.loc[x, "unidad_padre_id"]:
            x = e.loc[x, "unidad_padre_id"]
        out[u] = x if e.loc[x, "nivel"] == "Gerencia" else ""
    return out


def agregado(res, por: list[str], P) -> pd.DataFrame:
    cols = ["horas_nominales", "horas_ausencias", "horas_capacitacion", "horas_disponibles", "horas_carga", "horas_reproceso",
            "horas_extra", "fte_contractual_promedio", "fte_disponible", "fte_requerido", "brecha_fte", "fte_requerido_dotacion",
            "dotacion_corte", "fte_contractual_corte", "brecha_dotacion_fte", "fte_equivalente_horas_extra"]
    g = res.groupby(por)[cols].sum().reset_index()
    g["utilizacion"] = g.horas_carga / g.horas_disponibles.replace(0, np.nan)
    g["estado"] = np.select([g.utilizacion > P["umbral_sobre"], g.utilizacion < P["umbral_sub"]], ["Sobrecarga", "Holgura"], default="Equilibrio")
    return g


def carga_actividad(cg, d, H_PROD) -> pd.DataFrame:
    a = cg.groupby(["unidad_id", "actividad_id", "proceso_id", "cargo_id"]).agg(
        volumen_anual=("volumen", "sum"), reprocesos_anual=("cantidad_reprocesos", "sum"),
        horas_estandar=("horas_estandar", "sum"), horas_reproceso=("horas_reproceso", "sum"), horas_carga=("horas_carga", "sum")).reset_index()
    a["fte_requerido"] = a.horas_carga / H_PROD
    tot = a.groupby(["unidad_id", "cargo_id"]).horas_carga.transform("sum")
    a["pct_carga_del_cargo"] = a.horas_carga / tot.replace(0, np.nan)
    a.insert(2, "nombre_actividad", a.actividad_id.map(d["actividades"].set_index("actividad_id").nombre_actividad))
    return a.sort_values(["unidad_id", "horas_carga"], ascending=[True, False]).reset_index(drop=True)


def resumen_reprocesos(cg, d, H_PROD) -> pd.DataFrame:
    r = cg[cg.cantidad_reprocesos > 0].merge(d["reprocesos"][["periodo", "unidad_id", "actividad_id", "causa_principal"]],
                                             on=["periodo", "unidad_id", "actividad_id"], how="left")
    g = r.groupby(["proceso_id", "causa_principal"]).agg(cantidad_reprocesos=("cantidad_reprocesos", "sum"),
                                                       horas_reproceso=("horas_reproceso", "sum")).reset_index()
    g["fte_potencialmente_liberable"] = g.horas_reproceso / H_PROD
    g.insert(1, "nombre_proceso", g.proceso_id.map(d["procesos"].set_index("proceso_id").nombre_proceso))
    return g.sort_values("horas_reproceso", ascending=False).reset_index(drop=True)


def redistribucion(res, d, P) -> pd.DataFrame:
    """Empareja unidades con holgura y con sobrecarga del mismo cargo dentro de la misma gerencia."""
    prov = d["estructura"].set_index("unidad_id").provincia
    filas = []
    for (ger, cargo), g in res.groupby(["gerencia_id", "cargo_id"]):
        don = g[g.utilizacion < P["umbral_sub"]].copy()
        rec = g[g.utilizacion > P["umbral_sobre"]].copy()
        if don.empty or rec.empty:
            continue
        don["excedente"] = don.fte_disponible - don.fte_requerido
        rec["deficit"] = rec.fte_requerido - rec.fte_disponible
        don = don.sort_values("excedente", ascending=False)
        rec = rec.sort_values("deficit", ascending=False)
        for _, rr in rec.iterrows():
            falta = rr.deficit
            for i, dd in don.iterrows():
                mover = np.floor(min(falta, don.at[i, "excedente"]) * 2) / 2  # múltiplos de 0,5 FTE
                if mover < 0.5:
                    continue
                filas.append({"gerencia_id": ger, "cargo_id": cargo, "unidad_origen": dd.unidad_id, "unidad_destino": rr.unidad_id,
                              "misma_provincia": "S" if prov[dd.unidad_id] == prov[rr.unidad_id] else "N",
                              "fte_movible": mover, "utilizacion_origen": dd.utilizacion, "utilizacion_destino": rr.utilizacion,
                              "naturaleza": "Oportunidad a evaluar (no es decisión)"})
                don.at[i, "excedente"] -= mover
                falta -= mover
    return pd.DataFrame(filas)


# ======================================================================================
# 7. Escenarios
# ======================================================================================
def escenarios(cg, res, d, P, H_PROD) -> pd.DataFrame:
    n_meses = cg.periodo.nunique()
    base = cg.groupby(["unidad_id", "cargo_id", "actividad_id", "proceso_id"]).agg(
        horas_estandar=("horas_estandar", "sum"), horas_reproceso=("horas_reproceso", "sum")).reset_index()
    esc = d["escenarios"]
    tasa = res.set_index(["unidad_id", "cargo_id"]).tasa_indisponibilidad
    corte = res.set_index(["unidad_id", "cargo_id"]).fte_contractual_corte
    salida = []
    ids = ["ACTUAL"] + list(dict.fromkeys(esc.escenario_id))
    for eid in ids:
        b = base.copy()
        b["mult_vol"], b["mult_t"] = 1.0, 1.0
        for _, r in esc[esc.escenario_id == eid].iterrows():
            if r.ambito_tipo == "GLOBAL":
                m = pd.Series(True, index=b.index)
            elif r.ambito_tipo == "PROCESO":
                m = b.proceso_id == r.ambito_id
            else:
                m = b.actividad_id == r.ambito_id
            col = "mult_vol" if r.variable == "volumen_pct" else "mult_t"
            b.loc[m, col] *= (1 + r.valor)
        b["horas_carga_anual"] = (b.horas_estandar + b.horas_reproceso) * b.mult_vol * b.mult_t * 12 / n_meses
        g = b.groupby(["unidad_id", "cargo_id"]).horas_carga_anual.sum().reset_index()
        g["escenario_id"] = eid
        g["fte_requerido"] = g.horas_carga_anual / H_PROD
        idx = pd.MultiIndex.from_frame(g[["unidad_id", "cargo_id"]])
        t = tasa.reindex(idx).fillna(0).values
        g["fte_requerido_dotacion"] = g.fte_requerido / (1 - t)
        g["fte_contractual_corte"] = corte.reindex(idx).fillna(0).values
        g["brecha_dotacion_fte"] = g.fte_contractual_corte - g.fte_requerido_dotacion
        salida.append(g)
    out = pd.concat(salida, ignore_index=True)
    out.insert(0, "gerencia_id", out.unidad_id.map(gerencia_de(d)))
    nombres = dict(zip(esc.escenario_id, esc.nombre_escenario))
    nombres["ACTUAL"] = "Situación actual (período base)"
    out.insert(1, "nombre_escenario", out.escenario_id.map(nombres))
    return out


# ======================================================================================
# 7b. Indicadores complementarios IND-17 a IND-20 (aprobados en el Bloque 3)
# ======================================================================================
def productividad(cg, cap, res, d, P) -> pd.DataFrame:
    """IND-17: volumen anual de cada actividad transaccional / FTE disponible anual del cargo en la unidad."""
    act = d["actividades"]
    trans = act[act.unidad_trabajo != "hora"][["actividad_id", "nombre_actividad", "unidad_trabajo"]]
    v = cg.groupby(["unidad_id", "cargo_id", "actividad_id"]).volumen.sum().reset_index().merge(trans, on="actividad_id")
    v = v.merge(res[["unidad_id", "cargo_id", "fte_disponible", "dotacion_corte", "cumple_agregacion_minima"]], on=["unidad_id", "cargo_id"], how="left")
    v = v[v.fte_disponible > 0].copy()
    v["productividad_anual_por_fte"] = v.volumen / v.fte_disponible
    v["productividad_mensual_por_fte"] = v.productividad_anual_por_fte / cg.periodo.nunique()
    med = v.groupby("actividad_id").productividad_anual_por_fte.transform("median")
    v["indice_vs_mediana_actividad"] = v.productividad_anual_por_fte / med
    v["comparables"] = v.groupby("actividad_id").unidad_id.transform("nunique")
    return v.sort_values(["actividad_id", "indice_vs_mediana_actividad"], ascending=[True, False]).reset_index(drop=True)


def estacionalidad(cg, d) -> pd.DataFrame:
    """IND-18: carga del mes / carga mensual promedio, por proceso. Pico si el índice supera 1,10."""
    m = cg.groupby(["proceso_id", "periodo"]).horas_carga.sum().reset_index()
    m["indice_estacional"] = m.horas_carga / m.groupby("proceso_id").horas_carga.transform("mean")
    m["pico"] = np.where(m.indice_estacional > 1.10, "S", "N")
    m.insert(1, "nombre_proceso", m.proceso_id.map(d["procesos"].set_index("proceso_id").nombre_proceso))
    return m.sort_values(["proceso_id", "periodo"]).reset_index(drop=True)


def dispersion(res, P) -> pd.DataFrame:
    """IND-19: coeficiente de variación de la utilización anual entre unidades del mismo cargo y gerencia (al menos 3 unidades)."""
    g = res[res.horas_disponibles > 0].groupby(["gerencia_id", "cargo_id", "nombre_cargo"]).agg(
        unidades=("unidad_id", "nunique"), utilizacion_media=("utilizacion", "mean"),
        utilizacion_min=("utilizacion", "min"), utilizacion_max=("utilizacion", "max"),
        desviacion=("utilizacion", "std")).reset_index()
    g = g[g.unidades >= 3].copy()
    g["coef_variacion"] = g.desviacion / g.utilizacion_media
    g["carga_desigual"] = np.where(g.coef_variacion > 0.20, "S", "N")
    return g.sort_values("coef_variacion", ascending=False).reset_index(drop=True)


def pareto_causas(rep) -> pd.DataFrame:
    """IND-20: ranking de horas de reproceso por proceso y causa, con porcentaje acumulado y clase A/B/C."""
    p = rep.sort_values("horas_reproceso", ascending=False).reset_index(drop=True).copy()
    tot = p.horas_reproceso.sum()
    p["pct"] = p.horas_reproceso / tot
    p["pct_acumulado"] = p.pct.cumsum()
    p["clase"] = np.select([p.pct_acumulado.shift(fill_value=0) < 0.80, p.pct_acumulado.shift(fill_value=0) < 0.95], ["A", "B"], default="C")
    p.insert(0, "ranking", range(1, len(p) + 1))
    return p


# ======================================================================================
# 8. Conciliación de dotación (V-15)
# ======================================================================================
def conciliacion(d, dfs_orig, P, log: Bitacora) -> dict:
    c = d["colaboradores"]
    ini = pd.Timestamp(P["per_ini"] + "-01")
    hc_ini = int(((c.fecha_ingreso < ini) & (c.fecha_salida.isna() | (c.fecha_salida >= ini))).sum())
    hc_fin = int(((c.fecha_ingreso <= P["corte"]) & (c.fecha_salida.isna() | (c.fecha_salida >= P["corte"]))).sum())
    mv = d["movimientos"]
    ing = int((mv.tipo_movimiento == "INGRESO").sum())
    sal = int((mv.tipo_movimiento == "SALIDA").sum())
    esperado = hc_ini + ing - sal
    ok = esperado == hc_fin
    log.add("V-15", "OK" if ok else "ERROR", ARCHIVOS["movimientos"], "Dotación total",
            f"Inicial {hc_ini} + ingresos {ing} − salidas {sal} = {esperado}; dotación a la fecha de corte {hc_fin}",
            "Conciliado" if ok else "Revisar movimientos")
    return {"dotacion_inicial": hc_ini, "ingresos": ing, "salidas": sal, "dotacion_esperada": esperado, "dotacion_corte": hc_fin, "conciliado": ok}


# ======================================================================================
# 9. Reporte Markdown
# ======================================================================================
def md_tabla(df: pd.DataFrame, fmt: dict | None = None) -> str:
    fmt = fmt or {}
    cab = "| " + " | ".join(df.columns) + " |\n|" + "|".join("---" for _ in df.columns) + "|\n"
    filas = []
    for _, r in df.iterrows():
        vals = []
        for ccol in df.columns:
            v = r[ccol]
            if ccol in fmt and pd.notna(v):
                vals.append(fmt[ccol].format(v))
            elif isinstance(v, float):
                vals.append(f"{v:,.1f}")
            else:
                vals.append(str(v))
        filas.append("| " + " | ".join(vals) + " |")
    return cab + "\n".join(filas) + "\n"


def reporte_md(res, ger, uni, red, rep, esc_res, val, conc, P, H_PROD, ruta: Path, prod=None, est=None, disp_=None, par=None):
    pct = "{:.0%}"
    f1 = "{:,.1f}"
    tot = ger[["fte_contractual_corte", "fte_disponible", "fte_requerido", "brecha_fte", "fte_requerido_dotacion", "brecha_dotacion_fte", "horas_extra"]].sum()
    util_tot = ger.horas_carga.sum() / ger.horas_disponibles.sum()
    L = []
    L.append("# CAPACITY-ANALIZE — Resumen de resultados (DATOS FICTICIOS)\n")
    L.append("> Banco Volcán Azul S.A. es una entidad **ficticia**. Las fórmulas son **propuestas metodológicas** pendientes de aprobación; "
             "ningún valor de este reporte constituye una decisión.\n")
    L.append(f"**Período base:** {P['per_ini']} a {P['per_fin']} · **Fecha de corte de dotación:** {P['corte'].date()} · "
             f"**Horas productivas de 1 FTE en el período:** {H_PROD:,.0f} h · **Factor no productivo (PAR-002):** {P['f_np']:.0%}\n")
    L.append("## 1. Indicadores globales del piloto\n")
    L.append(md_tabla(pd.DataFrame([{
        "Dotación a la fecha de corte": f'{int(conc["dotacion_corte"])}',
        "FTE contractual (corte)": tot.fte_contractual_corte,
        "FTE disponible efectivo": tot.fte_disponible,
        "FTE requerido": tot.fte_requerido,
        "Brecha efectiva (disp − req)": tot.brecha_fte,
        "Utilización": util_tot,
        "Horas extra en el período": tot.horas_extra,
    }]), {"Utilización": pct}))
    L.append("\n*Brecha efectiva* compara FTE disponible con FTE requerido (ambos ya netos de ausencias). "
             "*Brecha de dotación* compara FTE contractual con FTE requerido ajustado por indisponibilidad. "
             "Son dos lecturas del mismo fenómeno: **no deben sumarse**.\n")
    L.append("## 2. Por gerencia\n")
    g = ger[["gerencia_id", "fte_contractual_corte", "fte_disponible", "fte_requerido", "brecha_fte", "utilizacion", "estado"]]
    L.append(md_tabla(g, {"utilizacion": pct}))
    L.append("## 3. Unidades y cargos en sobrecarga (utilización anual > umbral PAR-004)\n")
    L.append(f"Grupos con menos de {P['agreg_min']} personas (PAR-006) se marcan con agregacion = N: en producción se mostrarían agregados al nivel superior.\n")
    s = res[res.estado == "Sobrecarga"].sort_values("utilizacion", ascending=False).rename(columns={"cumple_agregacion_minima": "agregacion"})
    L.append(md_tabla(s[["nombre_unidad", "nombre_cargo", "agregacion", "dotacion_corte", "fte_disponible", "fte_requerido", "brecha_fte", "utilizacion", "meses_sobrecarga", "horas_extra"]],
                      {"utilizacion": pct, "dotacion_corte": "{:.0f}", "meses_sobrecarga": "{:.0f}", "horas_extra": "{:,.0f}"}) if not s.empty else "Ninguna.\n")
    L.append("## 4. Unidades y cargos con holgura (utilización anual < umbral PAR-005)\n")
    h = res[res.estado == "Holgura"].sort_values("utilizacion").rename(columns={"cumple_agregacion_minima": "agregacion"})
    L.append(md_tabla(h[["nombre_unidad", "nombre_cargo", "agregacion", "dotacion_corte", "fte_disponible", "fte_requerido", "brecha_fte", "utilizacion"]],
                      {"utilizacion": pct, "dotacion_corte": "{:.0f}"}) if not h.empty else "Ninguna.\n")
    L.append("## 5. Oportunidades de redistribución (a evaluar)\n")
    L.append(md_tabla(red[["cargo_id", "unidad_origen", "unidad_destino", "misma_provincia", "fte_movible", "utilizacion_origen", "utilizacion_destino"]],
                      {"utilizacion_origen": pct, "utilizacion_destino": pct}) if not red.empty else "No se identificaron emparejamientos.\n")
    L.append("## 6. Reprocesos: horas potencialmente liberables (top 10)\n")
    L.append(md_tabla(rep.head(10)[["nombre_proceso", "causa_principal", "cantidad_reprocesos", "horas_reproceso", "fte_potencialmente_liberable"]],
                      {"cantidad_reprocesos": "{:,.0f}", "horas_reproceso": "{:,.0f}", "fte_potencialmente_liberable": "{:.2f}"}))
    L.append(f"\nTotal: **{rep.horas_reproceso.sum():,.0f} h** ≈ **{rep.fte_potencialmente_liberable.sum():.1f} FTE** si se eliminaran todos los reprocesos.\n")
    L.append("## 7. Escenarios 2027 (FTE requerido para dotación vs. FTE contractual actual)\n")
    L.append(md_tabla(esc_res, {"fte_requerido": f1, "fte_requerido_dotacion": f1, "fte_contractual_corte": f1, "brecha_dotacion_fte": "{:+,.1f}"}))
    L.append("\nBrecha de dotación positiva = exceso de FTE; negativa = faltante.\n")
    if est is not None:
        L.append("## 8. Indicadores complementarios (IND-17 a IND-20)\n")
        L.append("### IND-18 · Meses pico por proceso (índice estacional > 1,10)\n")
        pk = est[est.pico == "S"]
        L.append(md_tabla(pk[["nombre_proceso", "periodo", "indice_estacional"]], {"indice_estacional": "{:.2f}"}) if not pk.empty else "Sin picos.\n")
        L.append("### IND-19 · Dispersión de la utilización entre unidades del mismo cargo\n")
        L.append(md_tabla(disp_[["gerencia_id", "nombre_cargo", "unidades", "utilizacion_min", "utilizacion_max", "coef_variacion", "carga_desigual"]],
                          {"unidades": "{:.0f}", "utilizacion_min": pct, "utilizacion_max": pct, "coef_variacion": "{:.2f}"}))
        L.append("### IND-20 · Pareto de causas de reproceso (clase A = ~80 % de las horas)\n")
        pa = par[par.clase == "A"]
        L.append(md_tabla(pa[["ranking", "nombre_proceso", "causa_principal", "horas_reproceso", "pct_acumulado"]],
                          {"ranking": "{:.0f}", "horas_reproceso": "{:,.0f}", "pct_acumulado": pct}))
        L.append(f"\n{len(pa)} de {len(par)} combinaciones proceso-causa explican el {pa.pct.sum():.0%} de las horas de reproceso.\n")
        L.append("### IND-17 · Productividad por FTE: mayores diferencias entre unidades (actividad con ≥ 5 unidades)\n")
        pr = prod[(prod.comparables >= 5) & (prod.cumple_agregacion_minima == "S")]
        ext = pd.concat([pr.nsmallest(5, "indice_vs_mediana_actividad"), pr.nlargest(5, "indice_vs_mediana_actividad")])
        L.append(md_tabla(ext[["nombre_actividad", "unidad_id", "productividad_mensual_por_fte", "indice_vs_mediana_actividad"]],
                          {"productividad_mensual_por_fte": "{:,.0f}", "indice_vs_mediana_actividad": "{:.2f}"}))
        L.append("\nLa productividad se compara solo dentro de la misma actividad y cargo. Un índice alejado de 1 es una señal para revisar, no una evaluación individual.\n")
    L.append("## 9. Calidad de datos\n")
    vv = val.groupby(["regla", "severidad"]).size().reset_index(name="registros")
    L.append(md_tabla(vv, {"registros": "{:.0f}"}))
    L.append(f"\nConciliación de dotación (V-15): inicial {conc['dotacion_inicial']} + ingresos {conc['ingresos']} − salidas {conc['salidas']} "
             f"= {conc['dotacion_esperada']} vs. corte {conc['dotacion_corte']} → **{'Conciliado' if conc['conciliado'] else 'NO conciliado'}**.\n")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text("\n".join(L), encoding="utf-8")


# ======================================================================================
# Main
# ======================================================================================
def ejecutar(dir_in: Path, dir_out: Path, dir_rep: Path) -> dict:
    dfs = cargar(dir_in)
    P = parametros(dfs)
    log = Bitacora()
    d = validar(dfs, P, log)
    disp = disponibilidad(d, P, log)
    cg = carga(d)
    cap = capacidad_mensual(disp, cg, d, P, log)
    res, H_NOM, H_PROD = resumen_anual(cap, d, P)
    uni = agregado(res, ["gerencia_id", "unidad_id", "nombre_unidad"], P)
    ger = agregado(res, ["gerencia_id"], P)
    act = carga_actividad(cg, d, H_PROD)
    rep = resumen_reprocesos(cg, d, H_PROD)
    red = redistribucion(res, d, P)
    esc = escenarios(cg, res, d, P, H_PROD)
    esc_res = esc.groupby(["escenario_id", "nombre_escenario"])[["fte_requerido", "fte_requerido_dotacion", "fte_contractual_corte", "brecha_dotacion_fte"]].sum().reset_index()
    conc = conciliacion(d, dfs, P, log)
    val = log.df()

    dir_out.mkdir(parents=True, exist_ok=True)
    r = lambda df: df.round(4)
    val.to_csv(dir_out / "00_reporte_validacion.csv", index=False)
    r(disp).to_csv(dir_out / "01_disponibilidad_colaborador_mes.csv", index=False)
    r(cg).to_csv(dir_out / "02_carga_actividad_unidad_mes.csv", index=False)
    r(cap).to_csv(dir_out / "03_capacidad_unidad_cargo_mes.csv", index=False)
    r(res).to_csv(dir_out / "04_resumen_anual_unidad_cargo.csv", index=False)
    r(uni).to_csv(dir_out / "05_resumen_anual_unidad.csv", index=False)
    r(ger).to_csv(dir_out / "06_resumen_anual_gerencia.csv", index=False)
    r(act).to_csv(dir_out / "07_carga_anual_por_actividad.csv", index=False)
    r(rep).to_csv(dir_out / "08_reprocesos_por_causa.csv", index=False)
    r(red).to_csv(dir_out / "09_oportunidades_redistribucion.csv", index=False)
    r(esc).to_csv(dir_out / "10_escenarios_2027_detalle.csv", index=False)
    r(esc_res).to_csv(dir_out / "11_escenarios_2027_resumen.csv", index=False)
    prod = productividad(cg, cap, res, d, P)
    est = estacionalidad(cg, d)
    dsp = dispersion(res, P)
    par = pareto_causas(rep)
    r(prod).to_csv(dir_out / "12_productividad_por_fte.csv", index=False)
    r(est).to_csv(dir_out / "13_indice_estacional.csv", index=False)
    r(dsp).to_csv(dir_out / "14_dispersion_utilizacion.csv", index=False)
    r(par).to_csv(dir_out / "15_pareto_causas_reproceso.csv", index=False)
    reporte_md(res, ger, uni, red, rep, esc_res, val, conc, P, H_PROD, dir_rep / "resumen_resultados.md", prod, est, dsp, par)
    return {"P": P, "d": d, "disp": disp, "carga": cg, "cap": cap, "res": res, "ger": ger, "esc": esc_res, "val": val, "conc": conc, "H_PROD": H_PROD,
            "prod": prod, "est": est, "dsp": dsp, "par": par}


def main():
    ap = argparse.ArgumentParser(description="CAPACITY-ANALIZE — motor demostrativo (datos ficticios)")
    ap.add_argument("--input", default=str(ROOT / "data" / "input"))
    ap.add_argument("--output", default=str(ROOT / "data" / "output"))
    ap.add_argument("--reportes", default=str(ROOT / "reports"))
    a = ap.parse_args()
    out = ejecutar(Path(a.input), Path(a.output), Path(a.reportes))
    v = out["val"]
    print("CAPACITY-ANALIZE — ejecución completada (datos ficticios)")
    print(f"  Validación: {(v.severidad == 'ERROR').sum()} errores, {(v.severidad == 'ADVERTENCIA').sum()} advertencias")
    print(f"  Conciliación de dotación: {'OK' if out['conc']['conciliado'] else 'NO CONCILIA'} (dotación corte {out['conc']['dotacion_corte']})")
    g = out["ger"]
    print(f"  FTE disponible {g.fte_disponible.sum():.1f} | FTE requerido {g.fte_requerido.sum():.1f} | Brecha {g.brecha_fte.sum():+.1f}")
    print(f"  Resultados en {a.output} y {a.reportes}/resumen_resultados.md")


if __name__ == "__main__":
    main()
