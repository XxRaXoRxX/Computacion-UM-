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

        pipe_read = []
        pipe_write = []

        for i in range(len(lines)):
            
            #Creación de pipes
            r, w = os.pipe()
            pipe_write.append(w)
            pipe_read.append(r)

            # Genero los hijos
            child_pid = os.fork()
            if (child_pid == 0):
                #codigo del hijo
                self.Inversor(read = pipe_read[i], write = pipe_write[i])

                os._exit(0)

        # Codigo del padre
        # Escribir los textos a los hijos
        for i in range(len(lines)):
            os.write(pipe_write[i], str.encode(lines[i]))

        archive.close()

        # Esperar hasta que el ultimo proceso hijo finalice.
        pid, status = os.waitpid(child_pid, 0)

        # Leer los textos de los hijos y escribirlo en el archivo
        #archive = open(file, "w")
        #for i in range(len(lines)):
        #    read = os.read(pipe_read[i], 100)
        #
        #    #Quitar el /n en la primera escritura
        #    if (i == 0):
        #        read = read.decode()
        #        read = read[2:]
        #        archive.write(read)
        #        continue
        #
        #    archive.write(read.decode())
        #print(archive.read())

        # Se cierra el archivo al editarlo arriba
        # archive.close()

        #Printea en pantalla el texto invertido
        print("Archivo invertido:")
        print("")
        for i in range(len(lines)):
            read = os.read(pipe_read[i], 100)
            read = read.decode()
            read = read[2:]
            print(read)

        for read in pipe_read:
            os.close(read)

        for write in pipe_write:
            os.close(write)

        #codigo del padre, todos los hijos finalizaron!
        print("Todos los procesos hijos finalizaron. Cerrando...")


    def Inversor(self, read, write):
        """Realiza la suma de pares para cada proceso.

        args:
                -read: Lectura del pipe
                -write: Escritura del pipe
        """

        #Leer el archivo en el pipe
        text = os.read(read, 100)
        #Cerrar el read del pipe
        os.close(read)

        #Leer el archivo de byte.
        text = text.decode()
        #Invertir letras.
        text = text[::-1]

        #Enviar texto al padre.
        os.write(write, str.encode(text))
        #Cerrar el write del pipe
        os.close(write)
        
#Arrancar ejemplo
main = Main()
main.main()

#Bibliografia: