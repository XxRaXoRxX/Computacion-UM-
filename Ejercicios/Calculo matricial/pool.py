# Calculo matricial.
# Realizar un programa en python que reciba por argumentos:
# -p cantidad_procesos
# -f /ruta/al/archivo_matriz.txt
# -c funcion_calculo
# El programa deberá leer una matriz almacenada en el archivo de texto pasado por argumento -f,
# y deberá calcular la funcion_calculo para cada uno de sus elementos.
# Para aumentar la performance, el programa utilizará un Pool de procesos, y cada proceso del pool realizará los cálculos sobre una de las filas de la matriz.
# La funcion_calculo podrá ser una de las siguientes:
# -raiz: calcula la raíz cuadrada del elemento.
# -pot: calcula la potencia del elemento elevado a si mismo.
# -log: calcula el logaritmo decimal de cada elemento.

import os, sys, math
import argparse as arg
from multiprocessing import Pool

class Constants():
    ERROR = "Valores ingresados incorrectos. Ingresa -h para mas información."
    RAIZ = "raiz"
    POT = "pot"
    LOG = "log"

class Main():
    def main(self):
            args = self.ArgumentsConfig()
            cons = Constants()

            if (args.file and args.process and args.calc):
                self.Process(args = args, cons = cons)
            else:
                print(cons.ERROR)


    def ArgumentsConfig(self):
        """Genero el ArgParse y sus argumentos.

        return:
                -arguments: Devuelve los argumentos creados en el argparse."""

        # Generas el parser con una descripción
        parser = arg.ArgumentParser(description="Realizar calculos en diferentes procesos.")

        # Ingreso de argumentos
        parser.add_argument("-p", "--process", type=int, help="Cantidad de procesos a realizar el calculo.")
        parser.add_argument("-f", "--file", type=str, help="Archivo donde leer la raiz..")
        parser.add_argument("-c", "--calc", type=str, help="Tipo de calculo, |raiz| calcular la raiz, |pot| calcular la potencia, |log| calcular logaritmo.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    def Process(self, args, cons):
        """Genero la cantidad de procesos ingresado por parametro.

        args:
                -args: Lista de argumentos ingresado por el usuario.
                -cons: Lista de constantes"""
        
        # Creación de los procesos.
        process = Pool(processes = args.process)

        matrix = []

        # Quito las comas y dejo solo numeros dentro de la matrix a editar.
        for line in self.ReadTxt(args.file):
            #Separar valores por la |, |.
            split = line.split(", ")
            split = list(map(float, split)) #Transformar lista de str a float.
            matrix.append(split)

        #Printeo en pantalla
        matrix = self.PrintMatrix(calc = args.calc, matrix = matrix, process = process, cons = cons)

        if (matrix == None):
            return
        else:
            self.PrintMatrix(matrix = matrix)


    def SplitFunction(self, calc, matrix, process, cons):
        """Ejecuto segun el calculo que hay que realizar.

        args:
                -calc: Tipo de calculo a realizar.
                -matrix: Matriz a realizar el calculo
                -process: Procesos a realizar la tarea.
                -cons: Lista de constantes."""
        
        newMatrix = []
        for m in matrix:
            if (calc == cons.RAIZ):
                newMatrix.append(process.map(self.Root, m)) 
            elif (calc == cons.POT):
                newMatrix.append(process.map(self.Pot, m)) 
            elif (calc == cons.LOG):
                newMatrix.append(process.map(self.Log, m))
            else:
                print("Error, valor del calculo ingresado incorrecto: " + str(calc))
                return None

        return newMatrix

    def PrintMatrix(self, matrix):
        """Transformar la lista a escritura de matriz tipo .txt.

        args:
                -matrix: Matriz a printear"""

        string = ""
        for m in matrix:
            for i in range(len(m)):
                if(i != (len(m) - 1)):
                    string += str(m[i]) + ", "
                else:
                    string += str(m[i]) + "\n"

        print(string)

    def ReadTxt(self, archive):
        """Leo la matriz ingresada en el .txt

        args:
                -archive: Nombre del archivo a abrir."""
        
        archive = open(archive, "r")
        lines = archive.readlines()
        return lines


    def Root(self, value):
        """Calcula la raíz cuadrada del elemento.

        args:
                -value: Valor a realizar el calculo."""
                
        return math.sqr(value)

    def Pot(self, value):
        """Calcula la potencia del elemento elevado a si mismo.

        args:
                -value: Valor a realizar el calculo."""

        return value ** value

    def Log(self, value):
        """Calcula el logaritmo decimal de cada elemento.

        args:
                -value: Valor a realizar el calculo."""

        return math.log(value)

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia:
# Transformar una lista completa de str a int: https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int