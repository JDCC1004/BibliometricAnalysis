import os
import time

from Automation import automatizacion


def safe_click(pagina, selector):
    element = pagina.wait_for_selector(selector, state="attached")
    #element.scroll_into_view_if_needed()
    element.wait_for_element_state("visible")
    element.wait_for_element_state("enabled")
    element.click()



def extraer_ieee (playwright, navegador, pagina):
    # Crear una nueva pestaña en el navegador
    contexto = pagina.context
    pagina = contexto.new_page()
    pagina.goto("https://library.uniquindio.edu.co/databases")
    pagina.bring_to_front()
    pagina.wait_for_load_state("domcontentloaded")


    try:
        # Acceder al enlace de IEEE
        pagina.locator("div[data-content-listing-item='fac-ingenier-a']").click()
        link = pagina.locator(
            "//a[contains(@href, 'https://ieeexplore-ieee-org.crai.referencistas.com/Xplore/home.jsp')]//span[contains(text(), 'IEEE (Institute of Electrical and Electronics Engineers) - (DESCUBRIDOR)')]")
        pagina.wait_for_load_state("domcontentloaded")
        link.last.click()

        # Iniciar sesión con correo institucional en caso de ser necesario
        if pagina.url != "https://ieeexplore-ieee-org.crai.referencistas.com/Xplore/home.jsp":
            automatizacion.iniciar_sesion(pagina)

        #Manejo de la búsqueda
        busqueda = 'input[type="search"]'
        pagina.wait_for_selector(busqueda, timeout=60000)
        pagina.fill(busqueda, '"computational thinking"')
        pagina.press(busqueda, "Enter")
        time.sleep(5)
        pagina.wait_for_load_state("domcontentloaded")

        # Seleccion de n resultados por pagina
        pagina.locator("#dropdownPerPageLabel").click()
        pagina.locator('button:has-text("100")').click()
        pagina.wait_for_load_state("domcontentloaded")

        # Descarga de citas en formato bibtex
        i = 0
        while True:
            try:
                i+=1
                # Seleccionar todas las citas y presionar el botón de exportar
                pagina.get_by_role("checkbox", name="Select All on Page").check()
                pagina.get_by_role("button", name="Export").click()

                # Seleccionar la opcion de exportar como cita y el formato bibtex
                pagina.locator("a.nav-link:has-text('Citations')").click()
                pagina.wait_for_load_state("domcontentloaded")
                pagina.locator('//label[@for="download-bibtex"]//input').check()

                # Descargar archivo
                with pagina.expect_download() as download_info:
                    pagina.wait_for_selector("button.stats-SearchResults_Citation_Download", timeout=10000).click()
                download = download_info.value
                download_path = os.path.join(os.getcwd(), "Datos", f"IEEE_{i}.bib")
                download.save_as(download_path)
                print(f"Archivo descargado en: {download_path}")
                time.sleep(1)

                pagina.get_by_role("button", name="Cancel").click()
                pagina.wait_for_load_state("domcontentloaded")

                # Manejo de paginación
                next_button = pagina.locator("//button[contains(text(), ' > ')]")

                if not next_button.is_visible():
                    print("El botón 'Next' no es visible. Fin del proceso.")
                    break

                next_button.click()
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(2)

            except Exception as e:
                print(f"No hay más páginas.{e}")
                break


    except Exception as e:
        print(f"Exception: {e}")
        navegador.close()
        playwright.stop()
        return
