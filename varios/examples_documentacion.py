from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")  # llega Terry
queue.append("Graham")
print(queue.popleft())
print(queue.popleft())

texto = "hola mundo"
print(dir(texto))
