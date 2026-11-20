#!/usr/bin/env python3
"""
Validador de carga de CAPACITY-ANALIZE (Fase 1).

Revisa una carga de fuentes REALES antes del cálculo, en dos etapas:
  1. Esquema (S-01 a S-11): archivos, columnas, tipos, rangos, listas, llaves y privacidad.
  2. Reglas de negocio (V-01 a V-16): reutiliza el motor de DATOS/BANCO-VOLCAN-AZUL/src.
     Solo se ejecuta si la etapa 1 no tiene errores.

Uso:
  python FASE1_ARRANQUE/scripts/validar_carga.py --dir  carpeta_con_14_csv
  python FASE1_ARRANQUE/scripts/validar_carga.py --excel PLANTILLA_CARGA_FUENTES_lleno.xlsx [--exportar carpeta_csv]

Salida: reporte CSV (por defecto FASE1_ARRANQUE/salidas/reporte_validacion_carga.csv).
Código de salida 0 = sin errores; 1 = hay errores que impiden calcular.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import pandas as pd

from esquema_fuentes import COLUMNAS_PROHIBIDAS, ENUMS, FUENTES

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parent
MOTOR = REPO / "DATOS" / "BANCO-VOLCAN-AZUL" / "src"
MAX_DETALLE = 20  # filas detalladas por regla y archivo


class Reporte:
    def __init__(self):
        self.filas = []

    def add(self, etapa, regla, severidad, archivo, registro, detalle):
        self.filas.append({"etapa": etapa, "regla": regla, "severidad": severidad, "archivo": archivo,
                           "registro": registro, "detalle": detalle})

    def errores(self, etapa=None):
        return sum(1 for f in self.filas if f["severidad"] == "ERROR" and (etapa is None or f["etapa"] == etapa))

    def df(self):
        return pd.DataFrame(self.filas, columns=["etapa", "regla", "severidad", "archivo", "registro", "detalle"])


def leer(dir_csv: Path | None, excel: Path | None, rep: Reporte) -> dict[str, pd.DataFrame | None]:
    datos = {}
    hojas = pd.read_excel(excel, sheet_name=None, dtype=str) if excel else {}
    for arch, meta in FUENTES.items():
        df = None
        if dir_csv:
            ruta = dir_csv / arch
            if ruta.exists():
                df = pd.read_csv(ruta, dtype=str, keep_default_na=False)
        else:
            hoja = arch.replace(".csv", "")[:31]
            if hoja in hojas:
                df = hojas[hoja].fillna("").astype(str)
                df = df[~(df.apply(lambda r: "".join(r).strip(), axis=1) == "")]
                ejemplo = [c["ejemplo"] for c in meta["columnas"]]
                if len(df) and list(df.iloc[0].reindex([c["nombre"] for c in meta["columnas"]]).fillna("")) == ejemplo:
                    df = df.iloc[1:]
                    rep.add("Esquema", "S-11", "ADVERTENCIA", arch, "fila 2", "Se ignoró la fila de EJEMPLO de la plantilla")
        if df is None:
            rep.add("Esquema", "S-01", "ERROR", arch, "-", "Fuente faltante")
        else:
            df.columns = [str(c).strip() for c in df.columns]
            df = df.apply(lambda s: s.str.strip())
        datos[arch] = df
    return datos


def es_fecha(s):
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s)) and not pd.isna(pd.to_datetime(s, errors="coerce", format="%Y-%m-%d"))


def es_periodo(s):
    return bool(re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", s))


def num(s):
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def validar_esquema(datos, rep: Reporte):
    for arch, df in datos.items():
        if df is None:
            continue
        meta = FUENTES[arch]
        esperadas = [c["nombre"] for c in meta["columnas"]]
        if df.empty:
            rep.add("Esquema", "S-11", "ADVERTENCIA", arch, "-", "La fuente no tiene filas")
        for col in df.columns:
            if col.lower() in COLUMNAS_PROHIBIDAS:
                rep.add("Esquema", "S-04", "ERROR", arch, col, "Columna con dato personal prohibido (DEC-025/026). Elimínela.")
            elif col not in esperadas:
                rep.add("Esquema", "S-03", "ADVERTENCIA", arch, col, "Columna no esperada; será ignorada")
        for spec in meta["columnas"]:
            n = spec["nombre"]
            if n not in df.columns:
                rep.add("Esquema", "S-02", "ERROR", arch, n, "Columna faltante")
                continue
            conteo = {}
            for i, v in df[n].items():
                fila = f"fila {i + 2}"
                regla = None
                if v == "":
                    if spec["requerido"]:
                        regla, msg = "S-05", "Valor requerido vacío"
                elif spec["tipo"] == "fecha" and not es_fecha(v):
                    regla, msg = "S-06", f"Fecha inválida '{v}' (use AAAA-MM-DD)"
                elif spec["tipo"] == "periodo" and not es_periodo(v):
                    regla, msg = "S-06", f"Período inválido '{v}' (use AAAA-MM)"
                elif spec["tipo"] == "sn" and v not in ("S", "N"):
                    regla, msg = "S-06", f"Valor '{v}' no es S/N"
                elif spec["tipo"] in ("entero", "decimal"):
                    x = num(v)
                    if x is None or (spec["tipo"] == "entero" and x != int(x)):
                        regla, msg = "S-06", f"'{v}' no es un número {spec['tipo']}"
                    elif (spec["min"] is not None and x < spec["min"]) or (spec["max"] is not None and x > spec["max"]):
                        regla, msg = "S-07", f"{v} fuera de rango [{spec['min']}, {spec['max']}]"
                elif spec["tipo"] == "lista" and v not in ENUMS[spec["lista"]]:
                    regla, msg = "S-08", f"'{v}' no permitido. Valores: {', '.join(ENUMS[spec['lista']])}"
                if n == "colaborador_id" and v and (re.fullmatch(r"\d{10}", v) or "@" in v or " " in v):
                    regla, msg = "S-10", "Parece cédula, correo o nombre: use un seudónimo (DEC-025)"
                if regla:
                    conteo[regla] = conteo.get(regla, 0) + 1
                    if conteo[regla] <= MAX_DETALLE:
                        rep.add("Esquema", regla, "ERROR", arch, f"{fila} · {n}", msg)
            for regla, k in conteo.items():
                if k > MAX_DETALLE:
                    rep.add("Esquema", regla, "ERROR", arch, n, f"... y {k - MAX_DETALLE} filas más con el mismo problema")
        llave = [k for k in meta["llave"] if k in df.columns]
        if len(llave) == len(meta["llave"]) and not df.empty:
            dup = df[df.duplicated(llave, keep=False)]
            if len(dup):
                ejemplo = " | ".join(dup.iloc[0][llave])
                rep.add("Esquema", "S-09", "ERROR", arch, ejemplo, f"{len(dup)} filas con llave duplicada ({' + '.join(llave)})")


def validar_reglas(datos, rep: Reporte, exportar: Path | None):
    sys.path.insert(0, str(MOTOR))
    try:
        import capacity_analize as ca
    except Exception as e:  # pragma: no cover
        rep.add("Reglas", "V-00", "ERROR", "motor", "-", f"No se pudo cargar el motor: {e}")
        return
    with tempfile.TemporaryDirectory() as tmp:
        destino = exportar or Path(tmp)
        destino.mkdir(parents=True, exist_ok=True)
        for arch, df in datos.items():
            cols = [c["nombre"] for c in FUENTES[arch]["columnas"]]
            df[cols].to_csv(destino / arch, index=False)
        try:
            dfs = ca.cargar(destino)
            P = ca.parametros(dfs)
            log = ca.Bitacora()
            d = ca.validar(dfs, P, log)
            disp = ca.disponibilidad(d, P, log)
            ca.capacidad_mensual(disp, ca.carga(d), d, P, log)
            ca.conciliacion(d, dfs, P, log)
        except Exception as e:
            rep.add("Reglas", "V-00", "ERROR", "motor", "-", f"Las reglas no pudieron ejecutarse: {type(e).__name__}: {e}")
            return
        vistos = set()
        for f in log.filas:
            clave = (f["regla"], f["archivo"], f["registro"])
            if clave in vistos:
                continue
            vistos.add(clave)
            rep.add("Reglas", f["regla"], f["severidad"], f["archivo"], f["registro"], f"{f['detalle']} → {f['accion']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Valida una carga de fuentes de CAPACITY-ANALIZE")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir", type=Path, help="Carpeta con los 14 CSV")
    g.add_argument("--excel", type=Path, help="Plantilla Excel completada")
    ap.add_argument("--exportar", type=Path, help="Carpeta donde guardar los CSV normalizados (útil con --excel)")
    ap.add_argument("--salida", type=Path, default=BASE / "salidas" / "reporte_validacion_carga.csv")
    a = ap.parse_args(argv)

    rep = Reporte()
    datos = leer(a.dir, a.excel, rep)
    validar_esquema(datos, rep)
    if rep.errores("Esquema") == 0:
        validar_reglas(datos, rep, a.exportar)
    else:
        rep.add("Reglas", "V-00", "OMITIDO", "-", "-", "Corrija primero los errores de esquema")

    a.salida.parent.mkdir(parents=True, exist_ok=True)
    df = rep.df()
    df.to_csv(a.salida, index=False)
    print("CAPACITY-ANALIZE · Validación de carga")
    for etapa in ("Esquema", "Reglas"):
        sub = df[df.etapa == etapa]
        print(f"  {etapa:<8} errores: {(sub.severidad == 'ERROR').sum():>4} | advertencias: {(sub.severidad == 'ADVERTENCIA').sum():>4}")
    resultado = "APTA para calcular" if rep.errores() == 0 else "NO APTA: corrija los errores"
    print(f"  Resultado: {resultado}")
    print(f"  Reporte: {a.salida}")
    return 0 if rep.errores() == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
