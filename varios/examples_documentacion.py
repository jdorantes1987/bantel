x=1
def prueba_variables(x=1, y=10):
    primero = x
    segundo = y


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

print(suma.__code__.co_varnames)

def fun(a, L=None):
    if L is None:
       L=[]
    L.append(a)
    print(L)


print(f"Defaults : ", fun.__defaults__)    
fun(1)
print(f"Defaults : ", fun.__defaults__)    
fun(98)
print(f"Defaults : ", fun.__defaults__)    
fun(0, L=[1, 2, 8])






