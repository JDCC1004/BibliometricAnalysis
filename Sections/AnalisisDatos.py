import streamlit as st
import os

def mostrar():
    carpetaGraficas = os.path.join("Graphics", "Frecuency")
    imagenes = [img for img in os.listdir(carpetaGraficas) if img.endswith(".png")]

    st.title("Visualización de Imágenes")

    for imagen in imagenes:
        rutaImagen = os.path.join(carpetaGraficas, imagen)
        st.image(rutaImagen, caption=imagen, use_container_width=True)