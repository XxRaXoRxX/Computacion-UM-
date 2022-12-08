# Cosas que mejorar:
## Client:
- Por parte del cliente se puede agregar mas opciones, como tamaño de imagen, la seed que quieran utilizar.
- Tener mas opciones como img2img, entre otros.
- Una mejor interfaz utilizando alguna página web.
## Server:
- Mejor sistema de almacenamiento de los datos, mediante uso de MYSQL, pudiendo filtrar búsquedas y devolviendo mejores imágenes.
## Redis:
- Que el usuario pueda cambiar el puerto mas fácilmente, y no tenga que entrar al **boot** y al código para cambiarlo.
## Celery:
- Responder a los cambios planteados por el usuario, según cambio de seed, tamaño de imagen, etc. 
- Que el usuario tenga un **config** con el tamaño de la imagen por default de imagen a crear y la conexión con el Redis. Actualmente esta muy hardcodeado el tema de la configuración.
