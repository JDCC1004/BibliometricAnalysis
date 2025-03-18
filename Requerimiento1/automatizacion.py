import os
import shutil
from playwright.sync_api import sync_playwright
import time
import Requerimiento1.extraccion_Sage as RS
import Requerimiento1.extraccion_IEEE as RSIEEE
import Requerimiento1.extraccion_sd as RSSD

def initialize_browser():
    playwright = sync_playwright().start()
    navegador = playwright.chromium.launch(headless=False)  # Cambia a True para headless
    context = navegador.new_context(
        accept_downloads=True,
    )
    pagina = context.new_page()
    pagina.goto("https://library.uniquindio.edu.co/databases")
    pagina.wait_for_load_state("domcontentloaded")

    return playwright, navegador, pagina

def eliminar_archivos(download_directory):
    if os.path.exists(download_directory):
        for archivo in os.listdir(download_directory):
            archivo_path = os.path.join(download_directory, archivo)
            try:
                if os.path.isfile(archivo_path):
                    os.remove(archivo_path)  # Borra archivos
                elif os.path.isdir(archivo_path):
                    shutil.rmtree(archivo_path)  # Borra subcarpetas
            except Exception as e:
                print(f"No se pudo borrar {archivo_path}: {e}")
    else:
        os.makedirs(download_directory)

def iniciar_sesion(pagina):
    # Iniciar sesión con correo institucional
    pagina.locator("a#btn-google").click()
    pagina.wait_for_load_state("domcontentloaded")
    pagina.fill("#identifierId", "pepitoperez@uqvirtual.edu.co")  # Modificar
    pagina.click("button:has-text('Siguiente')")
    pagina.wait_for_load_state("domcontentloaded")
    pagina.fill("input[name='Passwd']", "UnaContraseñaMuySegura123") # Modificar
    pagina.click("button:has-text('Siguiente')")
    time.sleep(2)
    pagina.wait_for_load_state("domcontentloaded")


def descargar_citas():
    # Inicialización del navegador
    playwright, navegador, pagina = initialize_browser()

    # Eliminar archivos de la carpeta Datos
    eliminar_archivos(os.path.join(os.getcwd(), "Datos"))

    #Extraccion de citas de las bases de datos
    RS.extraer_sage(playwright, navegador, pagina)
    RSIEEE.extraer_ieee(playwright, navegador, pagina)
    RSSD.extraer_sd(playwright, navegador, pagina)
