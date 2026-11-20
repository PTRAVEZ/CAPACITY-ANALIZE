import pandas as pd
import pytest
from src.calculations import standard_time_minutes, effective_hours_per_fte, fte_required, fte_gap

def test_standard_time_uses_median():
    df = pd.DataFrame({
        "id_actividad": ["ACT1", "ACT1", "ACT1"],
        "nivel_complejidad": ["Media"] * 3,
        "tiempo_observado_min": [5.0, 7.0, 100.0],
        "muestra_valida": [1, 1, 1],
    })
    result = standard_time_minutes(df)
    assert result.loc[0, "tiempo_estandar_min"] == 7.0

def test_effective_hours():
    row = {"horas_contractuales_mes": 160, "horas_vacaciones_promedio": 5,
           "horas_ausentismo_promedio": 3, "horas_capacitacion": 2,
           "horas_reuniones": 4, "horas_pausas_no_productivas": 6}
    assert effective_hours_per_fte(row) == 140

def test_fte_required_and_gap():
    assert fte_required(700, 140) == 5
    assert fte_gap(5, 4) == 1

def test_zero_effective_hours_rejected():
    with pytest.raises(ValueError):
        fte_required(100, 0)
