from articulos import (
    agrupa_facturacion,
    get_data_art_con_sus_sub_cod,
    get_maestro_linea_art,
)
from pandas import merge as pd_merge
from plotly import express as px

from accesos.datos import facturacion_por_cod_art


def get_data_facturacion_con_linea_art(**kwargs):
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    articulos = get_data_art_con_sus_sub_cod()
    facturas = facturacion_por_cod_art(anio=anio, mes=mes, usd=conv_usd)
    linea_art = get_maestro_linea_art()[["co_lin", "grupo", "lin_des", "detalle"]]
    # unir los artículos de las facturas
    # con los campos 'co_art' y 'campo1'
    # del archivo: 'Admin-Izq-Estructura-Ingresos-Articulos.xlsm'
    # hoja 'Cod_Articulos'
    join = pd_merge(
        facturas, articulos, how="left", left_on="cod_art_izq", right_on="co_art"
    )
    group_art_x_fact = join.groupby("campo1")[["monto_base_item$"]].sum()
    # unir los grupos ubicados en la hoja 'Linea_Articulo' del archivo excel: Admin-Izq-Estructura-Ingresos-Articulos.xlsm'
    # con el campo 'campo1' que contiene los grupos de la merge anterior.
    merge = pd_merge(
        linea_art, group_art_x_fact, how="left", left_on="co_lin", right_on="campo1"
    )
    merge.rename(columns={"monto_base_item$": "monto"}, inplace=True)
    return merge[["co_lin", "grupo", "lin_des", "detalle", "monto"]]


def sunburst_agrupa_facturacion(**kwargs):
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    data_ing = agrupa_facturacion(
        get_data_facturacion_con_linea_art(anio=anio, mes=mes, usd=conv_usd)
    )[["g1", "g2", "g3", "g4", "g5", "g6", "es_detalle", "monto"]]
    data_ing_detalle = data_ing[
        (data_ing["es_detalle"] == 1) & (data_ing["monto"] != 0.0)
    ]
    # print(data_ing_detalle['monto'].sum())
    # print(data_ing_detalle.to_string())
    # Crear un gráfico Sunburst con los datos
    fig = px.sunburst(
        data_ing_detalle,
        path=["g2", "g3", "g4", "g5", "g6"],
        values="monto",
        width=950,
        height=950,
    )  # color_continuous_scale="RdYlGn", color='sum_x_grupo'
    # Mostrar el gráfico
    fig.show()


if __name__ == "__main__":
    # print(agrupa_facturacion(get_data_facturacion_con_linea_art(anio=2023, usd=True))[['co_base', 'descripcion_cod_base', 'monto', 'sum_x_grupo', 'porce_x_grupo', 'descripcion_grupo']].to_string())
    sunburst_agrupa_facturacion(anio=2024, mes=11, usd=False)
