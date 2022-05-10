# Multiprocessing
# Escribir un programa que genere dos hijjos utilizando multiprocessing.
# Uno de los hijos deberá leer desde stdin texto introducido por el usuario, y deberá escribirlo en un pipe (multiprocessing).
# El segundo hijo deberá leer desde el pipe el contenido de texto, lo encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).
# El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

import os, sys, signal
import argparse as arg
import multiprocessing as mp
from codecs import encode #encode("str", "rot_13") 

class Constants():
    pass

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

        #Genero el segundo hijo
        child2 = mp.Process(target = self.Child2, name = "Encripter", args = (child2_conn,))
        #Genero el primer hijo
        child1 = mp.Process(target = self.Child1, name = "Terminal Reader", args = (child1_conn, child2.pid, fn))

        #Inicio los hijos
        child1.run()
        child2.run()

        #Esperando a que los hijos se cierren para poder cerrarse.
        while True:
            print(child1.is_alive())
            print(child2.is_alive())
            if (not child1.is_alive() and not child2.is_alive()):
                child1.join()
                child2.join()
                break;
                


    def Child1(self, pipe, child2_PID, fn):
        """Lee la terminal y manda todo esos datos al pipe.
        args:
                -pipe: Un extremo del pipe compartido entre los hijos.
                -child2_PID: El número del pid del segundo hijo
                -fn: Terminal principal."""

        #Señal para obtener los datos del queue.
        signal.signal(signal.SIGUSR1, self.Child1_Print)

        #Le doy acceso a la terminal al proceso hijo. 
        sys.stdin = os.fdopen(fn)

        #Al escribir en la terminal lo mando al pipe.
        for str in sys.stdin:
            if (str[:-1] == "stop"):
                #Envio una señal al child2 para que se cierre.
                os.kill(child2_PID, signal.SIGUSR1)
                exit(0)

            #Envio lo escrito al pipe.
            pipe.send(str)

    def Child2(self, pipe, child1_PID):
        """Realiza el encriptado rot13.
        args:
                -pipe: El pipe del hijo.
                -child1_PID: El número del pid del segundo hijo"""

        #Genero una señal para cerrar el hijo 2 cuando se escriba "stop".
        signal.signal(signal.SIGUSR1, self.Child2_Exit)

        while True:
            #Recibo el texto del pipe.
            text = pipe.recv()

            #Lo transformo a rot13
            text = encode(text, "rot_13")

            #Lo almaceno en queue.
            q.put(text)

            #Aviso por señal al hijo 1.
            os.kill(child1_PID, signal.SIGUSR1)
            
    def Child1_Print(self, s, f):
        """Printar en pantalla el archivo encriptado."""
        print(q.get())

    def Child2_Exit(self, s, f):
        """Cerrar el programa hijo 2."""
        exit(0)

#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: