# ArgParse Ejemplo:
# Ej2: Escribir un programa que reciba dos nombres de archivos por línea de órdenes utilizando los parámetros “-i” y “-o” procesados con argparse.
# Ej: python3 copiar.py -i existente.txt -o nuevo.txt

import argparse
import os

# Generas el parser con una descripción
parser = argparse.ArgumentParser(description="Realizar una copia de un archivo")

# Ingreso de argumentos
parser.add_argument("-i", "--copy", type=str, help="Archivo a realizar el copiado")
parser.add_argument("-o", "--paste", type=str, help="Pegar archivo copiado")

# Obtener lista de argumentos en args.
args = parser.parse_args()

# Funcion para copiar y pegar archivos.
def CopiarPegar(archivoCopiar, archivoPegar):
    if(archivoCopiar == "" or archivoPegar == ""):
        print("El parametro ingresado es vacio.")
        return

    os.system(f"cp ./{archivoCopiar} ./{archivoPegar}.")
    print(f"El archivo {archivoCopiar} se realizo una copia en {archivoPegar}.")

# Verificar si los datos ingresados son correctos.
if (args.copy and args.paste):
    CopiarPegar(archivoCopiar = args.copy, archivoPegar = args.paste)
else:
    print("Ingreso de parametros incorrecto.")