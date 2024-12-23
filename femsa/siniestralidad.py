import pandas as pd

ruta_file = "INCURRIDO AL CIERRE DE MES SEPTIEMBRE ADM $.xlsx"
archivo = pd.read_excel(ruta_file)
casos_por_edo = (
    archivo.groupby("ESTADO")
    .agg({"MONTO_PAGADO": ["count", "sum"]})
    .reset_index(names=[("DESCRIPCION", "Estado")])
    .reset_index(drop=True)
)

# Accede al grupo o nivel contenidos en la columna formada de una tupla o tuple
m_pagado = casos_por_edo[("MONTO_PAGADO", "sum")].sum()
casos = casos_por_edo[("MONTO_PAGADO", "count")].sum()
casos_por_edo["Porcent"] = casos_por_edo.apply(
    lambda x: x[("MONTO_PAGADO", "sum")] / m_pagado, axis=1
)
casos_por_edo["Porcent"] = casos_por_edo["Porcent"].apply("{:.2%}".format)
# ***Casos por Estado***
print(casos_por_edo)

casos_por_tip_serv = archivo.groupby("TIPO_SERVICIO").agg(
    {"MONTO_PAGADO": ["count", "sum"]}
)
l_campos = ["Cantidad", "Ptj_Cantidad", "Pagado", "Ptj_Pag"]
casos_por_tip_serv["Ptj_Cantidad"] = casos_por_tip_serv.apply(
    lambda x: x[("MONTO_PAGADO", "count")] / casos, axis=1
)
casos_por_tip_serv["Ptj_Cantidad"] = casos_por_tip_serv["Ptj_Cantidad"].apply(
    "{:.2%}".format
)
casos_por_tip_serv["Ptj_Pag"] = casos_por_tip_serv.apply(
    lambda x: x[("MONTO_PAGADO", "sum")] / m_pagado, axis=1
)
casos_por_tip_serv["Ptj_Pag"] = casos_por_tip_serv["Ptj_Pag"].apply("{:.2%}".format)
casos_por_tip_serv["Cantidad"] = casos_por_tip_serv.apply(
    lambda x: x[("MONTO_PAGADO", "count")], axis=1
)
casos_por_tip_serv["Pagado"] = casos_por_tip_serv.apply(
    lambda x: x[("MONTO_PAGADO", "sum")], axis=1
)
casos_por_tip_serv = casos_por_tip_serv[l_campos]  # Reordenación de columnas
# ***Casos por Tipo de Servicio***
print("\n" * 1, casos_por_tip_serv[l_campos].to_string())

# ***Usos por asegurados Cantidad y Total Monto Pagado***
print(
    "\n",
    "Uso por asegurado",
    len(archivo["CERTIFICADO"].unique()),
    "MONTO_PAGADO",
    archivo["MONTO_PAGADO"].sum(),
)

# ***Top 10 de Monto Pagado***
campos_top = ["ESTADO", "TIPO_SERVICIO", "MONTO_PAGADO", "INTERVENCION"]
print(
    "\n" * 1,
    archivo.nlargest(n=10, columns=["MONTO_PAGADO"], keep="all")
    .reset_index(drop=True)[campos_top]
    .to_string(),
)

# ***Monto pagado por Clinica y Tipo de Servicio***
archivo_sin_farm = archivo[archivo["TIPO_SERVICIO"] != "FARMACIA"]
casos_por_cert_clin = archivo_sin_farm.groupby(["CLINICA", "TIPO_SERVICIO"]).agg(
    {"MONTO_PAGADO": ["count", "sum"]}
)
print("\n" * 1, casos_por_cert_clin.to_string())

tipo_serv = archivo.groupby(["TIPO_SERVICIO"]).agg({"MONTO_PAGADO": ["sum"]})
gp_tipo_serv = tipo_serv.reset_index()
gp_tipo_serv["PORCENTJE"] = gp_tipo_serv.apply(
    lambda x: x["MONTO_PAGADO"] / gp_tipo_serv["MONTO_PAGADO"].sum(), axis=1
)
gp_tipo_serv["PORCENTJE"] = gp_tipo_serv["PORCENTJE"].apply("{:.2%}".format)
# ***Monto Pagado por Tipo de Servicio***
print("\n" * 1, gp_tipo_serv.to_string())
