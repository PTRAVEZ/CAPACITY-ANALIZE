"""Pruebas de la simulación de la Fase 1 (datos ficticios)."""
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]
RES = BASE / "resultados"


@pytest.fixture(scope="module", autouse=True)
def simulacion():
    p = subprocess.run([sys.executable, str(BASE / "scripts" / "simular_fase1.py")], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def val(nombre):
    return pd.read_csv(RES / f"validacion_{nombre}.csv")


def test_ronda1_rechaza_datos_personales_y_esquema():
    r = val("ronda1")
    assert {"S-01", "S-04", "S-06", "S-07", "S-08", "S-09"} <= set(r[r.severidad == "ERROR"].regla)


def test_ronda2_solo_errores_de_reglas():
    r = val("ronda2")
    err = r[r.severidad == "ERROR"]
    assert set(err.etapa) == {"Reglas"} and set(err.regla) == {"V-02", "V-04", "V-08"}


def test_carga_final_apta():
    for n in ("ronda3", "final"):
        assert (val(n).severidad == "ERROR").sum() == 0


def test_estudio_tiempos_suficiente_y_aplicado():
    est = pd.read_csv(RES / "estudio_tiempos_resultado.csv")
    assert (est.observaciones >= 30).all()
    act = pd.read_csv(BASE / "trabajo" / "carga_final" / "07_actividades.csv").set_index("actividad_id")
    for r in est.itertuples():
        assert act.loc[r.actividad_id, "tiempo_estandar_min"] == pytest.approx(r.estandar_nuevo)
        assert act.loc[r.actividad_id, "metodo_medicion"] == "Estudio de tiempos"


def test_privacidad_en_resultados():
    obs = pd.read_csv(RES / "estudio_tiempos_observaciones.csv")
    assert obs.colaborador_id.str.fullmatch(r"COL-\d{4}").all()
    jef = pd.read_csv(RES / "validacion_jefaturas.csv")
    assert (jef.dotacion_corte >= 3).all()


def test_documentos_generados():
    for n in ("03_BITACORA_CARGA_DATOS", "04_ESTUDIO_TIEMPOS", "05_INFORME_MENSUAL_01",
              "06_VALIDACION_JEFATURAS", "07_COMITE_SESION_02", "08_CIERRE_FASE1"):
        t = (BASE / f"{n}.md").read_text(encoding="utf-8")
        assert "Simulación con datos ficticios" in t
