# Comandos GNU/Linux en una computadora remota.
# El cliente debera darle al usuario un prompt en el que pueda ejecutar comandos de la shell.
# Esos comandos seran enviados al servidor, el servidor los ejecutará, y retornará al cliente.
# El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que
# se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.
# El cliente debe poder recibir los siguientes opciones:
# -h <host>: dirección IP o nombre del servidor al que conectarse.
# -p <port>: número de puerto del servidor.

import click, socket
import constants as cons

class Main():

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def Main(self):
        if (self.__host != ""):
            if (self.__port != ""):
                self.Client()
            else:
                print(cons.ARGUMENT_ERROR, self.__port)
                print(cons.HELP)
        else:
            print(cons.ARGUMENT_ERROR, self.__host)
            print(cons.HELP)

    def Client(self):
        # Conectarse al server.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__host, int(self.__port)))
        print(f"{cons.SERVER_CONNECT} {self.__host}:{self.__port}")

        print(cons.EXIT) # Printear como salir del shell.
        while True:
            answer = input(cons.INSERT)
            # Si ingresa exit se sale del shell.
            if (answer == "exit"):
                print(cons.DISCONNECT)
                s.close()
                return

            s.send(answer.encode(cons.ENCODE))
            recv = s.recv(1024)
            recv = recv.decode()
            recv = recv.split(cons.LIST)
            print(recv[0])
            print(recv[1])
            

# Obtener parametros ingresado por el usuario.
@click.command()
@click.option("-h", help = "Server host")
@click.option("-p", help = "Server port")
def StartProgram(h, p):
    main = Main(host = h, port = p)
    main.Main()

#Arrancar cliente
if __name__=="__main__":
    StartProgram()

#Bibliografia: