# Sincronización y nmap.
# Etapa 1:
# - El programa deberá crear un segmento de memoria compartida anónima, y generar dos hijos: H1 y H2
# - El H1 leerá desde el stdin línea por línea lo que ingrese el usuario.
# - Cada vez que el usuario ingrese una línea, H1 la almacenará en el segmento de memoria compartida, y enviará la señal USR1 al proceso padre.
# - El proceso padre, en el momento en que reciba la señal USR1 deberá mostrar por pantalla el contenido de la línea ingresada por el H1 en la memoria compartida, 
# y deberá notificar al H2 usando la señal USR1.
# - El H2 al recibir la señal USR1 leerá la línea desde la memoria compartida la línea, y la almacenará en mayúsculas en el archivo pasado por argumento (path_file).
# Etapa 2:
# - Cuando el usuario introduzca "bye" por terminal, el hijo H1 enviará la señal USR2 al padre indicando que va a terminar, y terminará.
# - El padre, al recibir la señal USR2 la enviará al H2, que al recibirla terminará también.
# - El padre esperará a que ambos hijos hayan terminado, y terminará también.

import os, sys, signal
import argparse as arg
from mmap import mmap

class Constants():
    ERROR = "Valores ingresados incorrectos. Ingresa -h para mas información."
    BYTE = b"\x00"

class Main():

    memory = ""
    pidChildList = []
    archive = ""

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
            self.archive = open(file, "w")
        else:
            print("El archivo ingresado no existe. Cerrando...")
            return

        #Creación del mapeo de memoria.
        self.memory = mmap(-1, 100)
        
        #Creación de señales en el padre
        signal.signal(signal.SIGUSR1, self.FatherSignalUSR1)
        signal.signal(signal.SIGUSR2, self.FatherSignalUSR2)

        # Genero ambos hijos.
        for i in range(2):
        
            pid = os.fork()
            if (pid == 0):
                if (i == 0):
                    self.Child1()
                    exit(0)
                else:
                    self.Child2()
                    return
            else:
                self.pidChildList.append(pid)

        # Esperar hasta que el ultimo proceso hijo finalice.
        #print(self.pidChildList)
        for i in range(2):
            os.wait()

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")

    def FatherSignalUSR1(self, s, f):
        """Señal del Padre para recibir lo del H1 (Child 1) los datos ingresados por el usuario.

        args:
                -s: Número de señal.
                -f: FRAME. Puntero donde el proceso debe volver en stack al finalizar esta función.
        """
        
        # Printeo en pantalla lo enviado por el Child 1 y le mando una señal al Child 2
        self.memory.seek(0)
        print("Padre recibiendo texto:", self.memory.read().decode())
        os.kill(self.pidChildList[1], signal.SIGUSR1)

    def FatherSignalUSR2(self, s, f):
        """Señal del Padre para recibir lo del H1 (Child1) cuando el usuario escribe un bye.

        args:
                -s: Número de señal.
                -f: FRAME. Puntero donde el proceso debe volver en stack al finalizar esta función.
        """

        print("Child 1 Finalizando...")
        # Enviando al child 2 que se suicide.
        os.kill(self.pidChildList[1], signal.SIGUSR2)


    def Child1(self):
        """Proceso Hijo 1, que se encarga de obtener lo escrito por el usuario en la terminal.

        args:
                -memory: Memoria virtual
        """
        for line in sys.stdin:

            #Quito el \n
            line = line[:-1]

            #Escritura "bye" cierra el bucle
            if (line == "bye" or line == "Bye" or line == "BYE"):
                print("Saliendo...")
                os.kill(os.getppid(), signal.SIGUSR2)
                return

            # Muevo el puntero a 0 para volver a escribir desde el inicio.
            self.memory.seek(0)
            # Elimino todo el contenido de la memoria dejando bites vacios.
            cons = Constants()
            self.memory[0:100] = cons.BYTE*100
            # Escribo la linea en memoria.
            self.memory.write(line.encode())
            os.kill(os.getppid(), signal.SIGUSR1)

    def Child2(self):
        """Proceso Hijo 2, que obtiene lo que escribio el usuario y lo transforma en mayuscula, guardandolo en un archivo.

        args:
                -archive: Archivo donde pegar lo escrito por el usuario en mayúscula.
        """

        # Cambio la señal SIGUSR1 a una función.
        signal.signal(signal.SIGUSR1, self.Child2SignalUSR1)
        signal.signal(signal.SIGUSR2, self.Child2SignalUSR2)
        
        #Me quedo esperando a que envien una señal.
        while True:
            signal.pause()

    def Child2SignalUSR1(self, s, f):
        """Señal del Hijo 2 para recibir del Padre los datos ingresados por el usuario.

        args:
                -s: Número de señal.
                -f: FRAME. Puntero donde el proceso debe volver en stack al finalizar esta función.
        """

        # Leo en texto en memoria y lo almaceno en el archivo en mayúscula
        self.memory.seek(0)
        text = self.memory.readline()
        text = text.decode().upper()

        # Quitar los string "\00" al decodear memoria vacia. 
        text = text.strip("\00")

        print("Escribiendo:", text, "en archivo...")

        # Agregarle un "\n" al final del texto
        text = text + "\n"
        self.archive.write(text)

    def Child2SignalUSR2(self, s, f):
        """Señal del Hijo 2 para recibir del Padre cuando se van a cerrar los procesos.

        args:
                -s: Número de señal.
                -f: FRAME. Puntero donde el proceso debe volver en stack al finalizar esta función.
        """
        
        print("Child 2 Finalizando...")
        exit(0)

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: