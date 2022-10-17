# Explicación del codigo chained.py

### Inicio del Código

1. En primer lugar se ejecuta el código:
``` if  __name__  ==  "__main__": ```
2. Luego realiza un valor random mediante una seed.
``` random.seed(418) ```
3. Luego al **import sys** verifica si solo se le paso un argumento al ejecutar el código, es decir el nombre del código, en este caso **chained.py** si solo se ejecuto mediante **"python3 chained.py"** y no se paso nada mas, considera que tiene solo un argumento y genera una tabla llamado **args** con tres valores **"[1, 2, 3]"**, en caso de haber paso algun argumento al iniciar el codigo, como por ejemplo **"python3 chained.py 5 8"**, en este caso al pasar dos valores más por argumento, los mete a la tabla **args** pero en este caso como mapeo y transformado esos valores a **enteros** y los muestra por consola.
```
args  = [1, 2, 3] if  len(sys.argv) ==  1  else  list(map(int, sys.argv[1:]))
print(args)
```
4.  Genera una variable con el tiempo actual del sistema, luego inicia la corrutina **"main(*args)"** por **asyncio.run()** y se les pasa los argumentos generados o ingresados por el usuario, y al final se genera otra variable con el valor de cuanto tiempo tardo en realizar la tarea de ejecución del main, y muestra este tiempo en pantalla.
```
start  = time.perf_counter()
asyncio.run(main(*args))
end  = time.perf_counter() -  start
print(f"Program finished in {end:0.2f} seconds.")
```
5. En la corrutina del **main(*args)**, lo que se hace es un **gather**, transformando las corrutinas del **chain(n)** en tareas, según tantos valores tengamos en la lista, enviando esos valores como parámetros dentro del **chain(n)**, y ejecutando estas tareas en bucle, saliendo y entrando en cada una según entradas/salidas tenga cada tarea.
```
async  def  main(*args):
	await asyncio.gather(*(chain(n) for  n  in  args))
```
6. En la corrutina del **chain(n)**, recibe un valor como argumento, y genera una variable **start** según el tiempo actual del sistema y muestra en pantalla _"lanzando primera"_ y ejecuta la corrutina **primera(n)**
```
async  def  chain(n:  int) ->  None:
	start  = time.perf_counter()
	print("Lanzando primera")
	prim  =  await  primera(n)
```
- En la corrutina del **primera(n)**, recibe un valor entero como parametro, y genera un valor _**random** entre **0 y 10**_ y lo almacena en una variable **i**, muestra este valor random por mensaje y ejecuta una corrutina de espera de **i** segundos.
Luego de esperar esos segundos, almacena en una variable **"result{n}-A"** mostrandolo por pantalla y retornando este valor a la variable **prim**.
```
async  def  primera(n:  int) ->  str:
	i  = random.randint(0, 10)
	print(f"primera({n}) esperando {i}s.")
	await asyncio.sleep(i)
	result  =  f"result{n}-A"
	print(f"Retornando primera({n}) == {result}.")
	return  result
```
Una vez retornado un valor por la corrutina primera, se muestra en consola _"lanzando segunda"_ y se ejecuta la corrutina segunda, mandando como parametro el **número ingresado como parametro** en la corrutina **chain(n)** y el valor que obtuvimos antes con la variable **prim** (**_ver explicación de corrutina en el punto debajo_**)
Genera una fecha de finalización, con el tiempo actual y restando el tiempo de inicio y lo muestro en pantalla, con el resultado del retorno de la segunda corrutina almacenado en **segu**.
```
	print("Lanzando Segunda")
	segu  =  await  segunda(n, prim)
	end  = time.perf_counter() -  start
	print(f"-->Encadenado result{n} => {segu} (tomó {end:0.2f} s).")
```
- En la corrutina del **segunda(n, arg)**, obtiene dos valores como parametros, tanto **n** como valor del **chain(n)**, ademas de **arg** que pasa como argumento lo que retorna la corrutina anterior llamado **primera(n)**
Genera un número **random entre 0 y 10** y lo almacenan en una variable **i**, muestra un mensaje diciendo que espera esos **i** segundos y inicia una corrutina de espera con ese valor **i** como parametro.
Al final de la espera almacena **"result{n}-B => {arg]"** lo muestra por pantalla y lo retorna.
7. Y el *gather* es el encargado de ir finalizando estas tareas en orden aleatorio, porque la espera en cada tarea es aleatorio mediante un **_random.randint()_** y mostrandose en pantalla.

### Consideraciones

Algo a tener en cuenta, es que el **gather** las tarea las genera en orden según las agregamos en la cola, pero estas se van ejecutando en ciclo, según no este ejecutando la corrutina **sleep**, por lo que va a ir ejecutando y finalizando de la cola de manera aleatoria, según el contador de cada uno, mostrando en que corrutina se encuentra actualmente, si en la **"primera"** o **"segunda"**. Y al finalizar de ejecutar todas las tareas, sale del **gather**, printea que el programa finalizo con el contador y finaliza el programa. Todo esto ejecutándose en un solo hilo mediante el **asyncio** de manera concurrente.