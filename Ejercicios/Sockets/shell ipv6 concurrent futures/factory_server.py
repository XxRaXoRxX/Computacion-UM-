import socketserver, subprocess, pickle, socket
from threading import Thread
import ipv4_server as ipv4
import ipv6_server as ipv6
import constants as cons

# Clase generador del shell en el server.
class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Obtener los datos.
        while True:
            data = self.request.recv(1024) # Se rompe al mandar muchos datos, la solución sería agregar mayor rango de bytes recibidos o mandar datos por partes.
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

class FactoryServer():

    def get_server(self, inet, host, port, concurrency):
        service = self.__get_service(inet, host, port, concurrency)
        print(cons.SRV_WORKING, host, ":" , port)
        return Thread(target = self.__server, args = (service,))

    def __server(self, service):
        service.serve_forever()

    def __get_service(self, inet, host, port, concurrency):

        # Obtener concurrencia
        con = self.__get_concurrency(concurrency)
        inet = self.__get_inet(inet)
        con_inet = con + "_" + inet

        match con_inet:
            case "process_ipv6":
                return ipv6.ForkingServer((host,port), RequestHandler)
            case "process_ipv4":
                return ipv4.ForkingServer((host,port), RequestHandler)
            case "thread_ipv6":
                return ipv6.ThreadedServer((host,port), RequestHandler)
            case "thread_ipv4":
                return ipv6.ThreadedServer((host,port), RequestHandler)
            case _:
                return "ERROR, socketserver or concurrency not found: " + con_inet

    def __get_inet(self, inet):
        match inet:
            case socket.AF_INET:
                return "ipv4"
            case socket.AF_INET6:
                return "ipv6"
            case _:
                return "Error, socketserver inet not found: " + str(inet)

    def __get_concurrency(self, concurrency):
        match concurrency:
            case "p":
                return "process"
            case  "t":
                return "thread"
            case _:
                return "Error, concurrency is invalid: " + str(concurrency)