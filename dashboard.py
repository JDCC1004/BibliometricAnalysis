import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Análisis Bibliométrico", layout="wide")

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", [
    "Inicio",
    "Análisis",
    "Gráficos",
    "Acerca de"
])

if opcion == "Inicio":
    from Sections import VistaGeneral
    VistaGeneral.mostrar()

elif opcion == "Análisis":
    from Sections import AnalisisDatos
    AnalisisDatos.mostrar()

elif opcion == "Gráficos":
    from Sections import VisualizacionDatos
    VisualizacionDatos.mostrar()

elif opcion == "Acerca de":
    from Sections import AcercaDe
    AcercaDe.mostrar()