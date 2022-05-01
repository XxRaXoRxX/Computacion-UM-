# Procesos pipe.
# Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
# - El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
# - El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
# - Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
# - El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.

import os
import argparse as arg

class Constants():
    ERROR = "Valores ingresados incorrectos. Ingresa -h para mas información."
    CONTENIDO_ARCHIVO = """HOLA MUNDO
    que tal
    este es un archivo
    de ejemplo.
    """

class Main():

    def main(self):
        args = self.ArgumentsConfig()
        cons = Constants()

        if (args.file):
            self.Fork(file = args.file, constants = cons)
        else:
            print(cons.ERROR)


    def ArgumentsConfig(self):
        """Genero el ArgParse y sus argumentos.

        return:
                -arguments: Devuelve los argumentos creados en el argparse.
        """

        # Generas el parser con una descripción
        parser = arg.ArgumentParser(description="Generar procesos hijos y invierten el texto del archivo, todo mediante os.pipe().")

        # Ingreso de argumentos
        parser.add_argument("-f", "--file", type=str, help="Archivo de texto que se utiliza para obtener las lineas de texto.")

        # Obtener lista de argumentos en args.
        return parser.parse_args()

    
    def Fork(self, file, constants):
        """Realizo el forkeo y genero los hijos

        ags:
                -file: Ubicación del archivo a invertir el texto.
                -constants: Lista de constantes.
        """

        # Creado un archivo en caso de no existir, sino lo cargo
        if not os.path.exists(file):
            archive = open(file, "w")
            archive.write(constants.CONTENIDO_ARCHIVO)
            print("Sin archivo en path, creado nuevo archivo de ejemplo en:", file)
            archive.close()

        archive = open(file, "r")

        lines = archive.readlines()

        if (len(lines) < 1):
            print("El archivo esta vacio. Cancelando...")
            return

        #Creación de Pipes.
        r_send, w_send = os.pipe()
        r_get, w_get = os.pipe()

        for i in range(len(lines)):
            #Envio linea de texto al hijo.
            os.write(w_send, lines[i].encode())

            # Genero los hijos
            child_pid = os.fork()
            if (child_pid == 0):

                #Cerrando pipes innecesarios.
                os.close(w_send)
                os.close(r_get)

                #codigo del hijo
                self.Inversor(read = r_send, write = w_get)

                os._exit(0)
        
        os.close(w_send)

        #Cierro el archivo con texto a editar.
        archive.close()

        # Esperar hasta que el ultimo proceso hijo finalice.
        pid, status = os.waitpid(child_pid, 0)

        #Printea en pantalla el texto invertido
        print("Archivo invertido:")
        print("")
        print(os.read(r_get, 100).decode())
        os.close(r_get)
        os.close(w_get)

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")

    def Inversor(self, read, write):
        """Realiza la suma de pares para cada proceso.

        args:
                -read: Lectura del pipe
                -write: Escritura del pipe
        """

        #Obtener lectura del pipe
        text = os.read(read, 100)
        #Decodear los bites.
        text = text.decode()

        #Quito el /n del texto
        text = text[:-2]
        #Invertir letras.
        text = text[::-1]
        #Agrego un /n al final texto
        text += "\n"

        #Enviar texto al padre.
        os.write(write, text.encode())
        #Cerrar el write del pipe
        os.close(write)
        #Cerrando el read del pipe
        os.close(read)
        
#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: