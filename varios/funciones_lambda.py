import pandas as pd

pagos = pd.read_excel("RepFormatoPago.xlsx")

print("\n" * 2, "Funcion lambda ejemplo 1")
calc = lambda num: "Número par" if num % 2 == 0 else "Número impar"
print(calc(15))

print("\n" * 2, "Funcion lambda ejemplo 2")
promedio = lambda n1, n2: (n1 + n2) / 2
print("promedio:", promedio(20, 10), sep=" ")

print("\n" * 2, "Funcion lambda aplicada a DataFrame")
pagos["mont_cob_reconv"] = pagos["mont_cob"].apply(lambda x: x * 1000)
print(pagos["mont_cob_reconv"])

print("\n" * 2, "Convertir valores de una columna a Mayúsculas usando funcion lambda")
convert_Mayus = pagos["prov_des"].apply(lambda s: s.upper())
print(convert_Mayus)

print("\n" * 2, 'Saber si un valor en una columna es mayor a "n" usando funcion lambda')
pagos["mont_cob_mayores_a_1000"] = pagos["mont_cob"].apply(lambda s: s > 1000)
print(pagos["mont_cob_mayores_a_1000"].head())
