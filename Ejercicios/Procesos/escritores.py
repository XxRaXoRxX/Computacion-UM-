# Procesos fork_fd.
# El programa deberá abrir (crear si no existe) un archivo de texto cuyo path ha sido pasado por argumento con -f.
# El programa debe generar <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto (el primer proceso con la "A", el segundo con la "B", etc). 
# Cada proceso almacenará en el archivo su letra <R> veces con un delay de un segundo entre escritura y escritura (realizar flush() luego de cada escritura).
# El proceso padre debe esperar a que los hijos terminen, luego de lo cual deberá leer el contenido del archivo y mostrarlo por pantalla.
# La opción -h mostrará ayuda. La opción -v activará el modo verboso, en el que se mostrará antes de escribir cada letra en el archivo: Proceso <PID> escribiendo letra 'X'.

from distutils import archive_util
import time
import os
import argparse as arg

class Constants():
    HELP = """El programa debe generar <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto (el primer proceso con la "A", el segundo con la "B", etc).
    Cada proceso almacenará en el archivo su letra <R> veces con un delay de un segundo entre escritura y escritura (realizar flush() luego de cada escritura).
    Retorna las letras de cada proceso, como por ejemplo, ABCACBABCBAC.
    -n: Cantidad de procesos hijos a generar.
    -r: Cantidad de repetición de letras despues del delay.
    -f: Archivo de texto que se crea con la información de los procesos detro.
    -hh: Muestra una ayuda de como funciona el codigo.
    -v: Habilita el modo verboso de la aplicación."""
    ERROR = "Valores ingresados incorrectos. Ingresa -hh para mas información."

class Main():

    def main(self):
        args = self.ArgumentsConfig()
        cons = Constants()

        if (args.helps):
            print(cons.HELP)
            return

        elif (args.number and args.repeat and args.file):
            self.Fork(loop = args.number, repeat = args.repeat, file = args.file, verbose = args.verbose)
        
        else:
            print(cons.ERROR)


    def ArgumentsConfig(self):
        """Genero el ArgParse y sus argumentos.

        return:
                -arguments: Devuelve los argumentos creados en el argparse.
        """

        # Generas el parser con una descripción
        parser = arg.ArgumentParser(description="Generar procesos hijos y printea una letra con un segundo de delay.")

        # Ingreso de argumentos
        parser.add_argument("-n", "--number", type=int, help="Cantidad de procesos a generar.")
        parser.add_argument("-r", "--repeat", type=int, help="Cantidad de repeticiones de letras despues del delay.")
        parser.add_argument("-f", "--file", type=str, help="Archivo de texto que se crea con la información de los procesos dentro.")
        parser.add_argument("-hh", "--helps", action="store_true", help="Ayuda de como utilizar este archivo python.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Modo detallado.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    
    def Fork(self, loop, repeat, file, verbose):
        """Realizo el forkeo y genero los hijos

        ags:
                -loop: Cuantos hijos genero
                -repeat: Repetición de letras de cada proceso
                -file: Ubicación del archivo.
                -verbose: Booleano para identificar si estoy en modo verboso o no.
        """
        alphabet =  ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "LL", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        archive = open(file, "a")

        for i in range(loop):
            child_pid = os.fork()
            if (child_pid == 0):
                #codigo del hijo
                self.Escritores(word = alphabet[i], repeat = repeat, file = archive, verbose = verbose)

                os._exit(0)

        # Esperar hasta que el ultimo proceso hijo finalice.
        pid, status = os.waitpid(child_pid, 0)

        archive.write("\n")
        archive.close()

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")


    def Escritores(self, word, repeat, file, verbose):
        """Realiza la suma de pares para cada proceso.

        args:
                -letra: Letra a printear por cada delay.
                -repeat: Repetición de letras de cada proceso.
                -file: Ubicación del archivo.
                -verbose: Booleano para identificar si estoy en modo verboso o no.
        """

        pid = os.getpid()

        for i in range(repeat):

            if (verbose): print(f"Proceso {pid} escribiendo letra {word}")

            #Escribir letra en el archivo.
            file.write(word)

            #Guardar archivo en el disco.
            file.flush()
            os.fsync(file)

            #Esperar un segundo.
            time.sleep(1)

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia:
# Como hacer que el padre espere a que los hijos terminen sus procesos para finalizar: https://stackoverflow.com/questions/10684180/python-checking-if-a-fork-process-is-finished