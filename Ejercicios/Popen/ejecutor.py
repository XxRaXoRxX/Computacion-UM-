#subprocess Popen.
# En este ejercicio la idea es agregar un comando y ejecutarlo en el sistema como -c "nombre del documento", de ahi lo almacenamos en dos archivos de documetos,
# mostrando en un archivo el output como -f "nombre de archivo" y el -i "nombre de archivo" almacenamos el log de errores. 

import argparse as arg
import datetime as date
import os

# Funcion utilizado para realizar el comando y almacenar el log y commando dentro de archivos. 
def UseCommands(command, commandArchive, logArchive):
    # Creación de archivo temporal para verificar si el error se genera o no.
    error = "ErrorLogBetaTesting.txt"

    os.system(f"{command} 1>> ./{commandArchive} 2> ./{error}")

    archive = open(error, "r")
    lines = archive.read()

    if (lines == ""):
        os.system(f"echo '{date.datetime.now()}: Comando |{command}| ejecutado correctamente.' >> ./{logArchive}")
    else:
        os.system(f"{command} 2>> ./{logArchive}")

    archive.close()
    os.system(f"rm ./{error}")

# Generas el parser con una descripción
parser = arg.ArgumentParser(description="Realizar un comando y almacenar comando y log dentro de archivos.")

# Ingreso de argumentos
parser.add_argument("-c", "--command", type=str, help="Comando a realizar dentro del sistema.")
parser.add_argument("-f", "--saveCommand", type=str, help="Archivo a pegar el comando.")
parser.add_argument("-l", "--saveLogs", type=str, help="Archivo a pegar los errores.")

# Obtener lista de argumentos en args.
args = parser.parse_args()

# Verificar si los datos ingresados son correctos.
if (args.command and args.saveCommand and args.saveLogs):
    UseCommands(command = args.command, commandArchive = args.saveCommand, logArchive = args.saveLogs)
else:
    print("Ingreso de parametros incorrecto.")