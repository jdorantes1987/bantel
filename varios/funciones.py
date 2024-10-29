import pandas as pd

# Lee un archivo .xlsx
pagos = pd.read_excel("./varios/RepFormatoPago.xlsx")

print(pagos.info())
duplicados = pagos[pagos['mont_doc'].duplicated(keep=False)==True]
print('All duplicados por columna:\n', duplicados['mont_doc'].count())


# print('\n' * 2,
#       'Multiplica las cantidades de una columna por 1000, tambien se pueden realizar sumas, restas y divisiones')
# reconvert_x_1000 = pagos['mont_doc'].apply(lambda x: x * 1000)
# print(reconvert_x_1000)

# print('\n' * 2, 'Convierte a minúsculas las cadenas de una columna')
# def convertir_a_minusc(x):
#     # return x.upper()  # para Mayúsculas
#     return x.lower()


# convert_Minus = pagos['prov_des'].apply(convertir_a_minusc)
# print(convert_Minus)

# print('\n' * 2, 'Saber si un número es primo')


# def is_prime(n):
#     if n in [2, 3]:
#         return True
#     if (n == 1) or (n % 2 == 0):
#         return False
#     r = 3
#     while r * r <= n:
#         if n % r == 0:
#             return False
#         r += 2
#     return True


# print(is_prime(1), is_prime(109))

# print('\n' * 2, "Saber si un número es par")


# def evenodd(x):
#     if (x % 2 == 0):
#         print(x, "Es par", sep=' ')
#     else:
#         print(x, "Impar", sep=' ')


# evenodd(452)
# evenodd(11)

# print('\n' * 2, "Función con argumentos opcionales o por defecto")


# def myfun(x, y=50):
#     print("x: ", x)
#     print("y: ", y)


# myfun(10)

# print('\n' * 2,
#       "Función con argumentos de palabra clave, La idea es permitir que la persona que llama especifique el nombre del argumento con valores para que la persona que llama no necesite recordar el orden de los parámetros")


# def student(firstname, lastname):
#     print(firstname, lastname)


# student(firstname='Geeks', lastname='Practice')
# student(lastname='Practice', firstname='Geeks')

# print('\n' * 2,
#       "Función con Argumentos posicionales. Al cambiar la posición, o si olvida el orden de las posiciones, los valores se pueden usar en los lugares incorrectos")


# def nameage(name, age):
#     print("Hi, I am", name)
#     print("My age is ", age)


# print("Case-1:")
# nameage("Suraj", 27)

# print("\nCase-2:")
# nameage(27, "Suraj")
