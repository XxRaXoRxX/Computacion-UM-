# Diseño del Sistema:
## Client:
La idea del cliente es que no tenga que instalar nada, sino que ejecute el **boot** y listo, agregue un prompt y obtenga la imagen, es por eso que no hay requerimientos ni ningún **install** en la carpeta. De todas formas, lamentablemente por el uso del lenguaje Python va a tener que instalar Python en su máquina. Que no es difícil pero ya es instalar algo.

## Server:
El servidor facilita la comunicación entre el cliente y el Celery, la idea principal del servidor, es evitar el uso intensivo del Celery por prompts repetidos, lo que hace el servidor es almacenar las imagenes mediante su prompt, y en caso de que el cliente pida un prompt almacenado en la base de datos, se lo devuelva al instante el servidor y no tenga que mandarlo al Redis y Celery donde tenga que trabajar por una imagen ya creada anteriormente.

## Redis y Celery:
El Redis es el encargado de enviar la tareas a los Workers (Celery), y estos deben recibir el prompt y realizar el trabajo y devolver la imagen, se planteo Celery, para poder aumentar la capacidad de Workers sin problemas en caso de tener muchos clientes que pidan imágenes, además de dejar al cliente fuera del trabajo duro y que no note eso, sino que los Workers con su poder de computo hagan el trabajo.
