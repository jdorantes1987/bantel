import pandas as pd
import numpy as np

print('DataFrame con estructura [{}]')
datos = [{'Nombres': 'Jackson Dorantes', 'Edades': 35}, {'Nombres': 'Mirtha Graterol', 'Edades': 42}, {'Nombres': 'Samira Dorantes', 'Edades': 16}, {'Nombres': 'Maria Fernanda Alarcon', 'Edades': 17}]
df2 = pd.DataFrame(datos)
print(df2)

print('\n' * 2, 'Numpy diccionario de Datos')
datos = np.array([[1, 28, 45], [35, 400, 74]])
df3 = pd.DataFrame(datos)
print(df3)

print('\n' * 2, 'Series')
s = pd.Series([1, 2, 3, 4, 90, 50, 64, 87, 100])
print(s)

datos = {
    'Nombres': ['Jackson Dorantes', 'Mirtha Graterol', 'Samira Dorantes', 'Maria Fernanda Alarcon'],
    'Edades': [35, 42, 16, 17]
}

print('\n' * 2, 'DataFrame con estructura {[]} la más usada')
df = pd.DataFrame(datos)
print(df)


