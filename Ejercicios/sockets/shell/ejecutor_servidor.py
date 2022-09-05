# El servidor debe atender solicitudes utilizando sockets de alto nivel con serversocket.
# -p <port>: Puerto donde va a atender el servidor.
# -c p|t: Modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas.
# Si la opción es "-c t" generará hilos nuevos.

import click, socketserver, subprocess, pickle
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
                decode = pickle.loads(data)

                # Desconectar al cliente
                if (decode == "exit"):
                    encode = pickle.dumps(cons.DISCONNECT)
                    self.request.send(encode)
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
                    self.request.send(encode)
                elif (err != ""):
                    send = cons.ERROR + err
                    send = pickle.dumps(send)
                    self.request.send(send)
                else:
                    except_error = cons.ERROR + cons.ERROR_SHELL + decode
                    except_error = pickle.dumps(except_error)
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

        # Abre hilos o aplicaciones segun commando -c
        if (self.__conc == "t"):
            server = self.ForkingServer(address, self.RequestHandler)
        else:
            server = self.ThreadedServer(address, self.RequestHandler)

        # Liberar puertos al desconectarse.
        server.allow_reuse_address = True

        print(cons.SRV_WORKING, cons.LOCALHOST, self.__port)
        server.serve_forever()

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