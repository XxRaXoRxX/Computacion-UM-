# Sincronización y nmap.
# Etapa 1:
# -  El programa deberá crear un segmento de memoria compartida anónima, y generar dos hijos: H1 y H2
# - El H1 leerá desde el stdin línea por línea lo que ingrese el usuario.
# - Cada vez que el usuario ingrese una línea, H1 la almacenará en el segmento de memoria compartida, y enviará la señal USR1 al proceso padre.
# - El proceso padre, en el momento en que reciba la señal USR1 deberá mostrar por pantalla el contenido de la línea ingresada por el H1 en la memoria compartida, 
# y deberá notificar al H2 usando la señal USR1.
# - El H2 al recibir la señal USR1 leerá la línea desde la memoria compartida la línea, y la almacenará en mayúsculas en el archivo pasado por argumento (path_file).
# Etapa 2:
# - Cuando el usuario introduzca "bye" por terminal, el hijo H1 enviará la señal USR2 al padre indicando que va a terminar, y terminará.
# - El padre, al recibir la señal USR2 la enviará al H2, que al recibirla terminará también.
# - El padre esperará a que ambos hijos hayan terminado, y terminará también.

import os
import argparse as arg
from nmap import nmap

class Constants():
    ERROR = "Valores ingresados incorrectos. Ingresa -h para mas información."

class Main():

    def main(self):
        args = self.ArgumentsConfig()
        cons = Constants()

        if (args.file):
            self.Fork(file = args.file, constants = cons)
        else:
            print(cons.ERROR)


    def ArgumentsConfig(self):
        """Genero el ArgParse y sus argumentos.

        return:
                -arguments: Devuelve los argumentos creados en el argparse.
        """

        # Generas el parser con una descripción
        parser = arg.ArgumentParser(description="Generar procesos hijos y invierten el texto del archivo, todo mediante os.pipe().")

        # Ingreso de argumentos
        parser.add_argument("-f", "--file", type=str, help="Archivo donde un hijo va a escribir lo escrito en mayuscula.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    
    def Fork(self, file, constants):
        """Realizo el forkeo y genero los hijos

        ags:
                -file: Ubicación del archivo a invertir el texto.
                -constants: Lista de constantes.
        """

        # Creado un archivo en caso de no existir, sino lo cargo
        if os.path.exists(file):
            archive = open(file, "r")
        else:
            print("El archivo ingresado no existe. Cerrando...")
            return

        lines = archive.readlines()

        #Creación del mapeo de memoria.
        nmap.nmap(-1, 0)

        # Genero ambos hijos.
        for i in range(2):

            if not os.fork():
                pass

        # Esperar hasta que el ultimo proceso hijo finalice.
        pid, status = os.waitpid(child_pid, 0)

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")

    def Inversor(self, read, write):
        """Realiza la suma de pares para cada proceso.

        args:
                -read: Lectura del pipe
                -write: Escritura del pipe
        """

        #Obtener lectura del pipe
        text = os.read(read, 100)
        #Decodear los bites.
        text = text.decode()

        #Quito el /n del texto
        text = text[:-2]
        #Invertir letras.
        text = text[::-1]
        #Agrego un /n al final texto
        text += "\n"

        #Enviar texto al padre.
        os.write(write, text.encode())
        #Cerrar el write del pipe
        os.close(write)
        #Cerrando el read del pipe
        os.close(read)
        
#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: