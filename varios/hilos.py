import threading


def gfg():
    print("GeeksforGeeks, hilo ejecutado.\n")


timer = threading.Timer(10.0, gfg)
timer.start()
print("Exit\n")
