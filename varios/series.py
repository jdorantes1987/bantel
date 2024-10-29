import pandas as pd
import numpy as np

an_array = np.arange(1, 10, 2)

ser = pd.Series(an_array)
print(ser)
ser2 = pd.Series(an_array, index=['1ro', '2do', '3er', '4to', '5to'])
print(ser2)

print(ser2.index)
print(ser2.values)

a_dict = {'1ro': 1, '2do': 3, '3er': 5, '4to': 7, '5to': 8}
ser3 = pd.Series(a_dict)
print(ser3)

ser4 = pd.Series(10.2, index=['1ro', '2do', '3er'])
print(ser4)

# Seleccionar un solo elemento de la serie

print(ser3[3])
print(ser3['3er'])

# Seleccionar un elementos de la serie notacion slice:
print(ser3[2:5])

# Seleccionar a traves de varios indices
print(ser3[[0, 2, -1]])

# Uso de condiciones y operadores boleanos
print(ser3[ser3 > 3]) #5, 7, 8

print(ser3[np.logical_and(ser3 > 5, ser3 < 8)]) #7

# Asignara valores (mutabilidad de las series)

ser3[2:] = 100
print(ser3)

# Operaciones Matemáticas
print(ser3 + ser3)
print(ser3 / 2)

print(ser3.mean())
print(np.mean(ser3))

