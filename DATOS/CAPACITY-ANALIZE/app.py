import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "input"

st.set_page_config(page_title="CAPACITY-ANALIZE", layout="wide")
st.title("CAPACITY-ANALIZE")
st.caption("Prototipo de análisis de capacidad humana — datos 100% ficticios")

@st.cache_data
def load_csv(name):
    path = INPUT / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

employees = load_csv("dim_colaboradores.csv")
volumes = load_csv("fact_volumenes_mensuales.csv")
activities = load_csv("dim_actividades.csv")
departments = load_csv("dim_departamentos.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Colaboradores simulados", f"{len(employees):,}")
c2.metric("Registros mensuales de volumen", f"{len(volumes):,}")
c3.metric("Actividades catalogadas", f"{len(activities):,}")

st.warning("Entorno demostrativo: no utilizar estas cifras para decisiones reales.")
st.subheader("Volúmenes mensuales simulados")
if not volumes.empty:
    summary = volumes.groupby("periodo", as_index=False)["volumen_recibido"].sum()
    st.line_chart(summary.set_index("periodo"))
    st.dataframe(summary, use_container_width=True)
st.subheader("Estructura departamental")
st.dataframe(departments, use_container_width=True)
st.info("La interfaz es un punto de partida. La lógica completa debe desarrollarse por fases con el prompt maestro.")
