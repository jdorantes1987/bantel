import datetime
import threading

from banco_central.bcv_estadisticas_tasas import actulizar_file_tasas


def my_thread():
    # Código que deseas ejecutar en el hilo
    actulizar_file_tasas()
    print("¡hilo ejecutado!")


# Hora a la que deseas que se ejecute el hilo
hora_ejecucion = datetime.datetime.now().replace(
    hour=16, minute=10, second=0, microsecond=0
)

# Calcula la cantidad de segundos hasta la hora de ejecución
segundos_espera = (hora_ejecucion - datetime.datetime.now()).total_seconds()
# Programa la ejecución del hilo en la hora especificada
t = threading.Timer(segundos_espera, my_thread)
t.start()
# Espera hasta que finalice la ejecución del método
t.join()
