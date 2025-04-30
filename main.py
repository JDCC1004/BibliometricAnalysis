import os

from Automation.automatizacion import descargar_citas
from Automation.arreglar_ieee import procesar_archivos_ieee
from Methods.unificarArchivos import unificar_filtrar_archivos
from Methods.agrupacion import agrupacion
import subprocess
from Methods.TextSimilarity import abstract_handler
from Methods.TextSimilarity import tf_idf, bert

def main():

    #Req 1
    #descargar_citas()  # ---> Descarga las citas de las bases de datos Sage, IEEE y ScienceDirect de manera automatizada
    #procesar_archivos_ieee() # ---> Arregla las entradas IEEE en formato BibTeX (Saltos de linea)
    #unificar_filtrar_archivos() # ---> Unifica y filtra las citas descargadas de las bases de datos

    #Req 2
    agrupacion()


    #Req 3
    #subprocess.run(["python", "Methods/Token.py"])
    subprocess.run(["python", "Methods/Token.py"])
    subprocess.run(["python", "Methods/Coincidences.py"])
    subprocess.run(["python", "Methods/Tab.py"])
    subprocess.run(["python", "Methods/WordCloud.py"])
    subprocess.run(["python", "Methods/WordCloud_Cat.py"])
    subprocess.run(["python", "Methods/Co-Word.py"])
    subprocess.run(["python", "Methods/Co-Word_Cat.py"])

    #Req 5
    #abstract_handler.extract()
    #abstract_handler.normalize()
    #tf_matrix = tf_idf.tfidf()
    #bert_matrix = bert.bert()

if __name__ == "__main__":
    main()
