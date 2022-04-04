#subprocess Popen.
# En este ejercicio la idea es agregar un comando y ejecutarlo en el sistema como -c "nombre del documento", de ahi lo almacenamos en dos archivos de documetos,
# mostrando en un archivo el output como -f "nombre de archivo" y el -i "nombre de archivo" almacenamos el log de errores. 

import argparse as arg
import datetime as date
import os

from subprocess import Popen, PIPE, STDOUT

# Funcion utilizado para realizar el comando y almacenar el log y commando dentro de archivos.
# Función realizada SIN el Subprocess Popen
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

# Funcion utilizado para realizar el comando y almacenar el log y commando dentro de archivos.
# Función realizada CON el Subprocess Popen
def UseCommandsSubprocess(command, commandArchive, logArchive):
    #Realizo el comando con el Popen, generando un hijo con el proceso de comando, el proceso hijo es p.
    p = Popen([f"{command}"], shell=True, stdout=PIPE, stderr=PIPE)
    #Guardo el output y error del popen en dos variables.
    out, err = p.communicate()

    #El returncode al ser cero significa que no hubo error y guarda lo que devuelve el comando y la fecha en el log.
    if p.returncode == 0:
        with open(commandArchive, "a") as command_file:
            command_file.write(str(out) + "\n")

        txt = f"Fecha y Hora: {date.datetime.now()}. Comando: {command} ejecutado correctamente."
        with open(logArchive, "a") as error_file:
            error_file.write(str(txt) + "\n")
    #El returncode al ser diferente de 0 es que dio algun tipo de error, entonces hay que guardar el error en el log.
    else:
        with open(logArchive, "a") as error_file:
            error_file.write(str(err) + "\n")

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
    UseCommandsSubprocess(command = args.command, commandArchive = args.saveCommand, logArchive = args.saveLogs)
else:
    print("Ingreso de parametros incorrecto.")