"""Pruebas de consistencia del motor demostrativo (criterios de aceptación CA-01 … CA-06)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import capacity_analize as ca  # noqa: E402


@pytest.fixture(scope="module")
def out(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("salida")
    return ca.ejecutar(ROOT / "data" / "input", tmp / "output", tmp / "reports")


def test_ca01_carga_reproducible_desde_insumos(out):
    """La carga total es igual a Σ volumen × tiempo estándar + Σ reprocesos × tiempo de reproceso (insumos válidos)."""
    d = out["d"]
    v = d["volumenes"].merge(d["actividades"], on="actividad_id")
    esperado = (v.volumen * v.tiempo_estandar_min / 60).sum()
    r = d["reprocesos"].merge(d["actividades"], on="actividad_id")
    esperado += (r.cantidad_reprocesos * r.tiempo_reproceso_min / 60).sum()
    assert out["cap"].horas_carga.sum() == pytest.approx(esperado, rel=1e-9)


def test_ca02_conciliacion_dotacion(out):
    assert out["conc"]["conciliado"]


def test_ca03_sin_doble_conteo_de_ausencias(out):
    """FTE disponible = FTE contractual × (1 − tasa de indisponibilidad): las ausencias se descuentan una sola vez."""
    c = out["cap"]
    c = c[c.horas_nominales > 0]
    tasa = (c.horas_ausencias + c.horas_capacitacion) / c.horas_nominales
    assert np.allclose(c.fte_disponible, c.fte_contractual * (1 - tasa), atol=1e-9)


def test_ca04_horas_no_superan_nominales(out):
    disp = out["disp"]
    assert (disp.horas_ausencias + disp.horas_capacitacion <= disp.horas_nominales + 1e-6).all()
    assert (disp.horas_disponibles >= -1e-9).all()


def test_ca05_anomalias_sembradas_detectadas(out):
    v = out["val"]
    for regla in ["V-02", "V-04", "V-07", "V-08", "V-09", "V-10", "V-11"]:
        assert (v.regla == regla).any(), f"No se detectó la anomalía de la regla {regla}"


def test_ca06_brecha_coherente(out):
    c = out["cap"]
    assert np.allclose(c.brecha_fte, c.fte_disponible - c.fte_requerido)
    g = out["ger"]
    assert g.fte_requerido.sum() == pytest.approx(out["res"].fte_requerido.sum())


def test_ind17_productividad_mediana(out):
    """IND-17: en cada actividad, el índice frente a la mediana tiene mediana 1."""
    p = out["prod"]
    med = p.groupby("actividad_id").indice_vs_mediana_actividad.median()
    assert np.allclose(med, 1.0)


def test_ind18_indice_estacional_promedio_uno(out):
    e = out["est"]
    assert np.allclose(e.groupby("proceso_id").indice_estacional.mean(), 1.0)
    assert set(e[e.pico == "S"].periodo.str[5:]) & {"12", "08", "04"}, "Deben aparecer los picos de diciembre, agosto o abril"


def test_ind19_dispersion_minimo_tres_unidades(out):
    assert (out["dsp"].unidades >= 3).all()


def test_ind20_pareto_acumulado(out):
    p = out["par"]
    assert p.pct_acumulado.iloc[-1] == pytest.approx(1.0)
    assert p.horas_reproceso.is_monotonic_decreasing
    assert (p.clase == "A").any()
