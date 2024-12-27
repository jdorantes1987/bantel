from datetime import date, datetime

from matplotlib.pyplot import show, subplots, title
from numpy import array, nan
from pandas import (
    DataFrame,
    Series,
    concat,
    factorize,
    merge,
    options,
    pivot_table,
    read_excel,
    to_datetime,
)
from seaborn import heatmap

from accesos.data_base import get_read_sql, insert_sql
from accesos.datos import (
    articulos_profit,
    dict_con_admin,
    factura_venta_con_su_detalle_en_usd,
    factura_venta_en_usd,
    facturacion_x_anio,
    get_fecha_tasa_bcv_del_dia,
    get_last__nro_fact_venta,
    get_monto_tasa_bcv_del_dia,
)
from accesos.files_excel import p_data_insert_fact_y_recibos
from banco_central.bcv import get_tasa
from varios.utilidades import date_today, last_date_of_month

options.display.float_format = (
    "{:,.2f}".format
)  # Configuramos separadores de miles y 2 decimales
hoy = date.today()
tabla_select = {"v": "saDocumentoVenta", "c": "saDocumentoCompra"}
l_tip_doc_ajust_m = ["AJPM", "AJNM"]
l_tip_doc_ajust_a = ["AJNA", "AJPA"]
l_col_art_conatel = [
    "art_146 2.3%",
    "art_147 0.5%",
    "art_148_anual 0.5%",
    "art_150 1%",
    "art_151 0.5%",
    "Fonacit 0.5%",
]


def __doc_select_data(k_tabla, fec_ini, fec_fin):
    tabla = tabla_select[str(k_tabla).lower()]
    print(tabla)
    r_isrl_fini = to_datetime(
        date(to_datetime(fec_ini).year, to_datetime(fec_ini).month, 1),
        format="%d-%m-%Y",
    ).strftime("%Y%m%d")
    r_isrl_ffin = to_datetime(
        last_date_of_month(to_datetime(fec_ini).date()), format="%d-%m-%Y"
    ).strftime("%Y%m%d")
    sql = (
        f"SELECT co_tipo_doc, iif(co_tipo_doc='N/CR', "
        f"-(total_bruto-monto_desc_glob), (total_bruto-monto_desc_glob)) as base_imponible, "
        f"iif(co_tipo_doc='N/CR', -monto_imp, monto_imp) as monto_imp, "
        f"iif(co_tipo_doc='N/CR', -total_neto, total_neto)  as total_neto, "
        f"otros1 as IGTF, num_comprobante "
        f"FROM {tabla} "
        f"WHERE anulado=0 and CONVERT(DATE, fec_reg)>='{fec_ini}' and CONVERT(DATE, fec_reg)<='{fec_fin}'"
    )

    sql2 = (
        f"SELECT co_tipo_doc, (total_bruto-monto_desc_glob) as base_imponible, monto_imp, total_neto, "
        f"otros1 as IGTF, num_comprobante "
        f"FROM {tabla} "
        f"WHERE anulado=0 and CONVERT(DATE, fec_reg)>='{r_isrl_fini}' and "
        f"CONVERT(DATE, fec_reg)<='{r_isrl_ffin}' AND co_tipo_doc='ISLR'"
    )
    doc = get_read_sql(sql, **dict_con_admin)
    ret_islr = get_read_sql(sql2, **dict_con_admin)
    ret_islr["co_tipo_doc"] = ret_islr["co_tipo_doc"].str.strip()  # suprimir espacios
    docs_col = ["base_imponible", "IGTF", "monto_imp", "total_neto"]
    ret_islr_t = ret_islr.groupby("co_tipo_doc")[docs_col].sum().reset_index()
    doc["co_tipo_doc"] = doc[
        "co_tipo_doc"
    ].str.strip()  # suprimir espacios en las cadenas de texto
    # Remplaza los valores nulos por espacios vacios, para no generar error al hacer la comparacion
    # en la columna numero comprobantes
    doc["num_comprobante"] = doc["num_comprobante"].replace(nan, " ")
    docs_tipos = ["FACT", "IVAN", "N/CR", "N/DB"]
    # Varifica si los valores de la columna "co_tipo_doc" existen dentro de la lista "docs_tipos"
    facturas = doc[
        doc["co_tipo_doc"].isin(docs_tipos)
        & ~doc["num_comprobante"].str.contains("00000000")
    ]  # Si no contiene comprobantes en cero
    # Agrupa los tipos de documentos, el método reset_index()
    # permite resetear los indices de filas del marco de datos
    group_doc = facturas.groupby("co_tipo_doc")[docs_col].sum().reset_index()
    docs = group_doc
    if tabla == "saDocumentoVenta":
        # Suma los valores de la columna base_imponible que no sean IVAN e ISLR dentro de la columna co_tipo_doc
        # para obtener el Anticipo de ISLR
        total_ant_islr = (
            docs.loc[
                ~docs["co_tipo_doc"].isin(["IVAN", "ISLR"]), "base_imponible"
            ].sum()
            * 0.01
        )
        docs.loc["aislr"] = ["ANT. ISLR", total_ant_islr, 0, 0, total_ant_islr]
    docs = concat([docs, ret_islr_t], axis=0, ignore_index=True)
    docs.loc["tg"] = [
        "TOTAL NETO",
        docs.loc[
            ~docs["co_tipo_doc"].isin(["IVAN", "ISLR", "ANT. ISLR"]), "base_imponible"
        ].sum(),
        docs.loc[
            ~docs["co_tipo_doc"].isin(["IVAN", "ISLR", "ANT. ISLR"]), "IGTF"
        ].sum(),
        docs.loc[
            ~docs["co_tipo_doc"].isin(["IVAN", "ISLR", "ANT. ISLR"]), "monto_imp"
        ].sum(),
        docs.loc[
            ~docs["co_tipo_doc"].isin(["IVAN", "ISLR", "ANT. ISLR"]), "total_neto"
        ].sum(),
    ]

    r_docs = docs.reset_index(drop=True)

    return r_docs


