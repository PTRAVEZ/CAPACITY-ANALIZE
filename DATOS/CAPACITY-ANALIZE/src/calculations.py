"""Motor inicial de fórmulas de capacidad humana."""
import pandas as pd

def standard_time_minutes(observations: pd.DataFrame) -> pd.DataFrame:
    required = {"id_actividad", "nivel_complejidad", "tiempo_observado_min", "muestra_valida"}
    missing = required - set(observations.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    valid = observations.loc[
        (observations["muestra_valida"] == 1) &
        (observations["tiempo_observado_min"] > 0)
    ]
    return (valid.groupby(["id_actividad", "nivel_complejidad"], as_index=False)
            .agg(tiempo_estandar_min=("tiempo_observado_min", "median"),
                 numero_observaciones=("tiempo_observado_min", "count")))

def workload_hours(volumes: pd.DataFrame, standard_times: pd.DataFrame,
                   volume_column: str = "volumen_procesado") -> pd.DataFrame:
    keys = ["id_actividad", "nivel_complejidad"]
    if not set(keys + [volume_column, "periodo"]).issubset(volumes.columns):
        raise ValueError("El archivo de volúmenes debe incluir periodo, actividad, complejidad y volumen.")
    merged = volumes.merge(standard_times, on=keys, how="left", validate="many_to_one")
    if merged["tiempo_estandar_min"].isna().any():
        raise ValueError("Existen actividades/complejidades sin tiempo estándar.")
    merged["carga_horas"] = merged[volume_column] * merged["tiempo_estandar_min"] / 60
    return merged

def effective_hours_per_fte(row) -> float:
    deductions = ["horas_vacaciones_promedio", "horas_ausentismo_promedio",
                  "horas_capacitacion", "horas_reuniones", "horas_pausas_no_productivas"]
    result = float(row["horas_contractuales_mes"]) - sum(float(row[c]) for c in deductions)
    if result <= 0:
        raise ValueError("Las horas efectivas por FTE deben ser mayores que cero.")
    return result

def fte_required(workload_hours_value: float, effective_hours: float) -> float:
    if effective_hours <= 0:
        raise ValueError("Las horas efectivas deben ser mayores que cero.")
    return float(workload_hours_value) / float(effective_hours)

def fte_gap(required: float, available: float) -> float:
    return float(required) - float(available)
