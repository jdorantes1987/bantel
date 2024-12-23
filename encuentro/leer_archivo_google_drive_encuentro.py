import numpy as np
import pandas as pd

ruta = "https://docs.google.com/spreadsheets/d/1BHI0mjidySPkKXD5Xz-c3JMI1yotG0Yt/export?format=xlsx"
df = pd.read_excel(ruta, sheet_name="SERVIDORES")
df = df[df["NOMBRE"].notnull()]  # FILTRO DE NO NULOS
print(df.info())
df["EDAD"] = df["EDAD"].fillna(0, inplace=False)

# Cambia el tipo de dato de la columna
df["EDAD"] = df["EDAD"].astype("Int64")
t_x_sex = df.groupby(["SEXO"])[["NOMBRE"]].count().reset_index()
t_x_sex.rename(columns={"NOMBRE": "CANTIDAD"}, inplace=True)
cta_sexo = t_x_sex["CANTIDAD"].sum()
t_x_sex["%_S_TOTAL"] = t_x_sex["CANTIDAD"] / cta_sexo
t_x_sex.loc["f"] = ["Total", t_x_sex["CANTIDAD"].sum(), t_x_sex["%_S_TOTAL"].sum()]
t_x_sex["%_S_TOTAL"] = t_x_sex["%_S_TOTAL"].apply("{:.2%}".format)
t_x_sex["CANTIDAD"] = t_x_sex["CANTIDAD"].apply(lambda x: int(round(x, 0)))
print("\n" * 2, "Participantes por:")
print(t_x_sex.reset_index(drop=True))

print("\n" * 2, "Finanzas")
fnzas = (
    df.groupby(["SEXO"])
    .agg({"MONTO ABONADO": "sum", "MONTO X ABONAR": "sum"})
    .reset_index()
)
# Convierte valores de la columna a positivos
fnzas["MONTO X ABONAR"] = fnzas["MONTO X ABONAR"].apply(lambda x: abs(x))
fnzas.loc["f"] = ["Total", fnzas["MONTO ABONADO"].sum(), fnzas["MONTO X ABONAR"].sum()]
fnzas["MONTO X ABONAR"] = fnzas["MONTO X ABONAR"].apply("${:,.2f}".format)
fnzas["MONTO ABONADO"] = fnzas["MONTO ABONADO"].apply("${:,.2f}".format)
print(fnzas.reset_index(drop=True))


print("\n" * 2, "Solventes de pago $30.00:")
pptes_solventes = df[df["MONTO ABONADO"] == 30.0]
for ind in pptes_solventes.index:
    print(
        pptes_solventes["NOMBRE"][ind],
        pptes_solventes["IGLESIA"][ind],
        pptes_solventes["RED"][ind],
        sep="--",
    )

x_igles = df.groupby(["IGLESIA"])[["NOMBRE"]].count().reset_index()
x_igles.rename(columns={"NOMBRE": "CANTIDAD"}, inplace=True)
x_igles_s = x_igles.sort_values(by=["CANTIDAD"], ascending=[False])
x_igles_s.loc["f"] = ["Total", x_igles_s["CANTIDAD"].sum()]
print("\n" * 2, "Enviados por:")
print(x_igles_s.reset_index(drop=True))

x_red = df.groupby(["RED"])[["NOMBRE"]].count().reset_index()
x_red.rename(columns={"NOMBRE": "CANTIDAD"}, inplace=True)
total_x_red_s = x_red.sort_values(by=["CANTIDAD"], ascending=[False])
total_x_red_s.loc["f"] = ["Total", total_x_red_s["CANTIDAD"].sum()]
print("\n" * 2, "Enviados por:")
print(total_x_red_s.reset_index(drop=True))

env_por = df.groupby(["ENVIADO POR", "RED"])[["NOMBRE"]].count().reset_index()
env_por.rename(columns={"NOMBRE": "CANTIDAD"}, inplace=True)
tep = env_por.sort_values(
    by=["RED", "CANTIDAD"], ascending=[True, False]
)  # Ordenar por varias columnas
print("\n" * 2, "Total:")
print(tep.reset_index(drop=True))

x_edo_civ = df.groupby(["ESTADO CIVIL"])[["NOMBRE"]].count().reset_index()
x_edo_civ.rename(columns={"NOMBRE": "CANTIDAD"}, inplace=True)
total_x_edo_civil_s = x_edo_civ.sort_values(by="CANTIDAD", ascending=False)
total_x_edo_civil_s.loc["f"] = ["Total", total_x_edo_civil_s["CANTIDAD"].sum()]
print("\n" * 2, "Total participantes por:")
print(total_x_edo_civil_s.reset_index(drop=True))

print("\n" * 2, "Edades:")
total_edades = df.groupby(["SEXO", "EDAD"])["EDAD"].aggregate(["count"])
total_edades.sort_values(by="EDAD", ascending=False)
total_edades.rename(columns={"count": "CANTIDAD"}, inplace=True)
print(total_edades)

print("\n" * 2, "Edad promedio por:")
prom_edades = (
    df.groupby(["SEXO"])["EDAD"].aggregate(["mean", "max", "min"]).reset_index()
)
prom_edades["mean"] = prom_edades["mean"].apply(lambda x: int(round(x, 0)))
prom_edades.rename(
    columns={"mean": "EDAD_PROMEDIO", "max": "EDAD_MAS_ALTA", "min": "EDAD_MAS_BAJA"},
    inplace=True,
)
prom_edades_sin_cero = prom_edades.replace(np.nan, 0)
print(prom_edades_sin_cero.reset_index(drop=True))
