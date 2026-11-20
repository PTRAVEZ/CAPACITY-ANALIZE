"""Pruebas del validador de carga de la Fase 1 (usa los datos ficticios del demostrador)."""
import shutil
import sys
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import load_workbook

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parent
DEMO = REPO / "DATOS" / "BANCO-VOLCAN-AZUL" / "data" / "input"
sys.path.insert(0, str(BASE / "scripts"))
import generar_plantillas  # noqa: E402
import validar_carga as vc  # noqa: E402


def correr(tmp_path, **kw):
    salida = tmp_path / "reporte.csv"
    args = []
    for k, v in kw.items():
        args += [f"--{k}", str(v)]
    codigo = vc.main(args + ["--salida", str(salida)])
    return codigo, pd.read_csv(salida)


def copia_demo(tmp_path):
    d = tmp_path / "carga"
    shutil.copytree(DEMO, d)
    return d


def test_demo_detecta_duplicado_y_negativo(tmp_path):
    codigo, rep = correr(tmp_path, dir=DEMO)
    assert codigo == 1
    assert {"S-09", "S-07"} <= set(rep.regla)
    assert (rep.regla == "V-00").any()  # reglas omitidas por errores de esquema


def test_carga_limpia_pasa_esquema_y_ejecuta_reglas(tmp_path):
    d = copia_demo(tmp_path)
    v = pd.read_csv(d / "08_volumenes_mensuales.csv", dtype=str)
    v = v[pd.to_numeric(v.volumen) >= 0].drop_duplicates(["periodo", "unidad_id", "actividad_id"])
    v.to_csv(d / "08_volumenes_mensuales.csv", index=False)
    codigo, rep = correr(tmp_path, dir=d)
    assert (rep[rep.etapa == "Esquema"].severidad == "ERROR").sum() == 0
    reglas = set(rep[rep.etapa == "Reglas"].regla)
    assert {"V-02", "V-04", "V-08", "V-11", "V-15"} <= reglas


def test_privacidad(tmp_path):
    d = copia_demo(tmp_path)
    c = pd.read_csv(d / "03_colaboradores.csv", dtype=str, keep_default_na=False)
    c.loc[0, "colaborador_id"] = "1712345678"
    c["cedula"] = "x"
    c.to_csv(d / "03_colaboradores.csv", index=False)
    _, rep = correr(tmp_path, dir=d)
    assert {"S-04", "S-10"} <= set(rep.regla)


def test_fuente_y_columna_faltantes(tmp_path):
    d = copia_demo(tmp_path)
    (d / "13_vacantes.csv").unlink()
    a = pd.read_csv(d / "07_actividades.csv", dtype=str).drop(columns=["metodo_medicion"])
    a.to_csv(d / "07_actividades.csv", index=False)
    _, rep = correr(tmp_path, dir=d)
    assert {"S-01", "S-02"} <= set(rep.regla)


def test_plantilla_excel_ida_y_vuelta(tmp_path, monkeypatch):
    monkeypatch.setattr(generar_plantillas, "OUT", tmp_path)
    ruta = generar_plantillas.plantilla_fuentes()
    wb = load_workbook(ruta)
    for arch in ["01_estructura_organizacional.csv", "02_cargos.csv"]:
        ws = wb[arch.replace(".csv", "")]
        df = pd.read_csv(DEMO / arch, dtype=str, keep_default_na=False)
        for i, fila in enumerate(df.itertuples(index=False), start=2):
            for j, v in enumerate(fila, start=1):
                ws.cell(i, j, v)
    wb.save(ruta)
    _, rep = correr(tmp_path, excel=ruta)
    esq = rep[rep.etapa == "Esquema"]
    assert not ((esq.archivo == "01_estructura_organizacional.csv") & (esq.severidad == "ERROR")).any()
    assert not ((esq.archivo == "02_cargos.csv") & (esq.severidad == "ERROR")).any()
    assert ((esq.regla == "S-11") | (esq.regla == "S-01")).any()  # las demás hojas solo tienen el ejemplo
