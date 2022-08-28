# El servidor debe atender solicitudes utilizando sockets de alto nivel con serversocket.
# -p <port>: Puerto donde va a atender el servidor.
# -c p|t: Modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas.
# Si la opción es "-c t" generará hilos nuevos.

import click, socketserver, subprocess
import constants as cons

class Main():

    def __init__(self, port, conc):
        self.__port = port
        self.__conc = conc

    # Clase generador del shell en el server.
    class RequestHandler(socketserver.BaseRequestHandler):
        def handle(self):
            # Obtener los datos.
            while True:
                data = self.request.recv(1024)
                data = data.decode()
                new_data = data.split()

                # Comunicar datos.
                p = subprocess.Popen(new_data, stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE,
                                        shell = True)
                out, err = p.communicate()

                # Enviar datos al cliente.
                if (out != ""):
                    send = cons.OK + cons.LIST + out.decode()
                    send = send.encode(cons.ENCODE)
                    self.request.send(send)
                elif (err != ""):
                    send = cons.ERROR + cons.LIST + err.decode()
                    send = send.encode(cons.ENCODE)
                    self.request.send(send)
                else:
                    except_error = cons.ERROR + cons.LIST + cons.ERROR_SHELL + data
                    except_error = except_error.encode(cons.ENCODE)
                    self.request.send(except_error)

    # Clase generador de hilos y procesos.
    class ThreadedServer(socketserver.ThreadingMixIn,
                        socketserver.TCPServer):
        pass
    class ForkingServer(socketserver.ForkingMixIn,
                        socketserver.TCPServer):
        pass

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

        if (self.__conc == "t"):
            server = self.ForkingServer(address, self.RequestHandler)
        else:
            server = self.ThreadedServer(address, self.RequestHandler)

        print(cons.SRV_WORKING, cons.LOCALHOST, self.__port)
        server.serve_forever()

# Obtener parametros ingresado por el usuario.
@click.command()
@click.option("-p", help = "Server port")
@click.option("-c", help = "Concurrency mode: t(threading) or p(process)")
def StartProgram(p, c):
    main = Main(port = p, conc = c)
    main.Main()

#Arrancar servidor
if __name__=="__main__":
    StartProgram()

#Bibliografia:
# Click example: https://www.geeksforgeeks.org/click-module-in-python-making-awesome-command-line-utilities/
# Shell commands: https://fedingo.com/python-run-shell-command-get-output/