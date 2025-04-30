from Automation.arreglar_ieee import procesar_archivos_ieee
from Automation.automatizacion import descargar_citas
from Methods.agrupacion import agrupacion
from Methods.unificarArchivos import unificar_filtrar_archivos
from Methods.TextSimilarity import abstract_handler
from Methods.TextSimilarity import tf_idf

def main():

    descargar_citas()  # ---> Descarga las citas de las bases de datos Sage, IEEE y ScienceDirect de manera automatizada
    procesar_archivos_ieee() # ---> Arregla las entradas IEEE en formato BibTeX (Saltos de linea)
    unificar_filtrar_archivos() # ---> Unifica y filtra las citas descargadas de las bases de datos
    agrupacion()

    abstract_handler.extract()
    abstract_handler.normalize()
    tf_idf.tfidf()





if __name__ == "__main__":
    main()