def datos_declaracion():
    #  variables para unir los dataframes
    all_consults = []
    # Consultar Libro de Compras y de ventas
    libro = ["v", "c"]
    fecini = input("Fecha inicial" + "\n")
    fecfin = input("Fecha final" + "\n")
    dia_ini_qna = to_datetime(fecini).day
    dia_fin_qna = to_datetime(fecfin).day
    for elem in libro:
        df2 = __doc_select_data(elem, fecini, fecfin)
        df2["Libro"] = elem
        print(df2.to_string(), "\n" * 1)
        all_consults.append(df2)

    df_union = concat(all_consults, axis=0, ignore_index=True)
    ret_islr = (
        df_union[
            df_union["Libro"].str.contains("c")
            & df_union["co_tipo_doc"].str.contains("ISLR")
        ]["base_imponible"].tolist()
        if (dia_ini_qna > 15 or (dia_ini_qna == 1 and dia_fin_qna > 15))
        else [0]
    )
    l_union = [
        df_union[
            df_union["Libro"].str.contains("v")
            & df_union["co_tipo_doc"].str.contains("FACT")
        ]["IGTF"].tolist(),
        df_union[
            df_union["Libro"].str.contains("c")
            & df_union["co_tipo_doc"].str.contains("IVAN")
        ]["base_imponible"].tolist(),
        df_union[
            df_union["Libro"].str.contains("v")
            & df_union["co_tipo_doc"].str.contains("ANT. ISLR")
        ]["base_imponible"].tolist(),
        ret_islr,
    ]
    df8 = DataFrame(
        l_union,
        columns=["Monto"],
        index=["IGTF VENTAS", "RET. IVA", "ANT. ISLR", "RET. ISLR"],
    ).reset_index()

    df8.rename(columns={"index": "Concepto"}, inplace=True)
    df8.loc["4"] = ["Total impuestos a pagar->", df8["Monto"].sum()]
    df8["Monto$"] = df8["Monto"].apply(lambda x: x / get_monto_tasa_bcv_del_dia())
    df8["Monto$"] = df8["Monto$"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    df9 = df8.replace(nan, 0)
    print(df9.to_string(index=False))  # '.to_string(index=False)' Ocultar el indice
    return df9


def graf_calor_ventas(usd=True):
    df = facturacion_x_anio(usd).reset_index()
    vtas = df.sort_values(by=["anio", "mes"], ascending=[True, True])
    meses_letras = (
        "ENE",
        "FEB",
        "MAR",
        "ABR",
        "MAY",
        "JUN",
        "JUL",
        "AGO",
        "SEP",
        "OCT",
        "NOV",
        "DIC",
    )
    vtas["mes_letras"] = vtas["mes"].apply(lambda x: meses_letras[x - 1])
    campos_monto_facturacion = ["monto_base_item", "monto_base_item$"]
    campo_select = campos_monto_facturacion[
        int(usd)
    ]  # Selecciona los montos en $ o Bs. ATENCIÓN: este codigo solo funciona con dos campos o dos valores lógicos ((1) VERDADERO (0) FALSO)
    print(vtas.to_string())
    # reshape flights dataeset in proper format to create seaborn heatmap
    flights_df = pivot_table(
        vtas,
        values=campo_select,
        index=["mes_letras"],
        columns=["anio"],
        aggfunc="sum",
        sort=False,
    )
    print("\n" * 1, flights_df)
    fig, ax = subplots(figsize=(8, 7))
    # create seaborn heatmap, usar parametro center=True para colocar derivados de un color
    heatmap(
        flights_df,
        linewidths=0.5,
        annot=True,
        cmap="Blues",
        center=True,
        annot_kws={"size": 10},
        fmt=",.2f",
        cbar_kws={"format": "%.0f"},
    )
    titulo = "Ventas BANTEL"
    title(titulo, fontsize=12)
    ttl = ax.title
    ttl.set_position([0.5, 0.5])
    show()


def __get_doc_ajustes(libro):
    tabla = tabla_select[libro]
    sql = f"Select * FROM {tabla} WHERE anulado=0 AND co_tipo_doc LIKE '%AJ%'"
    doc = get_read_sql(sql, **dict_con_admin)
    doc["co_tipo_doc"] = doc["co_tipo_doc"].str.strip()  # suprimir espacios
    doc["nro_orig"] = doc["nro_orig"].str.strip()  # suprimir espacios
    return doc


def __get_pagos():
    sql = "Select * FROM saPago"
    pagos = get_read_sql(sql, **dict_con_admin)
    pagos["cob_num"] = pagos["cob_num"].str.strip()
    return pagos


def __get_cobros():
    sql = "Select * FROM saCobro"
    cobros = get_read_sql(sql, **dict_con_admin)
    cobros["cob_num"] = cobros["cob_num"].str.strip()
    return cobros


def __doc_ajustes_automaticos_compras():
    df = __get_doc_ajustes("c")
    df_filt = df[df["co_tipo_doc"].isin(l_tip_doc_ajust_a)]
    return df_filt


def __doc_ajustes_automaticos_ventas():
    df = __get_doc_ajustes("v")
    df_filt = df[df["co_tipo_doc"].isin(l_tip_doc_ajust_a)]
    return df_filt


def __doc_ajustes_manuales_compras():
    df = __get_doc_ajustes("c")
    df_filt = df[df["co_tipo_doc"].isin(l_tip_doc_ajust_m)]
    return df_filt


def __doc_ajustes_manuales_ventas():
    df = __get_doc_ajustes("v")
    df_filt = df[df["co_tipo_doc"].isin(l_tip_doc_ajust_m)]
    return df_filt


def ajustes_aut_compras_sin_cta_contable():
    ajut_aut = __doc_ajustes_automaticos_compras()
    pgos = __get_pagos()
    merg1 = merge(ajut_aut, pgos, how="left", left_on="nro_orig", right_on="cob_num")
    ajut_sin_cta = merg1[merg1["dis_cen_y"].isnull()]  # Filtrar registros nulos
    print("---compras")
    print(
        ajut_sin_cta[
            ["co_tipo_doc", "nro_doc", "cob_num", "fecha", "total_bruto", "dis_cen_y"]
        ].to_string(index=False)
    )


def ajustes_man_compras_sin_cta_contable():
    ajut_man = __doc_ajustes_manuales_compras()
    ajut_sin_cta = ajut_man[ajut_man["dis_cen"].isnull()]  # Filtrar registros nulos
    print("---compras")
    print(
        ajut_sin_cta[
            [
                "co_tipo_doc",
                "nro_doc",
                "observa",
                "total_bruto",
                "saldo",
                "nro_orig",
                "fec_reg",
                "dis_cen",
            ]
        ].to_string()
    )


def ajustes_man_ventas_sin_cta_contable():
    ajut_man = __doc_ajustes_manuales_ventas()
    ajut_sin_cta = ajut_man[ajut_man["dis_cen"].isnull()]  # Filtrar registros nulos
    print("---ventas")
    print(
        ajut_sin_cta[
            [
                "co_tipo_doc",
                "nro_doc",
                "observa",
                "total_bruto",
                "saldo",
                "nro_orig",
                "fec_reg",
                "dis_cen",
            ]
        ].to_string()
    )


def ajustes_aut_ventas_sin_cta_contable():
    ajut_aut = __doc_ajustes_automaticos_ventas()
    cob = __get_cobros()
    merg1 = merge(ajut_aut, cob, how="left", left_on="nro_orig", right_on="cob_num")
    ajut_sin_cta = merg1[merg1["dis_cen_y"].isnull()]  # Filtrar registros nulos
    print("---ventas")
    print(
        ajut_sin_cta[
            ["co_tipo_doc", "nro_doc", "cob_num", "fecha", "total_bruto", "dis_cen_y"]
        ].to_string(index=False)
    )


def __get_impuestos_conatel__():
    datos_fact = facturacion_x_anio().reset_index()
    # Se agregan las nuevas columnas con los porcentajes de la matriz numpy
    datos_fact[l_col_art_conatel] = array([0.023, 0.005, 0.005, 0.010, 0.005, 0.005])
    # Se multiplica el porcentaje de cada columna por monto_base_item
    datos_fact[l_col_art_conatel] = datos_fact.apply(
        lambda x: x[l_col_art_conatel] * x["monto_base_item"], axis=1
    )
    # datos_fact['total_conatel'] = datos_fact.apply(
    #     lambda x: sum(x[['art_146', 'art_147', 'art_150', 'art_151']]), axis=1) # Agrega la columna total_conatel
    return datos_fact


def asiento_conatel(periodo):
    new_df = __get_impuestos_conatel__()
    new_df2 = new_df.set_index(
        ["anio", "mes"]
    )  # Asigna o establece 'anio' como columna clave
    # Elimina la columna 'monto_base_item' ya que no será usada en el nuevo dataframe
    new_df3 = new_df2.drop("monto_base_item", axis=1)
    # Se crea las lineas de los reglones en el comprobante
    linea = ["1", "2", "3", "4", "5", "6"]
    linea2 = ["7", "8", "9", "10", "11", "12"]
    # Multiplicar y agrega nuevos valores o elementos a las listas
    ctas_gasto = ["6.1.15.01.0001"] * 4  # Conatel
    ctas_pasivo = ["2.4.01.04.0001"] * 4  # Conatel
    ctas_gasto.append("6.1.15.01.0009")  # FIDETEL
    ctas_gasto.append(
        "6.1.15.01.0007"
    )  # Fonacit Fondo Nacional para el Desarrollo del Deporte
    ctas_pasivo.append("2.4.01.07.0002")  # FIDETEL
    ctas_pasivo.append(
        "2.4.01.07.0001"
    )  # Fonacit Fondo Nacional para el Desarrollo del Deporte
    s = Series(
        list(new_df3.loc[periodo]), index=linea
    )  # Crea una serie para el dataframe de los gastos
    o_gasto = {"monto": s}
    df_asiento_gto = DataFrame(o_gasto)
    df_asiento_gto["cuenta"] = ctas_gasto
    df_asiento_gto["grupo"] = "gasto"
    df_asiento_gto["descrip_det"] = l_col_art_conatel

    s2 = Series(
        list(new_df3.loc[periodo]), index=linea2
    )  # Crea una serie para el dataframe de los pasivos
    o_pasivo = {"monto": s2}
    df_asiento_pas = DataFrame(o_pasivo)
    df_asiento_pas["cuenta"] = ctas_pasivo
    df_asiento_pas["grupo"] = "pasivo"
    df_asiento_pas["descrip_det"] = l_col_art_conatel

    descrip_aux = f"PROV. PAGO CONATEL Y FONACIT {periodo} "
    list_df_asiento = [df_asiento_gto, df_asiento_pas]
    data_asiento_conatel = concat(list_df_asiento)
    data_asiento_conatel["debe"] = data_asiento_conatel.apply(
        lambda x: x["monto"] if x["grupo"] == "gasto" else 0.0, axis=1
    )
    data_asiento_conatel["haber"] = data_asiento_conatel.apply(
        lambda x: x["monto"] if x["grupo"] == "pasivo" else 0.0, axis=1
    )
    data_asiento_conatel["descrip_det"] = data_asiento_conatel.apply(
        lambda x: str(descrip_aux + x["descrip_det"]).upper(), axis=1
    )
    data_asiento_conatel = data_asiento_conatel[
        [
            "cuenta",
            "descrip_det",
            "debe",
            "haber",
        ]
    ]  # Reordena las columnas
    return data_asiento_conatel


# print(asiento_conatel((2024, 1)).to_string())
# print(__get_impuestos_conatel__().to_string())


def facturacion_docs_sin_saldo():  # Facturas de ventas cobradas en su totalidad
    sql = (
        "SELECT RTRIM(co_tipo_doc) as co_tipo_doc, nro_doc, fec_reg, co_cli, "
        "(iif(co_tipo_doc='N/CR', -(total_bruto-monto_desc_glob), "
        "(total_bruto-monto_desc_glob))) as Monto_Base "
        "FROM saDocumentoVenta "
        "WHERE anulado=0 and RTRIM(co_tipo_doc) in('FACT', 'N/CR') and saldo='0'"
    )
    fact = get_read_sql(sql, **dict_con_admin)
    # #  # suprimir espacios en las cadenas de texto en varias columnas a la vez
    # fact[['nro_doc', 'co_cli']] = fact[['nro_doc', 'co_cli']].apply(
    #     lambda x: x[['nro_doc', 'co_cli']].str.strip(), axis=1)
    return fact


campos_comunes_fact = ["co_tipo_doc", "doc_num", "fec_reg", "co_cli", "cli_des"]


def facturacion_saldo_x_clientes_detallado(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    print("\nFacturas con saldo a la fecha:")
    l_campos = campos_comunes_fact.copy()
    tasa = get_tasa()
    l_campos.extend(
        [
            "saldo_total_doc",
            "saldo_total_doc$",
            "saldo_total_doc_actual$",
            "dif_cambio$",
        ]
    )
    anio, mes, dato_cliente = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("dato_cliente", "all"),
    )
    df_fact = factura_venta_con_su_detalle_en_usd(anio=anio, mes=mes, usd=True)
    df_fact["saldo_total_doc_actual$"] = df_fact.apply(
        lambda x: x["saldo_total_doc"] / tasa, axis=1
    )
    df_fact["dif_cambio$"] = df_fact.apply(
        lambda x: x["saldo_total_doc$"] - x["saldo_total_doc_actual$"], axis=1
    )
    df_fact_con_saldo = df_fact[df_fact["saldo_total_doc"] != 0][
        l_campos
    ].drop_duplicates()
    datos_filter = df_fact_con_saldo
    if dato_cliente != "all":
        datos_filter = df_fact_con_saldo[
            (df_fact_con_saldo["co_cli"].str.contains(dato_cliente))
            | (df_fact_con_saldo["cli_des"].str.contains(dato_cliente))
        ].copy()  # substring criteria
    today = datetime.now()
    datos_filter["dias_transc"] = (
        today - datos_filter["fec_reg"]
    ).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
    datos_filter = datos_filter.sort_values(
        by=["cli_des", "saldo_total_doc", "fec_reg"], ascending=[True, False, False]
    )
    print("Saldo total Bs.:", round(datos_filter["saldo_total_doc"].sum(), ndigits=2))
    print("Saldo total $:", round(datos_filter["saldo_total_doc$"].sum(), ndigits=2))
    print(
        "Saldo total $ según tasa actual:",
        round(datos_filter["saldo_total_doc_actual$"].sum(), ndigits=2),
    )
    print(
        "Saldo diferencia en cambio$:",
        round(datos_filter["dif_cambio$"].sum(), ndigits=2),
    )
    return datos_filter


def facturacion_saldo_x_clientes_resumen(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    df_fact = facturacion_saldo_x_clientes_detallado(anio=anio, mes=mes, usd=True)
    df_fact["anio"] = df_fact["fec_reg"].dt.year  # Obtiene el año
    df_fact["mes"] = df_fact["fec_reg"].dt.month_name(locale="es_ES.utf8").str[:3]
    f_montos = "saldo_total_doc$" if conv_usd else "saldo_total_doc"
    pivot = pivot_table(
        df_fact,
        values=f_montos,
        index=["cli_des"],
        columns=["anio", "mes"],
        aggfunc="sum",
        margins=True,
        sort=False,
    ).replace(
        nan, 0
    )  # Remplaza los valores nan con ceros
    return pivot


def facturas_cobradas_x_clientes_detallado(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    print("\nFacturas cobradas a la fecha:")
    anio, mes = kwargs.get("anio", "all"), kwargs.get("mes", "all")
    l_campos = campos_comunes_fact.copy()
    l_campos.extend(["total_item_cobr", "total_item_cobr$"])
    df_fact = factura_venta_en_usd(anio=anio, mes=mes, usd=True)
    df_fact["total_item_cobr"] = df_fact.apply(
        lambda x: x["total_item"] + x["igtf"] - x["saldo_total_doc"], axis=1
    )  # Se le resta x['saldo_total_doc'] en caso de cobro parcial
    df_fact["total_item_cobr$"] = df_fact.apply(
        lambda x: x["total_item$"] + x["igtf$"] - x["saldo_total_doc$"], axis=1
    )  # Se le resta x['saldo_total_doc$'] en caso de cobro parcial
    # df_fact_cobradas = df_fact[(df_fact['saldo_total_doc'] == 0.00) | ((abs(df_fact['saldo_total_doc']) - abs(df_fact['total_item_cobr'])) != 0.00)][l_campos]
    df_fact_cobradas = df_fact[df_fact["total_item_cobr"] != 0.00][l_campos]
    docts = df_fact_cobradas.sort_values(
        by=["cli_des", "total_item_cobr", "fec_reg"], ascending=[True, False, False]
    )
    print("Total Bs.:", round(docts["total_item_cobr"].sum(), ndigits=2))
    print("Total $:", round(docts["total_item_cobr$"].sum(), ndigits=2))
    return docts


def facturas_cobradas_x_clientes_resumen(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    df_fact = facturas_cobradas_x_clientes_detallado(anio=anio, mes=mes, usd=conv_usd)
    df_fact["anio"] = df_fact["fec_reg"].dt.year  # Obtiene el año
    df_fact["mes"] = df_fact["fec_reg"].dt.month_name(locale="es_ES.utf8").str[:3]
    f_montos = "total_item_cobr$" if conv_usd else "total_item_cobr"
    pivot = pivot_table(
        df_fact,
        values=f_montos,
        index=["cli_des"],
        columns=["anio", "mes"],
        aggfunc="sum",
        margins=True,
        sort=True,
    ).replace(
        nan, 0
    )  # Remplaza los valores nan con ceros
    return pivot


def diccionario_facturacion(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    print("\nDiccionario de facturación general por año y mes:")
    anio, mes, conv_usd = (
        kwargs.get("anio", 2023),
        kwargs.get("mes", 12),
        kwargs.get("conv_usd", False),
    )
    print(anio, mes)
    df_fact = factura_venta_con_su_detalle_en_usd(anio=anio, mes=mes, usd=True)
    df_dic = pivot_table(
        df_fact,
        values=["monto_base_item", "monto_base_item$"],
        index=["anio", "mes_x"],
        aggfunc="sum",
        sort=True,
    )
    a_usd = 0 if conv_usd is False else 1
    anio_mes = round(df_dic.loc[(anio, mes)][a_usd], ndigits=2)
    return anio_mes


def diccionario_facturacion_total_por_anio(
    **kwargs,
):  # Facturas de ventas parcialmente cobradas o sin cobro
    print("\nDiccionario de facturación general por año:")
    anio, conv_usd = kwargs.get("anio", 2023), kwargs.get("conv_usd", False)
    print(anio)
    campos_monto_facturacion = ["monto_base_item", "monto_base_item$"]
    campo_select = campos_monto_facturacion[
        int(conv_usd)
    ]  # Selecciona los montos en $ o Bs. ATENCIÓN: este codigo solo funciona con dos campos o dos valores lógicos ((1) VERDADERO (0) FALSO)
    df_fact = (
        facturacion_x_anio(conv_usd).groupby("anio")[[campo_select]].sum().reset_index()
    )
    df_fact.set_index(["anio"], inplace=True)
    ventas_anio = round(df_fact.loc[anio][0], ndigits=2)
    return ventas_anio


#  1) OBTIENE LOS DATOS DEL ARCHIVOS DE EXCEL CON LOS PLANES DE FACTURACIÓN
# ------------------------------------------------------------------------------------
def data_facturacion(**kwargs) -> DataFrame:
    # Establece como String-str la columna nro_doc
    indice_file = kwargs.get("indice_file", 0)
    a_bolivares = kwargs.get("conv_a_bs", False)
    doc_emit = kwargs.get("num_doc")
    doc_ctrol_emit = kwargs.get("num_doc_ctrol")
    format_fact = kwargs.get("num_fact_format")
    data = read_excel(p_data_insert_fact_y_recibos[indice_file])
    # primero se filtran los documentos que se van a facturar
    data_ = data[data["facturar"].str.upper() == "SI"].copy()
    data_["nro_doc"] = str(doc_emit).zfill(6) if format_fact is True else int(doc_emit)
    data_["nro_control"] = (
        str(doc_ctrol_emit).zfill(6)
        if format_fact is True
        else int(str(doc_ctrol_emit).replace("00-", ""))
    )  # Rellena una cadena numérica con ceros a la izquierda
    data_["indice_fact"] = data_.apply(
        lambda x: x["id_client"] + str(x["enum"]), axis=1
    )
    # asigna una numeracion a cada cliente que luego se usará para asignar el nuevo número de factura
    data_["grupo"] = factorize(data_["indice_fact"])[
        0
    ]  # factorize sirve para crear correlativo por grupos
    # genera el nuevo número de factura, se le suma 1 porque el correlativo del grupo comienza en cero
    # tambien evalua si se le aplicará formato al correlativo del documento
    data_["nro_doc"] = data_.apply(
        lambda x: (
            str(int(x["nro_doc"]) + int(x["grupo"]) + 1).zfill(6)
            if format_fact is True
            else (int(x["nro_doc"]) + int(x["grupo"]) + 1)
        ),
        axis=1,
    )
    data_["nro_control"] = data_.apply(
        lambda x: (
            str(int(x["nro_control"]) + int(x["grupo"]) + 1).zfill(6)
            if format_fact is True
            else "00-0" + str(int(x["nro_control"]) + int(x["grupo"]) + 1)
        ),
        axis=1,
    )
    tasa = get_monto_tasa_bcv_del_dia()
    #  Multiplica la 'cantidad' de artículos por el 'monto_base' para obtener el neto por artículo
    #  despues aplica la tasa de cambio correpondiente
    data_["monto_base"] = data_.apply(
        lambda x: round(
            (
                (x["monto_base"] * x["cantidad"]) * tasa
                if a_bolivares is True
                else x["monto_base"] * x["cantidad"]
            ),
            ndigits=2,
        ),
        axis=1,
    )
    #  se debe combinar el cod. de artículos con la tabla Artículos
    return data_


def __data_encab_facturacion_masiva(
    indice_file, a_bs, num_doc, num_doc_ctrol, num_fact_format
) -> DataFrame:

    data = data_facturacion(
        indice_file=indice_file,
        conv_a_bs=a_bs,
        num_doc=num_doc,
        num_doc_ctrol=num_doc_ctrol,
        num_fact_format=num_fact_format,
    )

    #  Agrupa el monto neto por articulo
    data_f = (
        data.groupby(
            ["id_client", "nro_doc", "nro_control", "fecha_fact", "descrip_encab_fact"]
        )["monto_base"]
        .sum()
        .reset_index()
    )
    return data_f


#  2) EJECUTA LA INSTRUCCIÓN INDIVIDUAL PARA INSERTAR CADA ENCABEZADO DE FACTURA, PROXIMAMENTE SE MANEJARÁN TRANSACCIONES
# ------------------------------------------------------------------------------------
def facturacion_masiva(indice_file, a_bs, num_doc, num_doc_ctrol, num_fact_format):
    data = __data_encab_facturacion_masiva(
        indice_file, a_bs, num_doc, num_doc_ctrol, num_fact_format
    )
    # es necesario agrupar los encabezados de factura para totalizar la Base Imponible y el IVA
    data_agrupada = (
        data.groupby(
            ["id_client", "nro_doc", "nro_control", "fecha_fact", "descrip_encab_fact"]
        )["monto_base"]
        .sum()
        .reset_index()
    )
    date_current = date_today()  # Fecha actual
    tasa_camb = get_monto_tasa_bcv_del_dia()
    tasa_fecha = format(
        get_fecha_tasa_bcv_del_dia(), "%d-%m-%Y"
    )  # fecha sin hora, minutos y segundos
    data_iva = __determinar_impuesto_por_factura(
        indice_file, True, a_bs, num_doc, num_doc_ctrol, num_fact_format
    )
    data_con_iva = merge(
        data_agrupada, data_iva, how="left", left_on="nro_doc", right_on="nro_doc"
    )
    data_con_iva["total"] = data_con_iva.apply(
        lambda x: x["monto_base"] + x["iva"], axis=1
    )
    suc = ""
    if indice_file == 1:
        comentario = f"Tasa BCV {tasa_camb} Fecha {tasa_fecha}"
        suc = "01"
    else:
        comentario = ""

    campo5 = to_datetime(date_current).month_name(locale="es_ES.utf8")
    campo7 = to_datetime(date_current).year
    print(data_con_iva.to_string())
    # itera la cantidad de documentos a facturar
    for index, row in data_con_iva.iterrows():
        index += 1
        __exe_sql_insert_encab_facturacion(
            row["nro_doc"],
            row["descrip_encab_fact"],
            row["id_client"],
            "0001",
            row["fecha_fact"],
            date_current,
            row["monto_base"],
            row["iva"],
            row["total"],
            row["nro_control"],
            comentario,  # 'Corresponde:' + row["descrip_encab_fact"].replace('Servicio', '') + ' / ' +
            campo5,
            campo7,
            suc,
        )

        procesar_det_facturacion(
            indice_file,
            row["nro_doc"],
            a_bs,
            num_doc,
            num_doc_ctrol,
            num_fact_format,
            suc,
        )


#  2 Filtra los datos del detalle de cada factura por la columna 'facturar'
def procesar_det_facturacion(
    indice_file, nro_documento, a_bs, num_doc, num_doc_ctrol, num_fact_format, sucursal
):
    df = data_facturacion(
        indice_file=indice_file,
        conv_a_bs=a_bs,
        num_doc=num_doc,
        num_doc_ctrol=num_doc_ctrol,
        num_fact_format=num_fact_format,
    )

    data_ = df[df["nro_doc"] == nro_documento].copy()
    # ejemplo de cómo usar groupby y cumcount para crear un correlativo numérico dentro de cada grupo de una columna
    data_["correl"] = data_.groupby("nro_doc").cumcount() + 1
    data_iva_temp = __determinar_impuesto_por_factura(
        indice_file, False, a_bs, num_doc, num_doc_ctrol, num_fact_format
    )
    data_iva = data_iva_temp[data_iva_temp["nro_doc"] == nro_documento].copy()
    data_iva.rename(columns={"nro_doc": "nro_doc_iva"}, inplace=True)
    data_con_iva = merge(
        data_, data_iva, left_on="correl", right_on="correl_iva", how="left"
    )
    date_current = date_today()
    for index, row in data_con_iva.iterrows():
        index += 1
        comentario = "{l1} \n {l2} \n {l3}".format(
            l1=row["comentario_l1"], l2=row["comentario_l2"], l3=row["comentario_l3"]
        ).replace("nan", "")

        __exe_sql_insert_det_facturacion(
            row["correl"],
            row["nro_doc"],
            row["co_art"],
            round(row["monto_base"] / row["cantidad"], ndigits=2),
            row["iva"],
            date_current,
            row["cantidad"],
            row["monto_base"],
            comentario,
            row["tipo_imp"],
            row["p_iva"],
            sucursal,
        )


def __determinar_impuesto_por_factura(
    indice_file, agrupado, a_bs, num_doc, num_doc_ctrol, num_fact_format
):
    data_ = data_facturacion(
        indice_file=indice_file,
        conv_a_bs=a_bs,
        num_doc=num_doc,
        num_doc_ctrol=num_doc_ctrol,
        num_fact_format=num_fact_format,
    )

    # ejemplo de cómo usar groupby y cumcount para crear un correlativo numérico dentro de cada grupo de una columna
    data_["correl_iva"] = data_.groupby("nro_doc").cumcount() + 1
    articulos = articulos_profit()[["co_art", "tipo_imp"]]
    merg1 = merge(data_, articulos, how="left", left_on="co_art", right_on="co_art")
    # Crea una columna con el monto del iva para cada artículo
    merg1["iva"] = merg1.apply(
        lambda x: (
            round(x["monto_base"] * 16 / 100, ndigits=2) if x["tipo_imp"] == "1" else 0
        ),
        axis=1,
    )
    # Crea una columna con el porcentaje de iva para cada artículo
    merg1["p_iva"] = merg1.apply(lambda x: 16.0 if x["tipo_imp"] == "1" else 0, axis=1)
    if agrupado is True:
        # es necesario agrupar los encabezados de factura para totalizar la Base Imponible y el IVA
        data_agrupada = (
            merg1.groupby(
                [
                    "id_client",
                    "nro_doc",
                    "fecha_fact",
                    "descrip_encab_fact",
                    "tipo_imp",
                    "p_iva",
                ]
            )[["monto_base", "iva"]]
            .sum()
            .reset_index()[["nro_doc", "iva", "tipo_imp", "p_iva"]]
        )
    else:
        data_agrupada = merg1[["nro_doc", "iva", "tipo_imp", "p_iva", "correl_iva"]]
    return data_agrupada


def __exe_sql_insert_encab_facturacion(
    id_doc,
    descrip,
    cod_cli,
    vendedor,
    fecha_fact,
    fecha_cur,
    monto_base,
    monto_iva,
    monto_total,
    nro_control,
    comentario,
    campo5,
    campo7,
    sucursal,
):
    # SQL para insertar el Encabezado de Factura
    strsql = (
        "INSERT INTO [dbo].[saFacturaVenta] ([doc_num] ,[descrip],[co_cli],[co_tran],[co_mone],[co_ven],"
        "[co_cond] ,[fec_emis] ,[fec_venc] ,[fec_reg] ,[anulado] ,[status] ,[n_control] ,[ven_ter] ,"
        "[tasa] ,[porc_desc_glob] ,[monto_desc_glob] ,[porc_reca] ,[monto_reca] ,[total_bruto] ,"
        "[monto_imp] ,[monto_imp2] ,[monto_imp3] ,[otros1] ,[otros2] ,[otros3] ,[total_neto] ,"
        "[saldo] ,[dir_ent] ,[comentario] ,[dis_cen] ,[feccom] ,[numcom] ,[contrib] ,[impresa] ,"
        "[seriales_s] ,[salestax] ,[impfis] ,[impfisfac] ,[imp_nro_z] ,[campo1] ,[campo2] ,[campo3] ,"
        "[campo4] ,[campo5] ,[campo6] ,[campo7] ,[campo8] ,[co_us_in] ,[co_sucu_in] ,[fe_us_in] ,"
        "[co_us_mo] ,[co_sucu_mo] ,[fe_us_mo])     "
        "VALUES ('{doc}', '{descr}', '{c_cli}', '01', 'BS', "
        "'{ven}', '01', '{f_fact}', '{f_fact}', '{f_fact}', 0, '0', "
        "'{n_contr}', 0, 1, NULL, 0, NULL, 0, {m_base}, {m_iva}, 0, 0, 0, 0, 0, {m_total}, {m_total}, NULL, "
        "'{coment}', NULL, NULL, NULL, "
        "1, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{camp5}', NULL, '{camp7}', NULL, '999', "
        "'{suc}', '{f_act}', '999', '{suc}', '{f_act}')".format(
            doc=id_doc,
            descr=descrip,
            c_cli=cod_cli,
            ven=vendedor,
            f_fact=fecha_fact,
            f_act=fecha_cur,
            m_base=monto_base,
            m_iva=monto_iva,
            m_total=monto_total,
            n_contr=nro_control,
            coment=comentario,
            camp5=campo5,
            camp7=campo7,
            suc=sucursal,
        )
    )

    insert_sql(strsql, **dict_con_admin)

    # SQL para insertar el documento, se coloca dentro del insert encabezado de factura ya que usa los mismos datos
    strsql2 = (
        "INSERT INTO [dbo].[saDocumentoVenta] ([co_tipo_doc],[nro_doc],[co_cli],[co_ven],[co_mone],"
        "[mov_ban],[tasa],[observa],[fec_reg],[fec_emis],[fec_venc],[anulado],[aut],[contrib],[doc_orig],"
        "[tipo_origen],[nro_orig],[nro_che],[saldo],[total_bruto],[porc_desc_glob],[monto_desc_glob],"
        "[porc_reca],[monto_reca],[total_neto],[monto_imp],[monto_imp2],[monto_imp3],[tipo_imp],[tipo_imp2],"
        "[tipo_imp3],[porc_imp],[porc_imp2],[porc_imp3],[num_comprobante],[feccom],[numcom],[n_control],"
        "[dis_cen],[comis1],[comis2],[comis3],[comis4],[comis5],[comis6],[adicional],[salestax],[ven_ter],"
        "[impfis],[impfisfac],[imp_nro_z],[otros1],[otros2],[otros3],[campo1],[campo2],[campo3],[campo4],"
        "[campo5],[campo6],[campo7],[campo8],[co_us_in],[co_sucu_in],[fe_us_in],[co_us_mo],[co_sucu_mo],"
        "[fe_us_mo],[co_cta_ingr_egr])     "
        "VALUES('FACT','{doc}','{c_cli}','{ven}','BS', NULL, 1, 'FACT N° {doc} de Cliente {c_cli}', '{f_fact}',"
        "'{f_fact}','{f_fact}',0,1,0,'FACT',0,'{doc}',NULL,{m_total},{m_base},NULL,0,NULL,0,"
        "{m_total},{m_iva},0,0,NULL,NULL,NULL,0,0,0,NULL,NULL,NULL,'{n_contr}',NULL,0,0,0,0,0,0,0,NULL,0,NULL,NULL,NULL,"
        "0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'999','{suc}','{f_act}','999','{suc}',"
        "'{f_act}',NULL)".format(
            doc=id_doc,
            c_cli=cod_cli,
            ven=vendedor,
            f_fact=fecha_fact,
            f_act=fecha_cur,
            m_base=monto_base,
            m_iva=monto_iva,
            m_total=monto_total,
            n_contr=nro_control,
            suc=sucursal,
        )
    )

    insert_sql(strsql2, **dict_con_admin)


def __exe_sql_insert_det_facturacion(
    linea,
    id_doc,
    co_art,
    total_item,
    monto_iva,
    fecha_cur,
    cant_art,
    total_reng,
    comentario,
    tipo_imp,
    porcent_iva,
    sucursal,
):
    strsql = (
        "INSERT INTO [dbo].[saFacturaVentaReng] ([reng_num] ,[doc_num] ,[co_art] ,[des_art] ,[co_alma] ,"
        "[total_art] ,[stotal_art] ,[co_uni] ,[sco_uni] ,[co_precio] ,[prec_vta] ,[prec_vta_om] ,[porc_desc] ,"
        "[monto_desc] ,[tipo_imp] ,[tipo_imp2] ,[tipo_imp3] ,[porc_imp] ,[porc_imp2] ,[porc_imp3] ,[monto_imp] ,"
        "[monto_imp2] ,[monto_imp3] ,[reng_neto] ,[pendiente] ,[pendiente2] ,[tipo_doc] ,[num_doc] ,"
        "[total_dev] ,[monto_dev] ,[otros] ,[comentario] ,[lote_asignado] ,[monto_desc_glob] ,"
        "[monto_reca_glob] ,[otros1_glob] ,[otros2_glob] ,[otros3_glob] ,[monto_imp_afec_glob] ,"
        "[monto_imp2_afec_glob] ,[monto_imp3_afec_glob] ,[dis_cen] ,[co_us_in] ,[co_sucu_in] ,"
        "[fe_us_in] ,[co_us_mo] ,[co_sucu_mo] ,[fe_us_mo])     "
        "VALUES ({reng}, '{doc}', '{codigo_art}', NULL, "
        "'NA', {cant_a}, 0, '001', NULL, '01', {t_item}, NULL, NULL, 0, '{tp_imp}', NULL, NULL, {ptj_iva}, 0, 0, {m_iva}, 0, 0, "
        "{total_r}, {cant_a}, 0, NULL, NULL, 0, 0, 0, '{coment}', 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, '999', '{suc}', "
        "'{f_act}', '999', '{suc}', '{f_act}')".format(
            reng=linea,
            doc=id_doc,
            codigo_art=co_art,
            t_item=total_item,
            m_iva=monto_iva,
            f_act=fecha_cur,
            cant_a=cant_art,
            total_r=total_reng,
            coment=comentario,
            tp_imp=tipo_imp,
            ptj_iva=porcent_iva,
            suc=sucursal,
        )
    )
    insert_sql(strsql, **dict_con_admin)


def procesar_facturacion_masiva(indice_file, a_bs, num_fact_format):
    # Convierte el dataframe obtenido a un diccionario
    lista_last_documents = get_last__nro_fact_venta().to_dict()
    # asigna a la variable el último número de factura emitida en profit
    num_doc = (
        lista_last_documents["doc_num"][0]
        if lista_last_documents["doc_num"] != {}
        else 0
    )
    # asigna a la variable el último número de control de factura en profit
    num_doc_ctrol = (
        lista_last_documents["n_control"][0]
        if lista_last_documents["n_control"] != {}
        else 0
    )
    facturacion_masiva(indice_file, a_bs, num_doc, num_doc_ctrol, num_fact_format)


if __name__ == "__main__":
    print(facturacion_docs_sin_saldo())
