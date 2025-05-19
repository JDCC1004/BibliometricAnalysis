import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Análisis Bibliométrico", layout="wide")

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", [
    "Inicio",
    "Análisis",
    "Gráficos de Frecuencia",
    "Gráficos de Co-ocurrencia",
    "Dendogramas",
    "Nube de Palabras",
    "Acerca de"
])

if opcion == "Inicio":
    from Sections import VistaGeneral
    VistaGeneral.mostrar()

elif opcion == "Análisis":
    from Sections import Analisis
    Analisis.mostrar()

elif opcion == "Gráficos de Frecuencia":
    from Sections import GraficoFrecuencia
    GraficoFrecuencia.mostrar()

elif opcion == "Gráficos de Co-ocurrencia":
    from Sections import Coocurrencia
    Coocurrencia.mostrar()

elif opcion == "Dendogramas":
    from Sections import Dendogramas
    Dendogramas.mostrar()

elif opcion == "Nube de Palabras":
    from Sections import NubePalabras
    NubePalabras.mostrar()

elif opcion == "Acerca de":
    from Sections import AcercaDe
    AcercaDe.mostrar()