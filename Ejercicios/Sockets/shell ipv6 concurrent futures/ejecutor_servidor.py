# El servidor debe atender solicitudes utilizando sockets de alto nivel con serversocket. Implementando Factory Method
# -p <port>: Puerto donde va a atender el servidor.
# -c p|t: Modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas.
# Si la opción es "-c t" generará hilos nuevos.

import click, socket
import constants as cons
from factory_server import FactoryServer

class Main():

    def __init__(self, port, conc):
        self.__port = port
        self.__conc = conc

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
        # Obtener las direcciones IPV4 y IPV6 segun puerto del pc.
        directions = socket.getaddrinfo("localhost", self.__port, socket.AF_UNSPEC, socket.SOCK_STREAM)

        # Genero la lista de servidores runneando en segundo plano mediante hilos IPV4 y IPV6.
        factory = FactoryServer()
        ips = []
        for dir in directions:
            inet, sock, n, m, address = dir
            ips.append(factory.get_server(inet = inet, 
                                          host = address[0],
                                          port = address[1], 
                                          concurrency = self.__conc))
        for ip in ips:
            ip.start()

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
