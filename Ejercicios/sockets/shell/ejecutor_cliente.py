# Comandos GNU/Linux en una computadora remota.
# El cliente debera darle al usuario un prompt en el que pueda ejecutar comandos de la shell.
# Esos comandos seran enviados al servidor, el servidor los ejecutará, y retornará al cliente.
# El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que
# se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.
# El cliente debe poder recibir los siguientes opciones:
# -h <host>: dirección IP o nombre del servidor al que conectarse.
# -p <port>: número de puerto del servidor.

import click, socket, pickle
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
            # Pregunta al usuario
            answer = input(cons.INSERT)

            # Envio de datos al servidor
            encode = pickle.dumps(answer)
            s.send(encode)
            recv = s.recv(1024)
            decode = pickle.loads(recv)
            print(decode)

            # Desconectarse cuando recibe dato desconexión
            if (decode == cons.DISCONNECT):
                break
            

# Obtener parametros ingresado por el usuario.
@click.command()
@click.option("-h", "--host", help = "Server host")
@click.option("-p", "--port", help = "Server port")
def StartProgram(host, port):
    main = Main(host = host, port = port)
    main.Main()

#Arrancar cliente
if __name__=="__main__":
    StartProgram()

#Bibliografia: