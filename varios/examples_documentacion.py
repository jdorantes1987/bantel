empleados = [
    {"nombre": "jackson", "apellido": "dorantes", "edad": 38, "salario": 3000},
    {"nombre": "juan", "apellido": "perez", "edad": 25, "salario": 800},
    {"nombre": "maria", "apellido": "gomez", "edad": 30, "salario": 1200},
    {"nombre": "luis", "apellido": "ramirez", "edad": 35, "salario": 2800},
    {"nombre": "pedro", "apellido": "garcia", "edad": 40, "salario": 1200},
]

mayores_salarios = filter(lambda x: x["salario"] < 2000, empleados)
print(list(mayores_salarios))

lista = ["mesa", "silla", "cama", "sofa", "sillon"]

lista_mayusculas = map(lambda x: x.upper(), lista)
print(list(lista_mayusculas))
