def suma(a, b,  c,  / , d, e,  *, f,  g):
    return a+b+c+d+e+f+g

print(suma(1, 2, 3, 4, 5, f=6, g=7))

def sumar(*args):
    return sum(args)

print(sumar(1, 2, 3))

lista = [1, 2, 3]
tupla = (4, 5, 6)
diccionario = {7: 'siete', 8: 'ocho', 9: 'nueve'}

print(sumar(*lista, *tupla, *diccionario))

def fun(**kwargs):
       print(kwargs)
       suma = sum(kwargs.values())
       print(suma)

fun(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9)

