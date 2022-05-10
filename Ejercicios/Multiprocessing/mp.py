# Multiprocessing
# Escribir un programa que genere dos hijjos utilizando multiprocessing.
# Uno de los hijos deberá leer desde stdin texto introducido por el usuario, y deberá escribirlo en un pipe (multiprocessing).
# El segundo hijo deberá leer desde el pipe el contenido de texto, lo encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).
# El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

import os, sys, signal
import argparse as arg
import multiprocessing as mp
from codecs import encode

class Constants():
    STOP = "Para parar bucle escribir |stop|"
    CHILD1_STOP = "Cerrando Hijo 1..."
    CHILD2_STOP = "Cerrando Hijo 2..."
    FATHER_STOP = "Cerrando Padre..." 

class Main():

    #Variables Globales.
    #Genero el queue
    q = mp.Queue()

    def main(self):
        cons = Constants()
        self.Multiprocessing(cons = cons)

    def Multiprocessing(self, cons):
        """
        Generamos los dos hijos y funcionamiento.

        args:
                -cons: Constantes."""

        #Me guardo el stdin en una variable.
        fn = sys.stdin.fileno()

        #Genero el pipe.
        child1_conn, child2_conn = mp.Pipe()

        #Genero el primer hijo
        child1 = mp.Process(target = self.Child1, name = "Terminal Reader", args = (child1_conn, fn, cons))
        child1.start()
        #Genero el segundo hijo
        child2 = mp.Process(target = self.Child2, name = "Encripter", args = (child2_conn, child1.pid, cons))
        child2.start()

        #Esperando a que los hijos se cierren para poder cerrarse.
        while True:
            if (not child1.is_alive() and not child2.is_alive()):
                child1.join()
                child2.join()
                print(cons.FATHER_STOP)
                break
                


    def Child1(self, pipe, fn, cons):
        """Lee la terminal y manda todo esos datos al pipe.

        args:
                -pipe: Un extremo del pipe compartido entre los hijos.
                -fn: Terminal principal.
                -cons: Constantes"""

        print(cons.STOP)

        #Señal para obtener los datos del queue.
        signal.signal(signal.SIGUSR1, self.Child1_Print)

        #Le doy acceso a la terminal al proceso hijo. 
        sys.stdin = os.fdopen(fn)

        #Al escribir en la terminal lo mando al pipe.
        for str in sys.stdin:

            #Le quito el \n al texto
            str = str[:-1]

            if (str == "stop"):
                #Envio una señal al child2 para que se cierre.
                pipe.send("stop")
                print(cons.CHILD1_STOP)
                exit(0)

            #Envio lo escrito al pipe.
            pipe.send(str)

    def Child2(self, pipe, child1_PID, cons):
        """Realiza el encriptado rot13.

        args:
                -pipe: El pipe del hijo.
                -child1_PID: El número del pid del segundo hijo
                -cons: Constantes"""

        while True:
            #Recibo el texto del pipe.
            text = pipe.recv()

            #Si el texto es stop que se cierre.
            if(text == "stop"):
                self.Child2_Exit(cons = cons)

            #Lo transformo a rot13
            text = encode(text, "rot_13")

            #Lo almaceno en queue.
            self.q.put(text)

            #Aviso por señal al hijo 1.
            os.kill(child1_PID, signal.SIGUSR1)
            
    def Child1_Print(self, s, f):
        """Printar en pantalla el archivo encriptado.
        
        args:
                -s: Número de señal.
                -f: FRAME. Puntero donde el proceso debe volver en stack al finalizar esta función."""

        print(self.q.get())

    def Child2_Exit(self, cons):
        """Cerrar el programa hijo 2.
        
        args:
                -cons: Constantes"""
            
        print(cons.CHILD2_STOP)
        exit(0)

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: