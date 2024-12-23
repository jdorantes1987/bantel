import datetime

import pandas as pd

cadena = "El resultado de sumar {id_Mov} y {descr} es".format(
    id_Mov="MB20231214", descr="Prueba"
)

hoy = datetime.datetime.now()

t = datetime.time(hoy.hour, hoy.minute, hoy.second)
d = datetime.date.today()

dt = datetime.datetime.combine(d, t)
print("dt:", dt)

d = dict({"A": [1, 2, 3], "B": [4, 5, 6]})
df = pd.DataFrame(d)
df["C"] = [7, 8, 9]
dfs = df.set_axis(["1ero", "2do", "3ero"], axis="index")
print(dfs)
print(dfs.describe())

print(df["A"][1:3])

df["D"] = [10, 11, 12]
print(df)

print(df[["C", "A"]])

print(df.loc[0:1])

lst = [
    ["Geeks", "For", "Geeks", "is", "portal", "for", "Geeks", "l"],
    ["Jackson", "Jhoan", "Mirtha", "Alejandro", "Samira", "Mafer"],
]
lst2 = ["Wilmer", "Luis"]

lst[1][6:6] = lst2

# Calling DataFrame constructor on list
df = pd.DataFrame(lst)
print(df)
"""
sum_fin_mes = celulas['Monto Bs'].resample('M').sum()  # BM para sumar todos los días hábiles del mes y M para todos los dias del mes
print(sum_fin_mes.to_string())
print('fecha max:', celulas.index.min())
print('diferencia entre dia inicial y dia final:', (celulas.index.max() - celulas.index.min()).days)
"""

import pandas as pd
import plotly.figure_factory as ff

df = pd.DataFrame()
df["date"] = ["2016-04-01", "2016-04-02", "2016-04-03", "2016-04-03", "2016-04-03"]
df["calories"] = [2200, 2100, 1500, 2200, 2100]
df["sleep hours"] = [8, 7.5, 8.2, 3, 4]
df["gym"] = [True, False, False, True, True]


dfx = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})
dfx["A_next"] = dfx["A"].shift(-1)
dfx["B_next"] = dfx["B"].shift(-1)
print(dfx)
