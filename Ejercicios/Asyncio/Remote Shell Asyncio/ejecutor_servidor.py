# El servidor debe atender solicitudes utilizando asyncio.
# -p <port>: Puerto donde va a atender el servidor.
# -c p|t: Modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas.
# Si la opción es "-c t" generará hilos nuevos.

import click, socketserver, subprocess, pickle
import asyncio
import constants as cons

class Main():

    def __init__(self, port, host):
        self.__port = port
        self.__host = host

    async def handle(self, reader, writer):
        while True:
            # Obtener los datos.
            data = await reader.read(1024)
            message = pickle.loads(data)
            #addr = writer.get_extra_info('peername')

            # Desconectar al cliente
            if (message == "exit"):
                writer.write(pickle.dumps(cons.DISCONNECT))
                await writer.drain() # Enviar desconexión exitosa.
                writer.close()
                break

            # Comunicar datos.
            p = subprocess.Popen([f"{message}"], stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True,
                                universal_newlines = True)
            out, err = p.communicate()

            # Enviar datos al cliente.
            if (out != ""):
                send = cons.OK + out
                writer.write(pickle.dumps(send))
            elif (err != ""):
                send = cons.ERROR + err
                writer.write(pickle.dumps(send))
            else:
                except_error = cons.ERROR + cons.ERROR_SHELL + message
                writer.write(pickle.dumps(except_error))

            await writer.drain() # Enviar datos.

    # Estableciendo conexión.
    def main(self):
        if (self.__port != ""):
            if (self.__host != ""):
                asyncio.run(self.server())
            else:
                print(cons.ARGUMENT_ERROR, self.__conc)
                print(cons.HELP)
        else:
            print(cons.ARGUMENT_ERROR, self.__port)
            print(cons.HELP)

    async def server(self):
        
        # Crear el servidor.
        server = await asyncio.start_server(self.handle, self.__host, self.__port)
        print(cons.SRV_WORKING, self.__host, self.__port)
        
        # Runeamos el servidor.
        async with server:
            await server.serve_forever()

# Obtener parametros ingresado por el usuario.
@click.command()
@click.option("-p", "--port", help = "Server port")
@click.option("-h", "--host", help = "Server host")
def StartProgram(port, host):
    main = Main(port = port, host = host)
    main.main()

#Arrancar servidor
if __name__=="__main__":
    StartProgram()

#Bibliografia:
# Click example: https://www.geeksforgeeks.org/click-module-in-python-making-awesome-command-line-utilities/
# Shell commands: https://fedingo.com/python-run-shell-command-get-output/
