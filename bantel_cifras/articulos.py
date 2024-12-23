import pandas as pd
from numpy import nan

from accesos.data_base import get_read_sql
from accesos.datos import dict_con_admin

path_file_articulos = (
    "F:/ESTRUCTURA-INGRESOS/Admin-Izq-Estructura-Ingresos-Articulos.xlsm"
)
pd.options.display.float_format = (
    "{:,.2f}".format
)  # Configuramos separadores de miles y 2 decimales


def get_maestro_linea_art():
    """--> Obtiene los grupos ubicados en la hoja 'Linea_Articulo'
    del archivo excel:
    Admin-Izq-Estructura-Ingresos-Articulos.xlsm'
    """
    linea_art = pd.read_excel(path_file_articulos, sheet_name="Linea_Articulo")
    linea_art2 = linea_art.drop(["monto"], axis=1)  # Elimina la columna 'monto'
    return linea_art2


def agrupa_facturacion(data_linea_art):
    l_campos = [
        "co_base",
        "grupo",
        "descripcion_cod_base",
        "monto",
        "es_detalle",
        "sum_x_grupo",
        "porce_x_grupo",
        "descripcion_grupo",
        "g1",
        "g2",
        "g3",
        "g4",
        "g5",
        "g6",
    ]
    linea_art = data_linea_art
    # Se convierte el tipo de datos a String de la columna grupo ya que para los valores 01, 02, 05 los toma como float
    linea_art["grupo"] = linea_art["grupo"].astype("str")
    # Asigna el grupo padre para aquellos códigos de lineas que no tiene padre ejemplo "ING-01, ING-02, ING-05" no tienen grupo
    linea_art["grupo"] = linea_art.apply(
        lambda x: str(x["co_lin"])[:5] if x["grupo"] == "nan" else x["grupo"], axis=1
    )
    join_ph = pd.merge(
        linea_art, linea_art, left_on="grupo", right_on="co_lin", suffixes=("_p", "_h")
    )
    join1 = pd.merge(linea_art, join_ph, left_on="co_lin", right_on="co_lin_p")
    join1 = join1.rename(
        columns={
            "co_lin": "co_base",
            "detalle": "es_detalle",
            "lin_des": "descripcion_cod_base",
            "lin_des_h": "descripcion_grupo",
        }
    )

    join1["sum_x_grupo"] = join1.apply(
        lambda x: (
            join1[(join1["co_base"].str[: len(x["co_base"])] == x["co_base"])][
                "monto"
            ].sum()
            if x["es_detalle"] == 0
            else x["monto"]
        ),
        axis=1,
    )

    join1["porce_x_grupo"] = join1.apply(
        lambda x: (
            x["monto"] / join1[join1["grupo"] == x["grupo"]]["monto"].sum()
            if x["es_detalle"] == 1 and x["sum_x_grupo"] != 0
            else (
                (
                    x["sum_x_grupo"]
                    / join1[(join1["co_base"] == x["grupo"])]["sum_x_grupo"].sum()
                )
                if (x["sum_x_grupo"] != 0) and len(x["co_base"]) != 5
                else (
                    x["sum_x_grupo"] / join1["monto"].sum()
                    if x["sum_x_grupo"] != 0
                    else 0
                )
            )
        ),
        axis=1,
    )

    #  Se crean los grupos para el gráfico de Sunburst
    linea_art_index = linea_art.copy()
    linea_art_index.set_index(["co_lin"], inplace=True)
    join1["g1"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:3], "lin_des"]
    )
    join1["g2"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:6], "lin_des"]
    )
    join1["g3"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:8], "lin_des"]
    )
    join1["g4"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:10], "lin_des"] if len(x) >= 10 else None
    )
    join1["g5"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:12], "lin_des"] if len(x) >= 12 else None
    )
    join1["g6"] = join1["co_base"].apply(
        lambda x: linea_art_index.loc[x[:16], "lin_des"] if len(x) >= 16 else None
    )
    # join1 = join1.replace(nan, 0)  # Reemplaza todos los valores nan por cero 0
    join1 = join1[l_campos]
    join1["porce_x_grupo"] = join1["porce_x_grupo"].apply("{:.2%}".format)
    return join1


def get_data_articulos() -> pd.DataFrame:
    articulos = pd.read_excel(path_file_articulos, sheet_name="Cod_Articulos")
    return articulos


def get_data_art_con_sus_sub_cod():
    """
    --> Obtiene los campos 'co_art' y 'campo1'
        del archivo excel que contiene los artículos
        con la estructura de los ingresos.

        El campo 'campo1' representa el grupo
        correspodiente al que pertenece cada artículo.

    """
    articulos = get_data_articulos()
    return articulos[["co_art", "campo1"]]


def get_data_articulos_profit():
    sql = f"Select * FROM saArticulo"
    art = get_read_sql(sql, **dict_con_admin)
    return art
