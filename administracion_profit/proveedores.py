import pandas as pd
from varios.utilidades import search_df as busq_in_dataframe
from datetime import date
from accesos.datos import proveedores
from accesos.datos import factura_compra_con_su_detalle

hoy = date.today()


def search_prov(string_s):
    df = proveedores().copy()
    # Extrae los primeros 60 caracteres de la izquierda
    df["direc1"] = df["direc1"].str[:60]
    # Extrae los primeros 60 caracteres de la izquierda
    df["prov_des"] = df["prov_des"].str[:45]
    df["fe_us_in"] = pd.to_datetime(df["fe_us_in"]).dt.normalize()
    resul = busq_in_dataframe(string_s, df)[
        ["co_prov", "prov_des", "rif", "telefonos", "respons", "direc1", "co_us_in"]
    ]
    return resul


def get_top_compras_x_prov(top=15):
    print(f"\nTOP {top}", "facturación por proveedor")
    l_col = ["anio", "co_prov", "prov_des", "monto_base_item"]
    data_fact = factura_compra_con_su_detalle()
    prov = proveedores().copy()
    result = data_fact.nlargest(
        n=top, columns=["monto_base_item"], keep="all"
    ).reset_index(drop=True)
    join1 = pd.merge(result, prov, how="left", left_on="co_prov", right_on="co_prov")
    join1["co_prov"] = join1[
        "co_prov"
    ].str.strip()  # Elimina o suprime los espacios de más
    result = join1[l_col]
    print("Total Bs. {:,.2f} \n".format(result["monto_base_item"].sum()))
    return result
