# Calculo matricial. Utilizando Celery.
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
from celery import Celery
from tasks import Root, Pot, Log

class Constants():
    ERROR = "Valores ingresados incorrectos. Ingresa -h para mas información."
    RAIZ = "raiz"
    POT = "pot"
    LOG = "log"

class Main():
    def main(self):
            args = self.ArgumentsConfig()
            cons = Constants()

            if (args.file and args.calc):
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
        parser.add_argument("-f", "--file", type=str, help="Archivo donde leer la raiz..")
        parser.add_argument("-c", "--calc", type=str, help="Tipo de calculo, |raiz| calcular la raiz, |pot| calcular la potencia, |log| calcular logaritmo.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    def Process(self, args, cons):
        """Genero la cantidad de procesos ingresado por parametro.

        args:
                -args: Lista de argumentos ingresado por el usuario.
                -cons: Lista de constantes"""

        matrix = []

        # Quito las comas y dejo solo numeros dentro de la matrix a editar.
        for line in self.ReadTxt(args.file):
            #Separar valores por la |, |.
            split = line.split(", ")
            split = list(map(float, split)) #Transformar lista de str a float.
            matrix.append(split)

        #Printeo en pantalla
        matrix = self.SplitFunction(calc = args.calc, matrix = matrix, cons = cons)

        if (matrix == None):
            return
        else:
            self.PrintMatrix(matrix = matrix)


    def SplitFunction(self, calc, matrix, cons):
        """Ejecuto segun el calculo que hay que realizar.

        args:
                -calc: Tipo de calculo a realizar.
                -matrix: Matriz a realizar el calculo
                -cons: Lista de constantes."""
        
        newMatrix = []
        for m in matrix:
            if (calc == cons.RAIZ):
                result = Root.delay(m)
                newMatrix.append(result.get()) 
            elif (calc == cons.POT):
                result = Pot.delay(m)
                newMatrix.append(result.get()) 
            elif (calc == cons.LOG):
                result = Log.delay(m)
                newMatrix.append(result.get())
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

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia:
# Transformar una lista completa de str a int: https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int

#Codigo de test:
# python3 pool.py -f "matriz.txt" -c raiz|pot|log