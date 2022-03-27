# GetOPT Ejemplo:
# Ej1: Crear una calculadora, donde se pase como argumentos luego de la opción -o el operador que se va a ejecutar (+,-,*,/), 
# luego de -n el primer número de la operación, y de -m el segundo número.
# Ej: python3 calc.py -o + -n 5 -m 6

import getopt
import sys

# Función de calculadora, donde lleva los siguientes parametros
# -o: (+,-,x,/) El signo * no funciona, me devuelve el nombre del script como argumento.
# -n: Primer número
# -m: segundo número
def Calculadora(signo, primerNumero, segundoNumero):
    if (primerNumero.isnumeric() and segundoNumero.isnumeric()):

        primerNumero = int(primerNumero)
        segundoNumero = int(segundoNumero)
        
        switcher = {
            "+": primerNumero + segundoNumero,
            "-": primerNumero - segundoNumero,
            "x": primerNumero * segundoNumero,
            "/": primerNumero / segundoNumero 
        }
        return switcher.get(signo, "Signo Incorrecto, intentalo de nuevo.")
    else:
        return "Números ingresados incorrectos."

# Obtenemos argumentos mediante getopt.
(opt,arg) = getopt.getopt(sys.argv[1:], 'o:n:m:')
#(opt,arg) = getopt.getopt(sys.argv[1:], 'ab:c', ["agregar", "opcion1", "opcion2="]) En este caso se puede llamar -a, -b algo, -c // -agregar, -opcion1, -opcion2 algo.

# Mostramos en pantalla opciones almacenado en opt y argumentos almacenado en arg.
print("opciones: ", opt)
print("argumentos: ", arg)

# Realizamos la operación de calculadora en caso de tener las opciones y argumentos correctos
signo = "?"
num1 = "?"
num2 = "?"

# Realiza una busqueda de opciones y verifica si la opcion ingresada es correcta, y al lado de la opcion ingresada va el valor ar, que es el argumento que obtiene.
for (op,ar) in opt:
        if (op == "-o"):
            signo = ar
        elif (op == "-n"):
            num1 = ar
        elif (op == "-m"):
            num2 = ar
        else:
            print("Valores ingresados en", str(op), "es incorrecto.")

print( num1, signo, num2, "=", Calculadora(signo = signo, primerNumero = num1, segundoNumero = num2) )