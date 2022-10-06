# El servidor debe atender solicitudes utilizando sockets de alto nivel con serversocket.
# -p <port>: Puerto donde va a atender el servidor.
# -c p|t: Modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas.
# Si la opción es "-c t" generará hilos nuevos.

import click, socket, subprocess, pickle
import constants as cons
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, as_completed

class Main():

    def __init__(self, port, conc):
        self.__port = port
        self.__conc = conc

    # Clase generador del shell en el server.
    def handle(self, socket, address):
        # Obtener los datos.
        print(address, cons.CONNECT)

        while True:
            data = socket.recv(1024) # Se rompe al mandar muchos datos, la solución sería agregar mayor rango de bytes recibidos o mandar datos por partes.
            decode = pickle.loads(data)

            # Desconectar al cliente
            if (decode == "exit"):
                encode = pickle.dumps(cons.DISCONNECT)
                socket.send(encode)
                break

            # Comunicar datos.
            p = subprocess.Popen([f"{decode}"], stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True,
                                universal_newlines = True)
            out, err = p.communicate()

            # Enviar datos al cliente.
            if (out != ""):
                send = cons.OK + out
                encode = pickle.dumps(send)
                socket.send(encode)
            elif (err != ""):
                send = cons.ERROR + err
                send = pickle.dumps(send)
                socket.send(send)
            else:
                except_error = cons.ERROR + cons.ERROR_SHELL + decode
                except_error = pickle.dumps(except_error)
                socket.send(except_error)

    # Estableciendo conexión.
    def Main(self):
        if (self.__port != ""):
            if (self.__conc == "t" or self.__conc == "p"):
                self.Server()
            else:
                print(cons.ARGUMENT_ERROR, self.__conc)
                print(cons.HELP)
        else:
            print(cons.ARGUMENT_ERROR, self.__port)
            print(cons.HELP)

    def Server(self):
        address = (cons.LOCALHOST, int(self.__port))

        # Abre hilos o aplicaciones segun commando -c
        if (self.__conc == "p"):
            #Creación del pool por procesos
            executor = ProcessPoolExecutor(max_workers = 10)
        else:
            #Creación del pool por hilos
            executor = ThreadPoolExecutor(max_workers = 10)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #... tenemos un pool "executor", y un socket que se llama "s"
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(address)
            s.listen(1)

            print(cons.SRV_WORKING, cons.LOCALHOST, self.__port)
            
            while True:
                s2, addr = s.accept()
                result = executor.submit(self.handle, s2, addr)
                #s2.close()

# Obtener parametros ingresado por el usuario.
@click.command()
@click.option("-p", "--port", help = "Server port")
@click.option("-c", "--concurrency", help = "Concurrency mode: t(threading) or p(process)")
def StartProgram(port, concurrency):
    main = Main(port = port, conc = concurrency)
    main.Main()

#Arrancar servidor
if __name__=="__main__":
    StartProgram()

#Bibliografia:
# Click example: https://www.geeksforgeeks.org/click-module-in-python-making-awesome-command-line-utilities/
# Shell commands: https://fedingo.com/python-run-shell-command-get-output/
