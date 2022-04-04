# Procesos fork.
# El programa debe generar <numero> procesos hijos, y cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID.
# PID – PPID : <suma_pares>
# La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación. 
# El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la ejecución de cada proceso hijo, que indique su inicio y fin.

import os
import argparse as arg

class Constants():
    HELP = """El programa debe generar <numero> procesos hijos, y cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID.
    PID – PPID : <suma_pares>
    -n: Es la cantidad de procesos a generar.
    -h: Muestra una ayuda de como funciona el codigo.
    -v: Habilita el modo verboso de la aplicación."""

class Main():

    def main(self):
        args = self.ArgumentsConfig()
        mode_verbose = False

        if (args.helps):
            cons = Constants()
            print(cons.HELP)
            return

        elif (args.verbose):
            mode_verbose = True

        elif (args.number):
            self.Fork(loop = args.number, verbose = mode_verbose)
        
        else:
            print("Valores ingresados incorrectos. Ingresa -h para mas información.")


    def ArgumentsConfig(self):
        """Genero el ArgParse y sus argumentos.

        return:
                -arguments: Devuelve los argumentos creados en el argparse.
        """

        # Generas el parser con una descripción
        parser = arg.ArgumentParser(description="Generar procesos hijos y realizar una suma par entre 0 y el PID.")

        # Ingreso de argumentos
        parser.add_argument("-n", "--number", type=int, help="Cantidad de procesos a generar.")
        parser.add_argument("-i", "--helps", type=str, help="Ayuda de como utilizar este archivo python.")
        parser.add_argument("-v", "--verbose", type=str, help="Modo detallado.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    
    def Fork(self, loop, verbose):
        """Realizo el forkeo y genero los hijos

        ags:
                -loop: Cuantos hijos genero
                -verbose: Booleano para identificar si estoy en modo verboso o no.
        """
        status = 0

        for i in range(loop):
            child_pid = os.fork()
            if (child_pid == 0):
                #codigo del hijo
                self.SumaPares(verbose = verbose)

                os._exit(0)

        wpid = os.wait(status)
        while (wpid > 0):
            pass

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")


    def SumaPares(self, verbose):
        """Realiza la suma de pares para cada proceso.

        args:
                -verbose: Booleano para identificar si estoy en modo verboso o no.
        """
        pid = os.getpid()
        ppid = os.getppid()

        if (verbose): print(f"Starting process: {pid}")

        suma = 0
        for i in range(pid):
            suma += 2
        print(f"{pid} - {ppid}: {suma}")

        if (verbose): print(f"Ending process: {pid}")

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia:
# Como hacer que el padre espere a que los hijos terminen sus procesos para finalizar: https://stackoverflow.com/questions/19461744/how-to-make-parent-wait-for-all-child-processes-to-finish