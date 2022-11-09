# Parte del Celery:
# La funcion_calculo podrá ser una de las siguientes:
# -raiz: calcula la raíz cuadrada del elemento.
# -pot: calcula la potencia del elemento elevado a si mismo.
# -log: calcula el logaritmo decimal de cada elemento.
import math
from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1', backend='redis://127.0.0.1')

@app.task
def Root(value):
    """Calcula la raíz cuadrada del elemento.

    args:
            -value: Valor a realizar el calculo."""

    #newMatrix = []
    #for v in value:
    #    newMatrix.append(math.sqrt(v))
    #return newMatrix

    new_matrix = map(math.sqrt, value)

    return list(new_matrix)

@app.task
def Pot(value):
    """Calcula la potencia del elemento elevado a si mismo.

    args:
            -value: Valor a realizar el calculo."""

    #newMatrix = []
    #for v in value:
    #    newMatrix.append(math.pow(v, v))
    #return newMatrix

    # Genera una lista con los valores de la potencia, en este caso 2.
    pot_list = [2]*len(value)
    new_matrix = map(math.pow, value, pot_list)

    return list(new_matrix)

@app.task
def Log(value):
    """Calcula el logaritmo decimal de cada elemento.

    args:
            -value: Valor a realizar el calculo."""

    #newMatrix = []
    #for v in value:
    #    newMatrix.append(math.log(v))
    #return newMatrix

    new_matrix = map(math.log, value)

    return list(new_matrix)

# Esto no es necesario, en la versión actual de celery se startea automatico.
#if __name__ == "__main__":
#    app.start()

# Para ejecutar Celery:
# celery -A tasks worker --loglevel=INFO -c4
# Para ejecutar Rudist:
# docker run -p 6379:6379 redis