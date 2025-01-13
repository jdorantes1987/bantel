from re import findall
from xml.etree import ElementTree as xml_tree

from numpy import nan
from pandas import DataFrame, concat, merge, merge_asof, to_datetime

from accesos.data_base import get_read_sql
from accesos.files_excel import datos_estadisticas_tasas as p_est_bcv
from varios.utilidades import search_df, ultimo_dia_mes

# dict_con_admin = {'host': '10.100.104.11', 'base_de_datos': 'BANTEL_I'}  # BANTEL_A, BANTEL_I
# dict_con_contab = {'host': '10.100.104.11', "base_de_datos": "BANTEL_IC"}  # TBANTEL_C, BANTEL_IC
dict_con_admin = {}
dict_con_contab = {"base_de_datos": "TBANTEL_C"}


# Agrega un identificador unico para la columna pasa por parámetro
def get_identificador_unicos(df, name_field) -> DataFrame:
    df["correl"] = df.groupby([name_field]).cumcount() + 1
    df["correl"] = df["correl"].astype("str")
    df["identificador"] = df.apply(lambda x: str(x[name_field]) + x["correl"], axis=1)
    return df


def articulos_profit():
    sql = """
          Select RTRIM(co_art) as co_art, fecha_reg, art_des, tipo_imp, tipo, anulado, fecha_inac, co_lin, co_subl, co_cat, co_color
          co_ubicacion, cod_proc, item, modelo, ref, comentario, dis_cen, RTRIM(campo1) as campo1, campo2, campo3, campo4,
          campo5, campo6, campo7, campo8, co_us_in, co_sucu_in, fe_us_in, co_us_mo, co_sucu_mo, fe_us_mo
          FROM saArticulo
          """
    return get_read_sql(sql, **dict_con_admin)


def factura_venta_con_su_detalle(**kwargs):
    anio, mes = kwargs.get("anio"), kwargs.get("mes")
    where_anio = "" if anio == "all" else f" AND year(fact.fec_reg)='{anio}'"
    where_all = "WHERE fact.[anulado]=0 " + where_anio
    where_mes = f"WHERE fact.[anulado]=0 AND year(fact.fec_reg)='{anio}' and month(fact.fec_reg)='{mes}'"
    where = where_all if mes == "all" else where_mes
    sql = f"""
          SELECT reng_num, RTRIM(fact.doc_num) as doc_num, RTRIM(dfact.co_art) as co_art, RTRIM(art.campo1) as cod_art_izq,
                fact.fec_emis, fact.fec_reg, fact.fec_venc, fact.descrip,
                year(fact.fec_reg) AS anio, month(fact.fec_reg) AS mes, fact.co_ven, RTRIM(fact.co_cli) as co_cli,
                c.cli_des, (dfact.reng_neto-dfact.monto_desc_glob) AS monto_base_item,
                (dfact.monto_imp+dfact.monto_imp_afec_glob) as iva,
                ((dfact.reng_neto-dfact.monto_desc_glob)+(dfact.monto_imp+dfact.monto_imp_afec_glob)) as total_item,
                fact.otros1 as igtf, fact.saldo as saldo_total_doc
          FROM saFacturaVenta AS fact INNER JOIN saFacturaVentaReng AS dfact ON
                fact.doc_num = dfact.doc_num LEFT JOIN saArticulo AS art ON
                dfact.co_art = art.co_art LEFT JOIN saCliente AS c ON fact.co_cli = c.co_cli
          {where}
          ORDER BY fact.fec_reg, fact.doc_num
          """
    fact_det = get_read_sql(sql, **dict_con_admin)
    fact_det["co_tipo_doc"] = "FACT"
    return fact_det


def facturacion_notas_credito(**kwargs):
    l_campos = [
        "reng_num",
        "doc_num",
        "co_art",
        "cod_art_izq",
        "co_tipo_doc",
        "fec_emis",
        "fec_reg",
        "fec_venc",
        "anio",
        "mes",
        "co_ven",
        "co_cli",
        "cli_des",
        "descrip",
        "monto_base_item",
        "iva",
        "igtf",
        "total_item",
        "saldo_total_doc",
    ]
    anio, mes = kwargs.get("anio"), kwargs.get("mes")
    where_anio = "" if anio == "all" else f"AND year(docv.fec_reg)='{anio}'"
    where_all = "WHERE docv.co_tipo_doc='N/CR' AND docv.anulado=0 " + where_anio
    where_mes = f"WHERE docv.co_tipo_doc='N/CR' AND docv.anulado=0 AND year(docv.fec_reg)='{anio}' and month(docv.fec_reg)='{mes}'"
    where = where_all if mes == "all" else where_mes

    sql = f"""
          SELECT 1 as reng_num, RTRIM(docv.nro_doc) as doc_num, RTRIM(docv.co_tipo_doc) as co_tipo_doc,
                 observa as descrip, docv.dis_cen, docv.fec_emis,
                 docv.fec_reg, docv.fec_venc, year(docv.fec_reg) AS anio, month(docv.fec_reg) AS mes, docv.co_ven,
                 RTRIM(docv.co_cli) as co_cli, c.cli_des, -docv.total_bruto as monto_base_item, -docv.monto_imp as iva,
                -(docv.total_neto-docv.otros1) as total_item, -docv.otros1 as igtf,  -docv.saldo as saldo_total_doc
          FROM saDocumentoVenta AS docv LEFT JOIN saCliente AS c ON docv.co_cli = c.co_cli
          {where}
          """
    df_notas = get_read_sql(sql, **dict_con_admin)
    #  Desempaqueta la cuenta contable del texto xml en las notas de credito
    df_notas["dis_cen"] = df_notas["dis_cen"].apply(
        lambda x: (
            str(xml_tree.fromstring(x).findtext("Carpeta01/CuentaContable"))
            if x is not None
            else None
        )
    )
    art = articulos_profit()
    #  Desempaqueta la cuenta contable del texto xml en los articulos
    art["dis_cen"] = art["dis_cen"].apply(
        lambda x: (
            str(xml_tree.fromstring(x).findtext("Carpeta03/CuentaContable"))
            if x is not None
            else None
        )
    )
    art2 = art[["co_art", "dis_cen", "campo1"]]
    #  El método drop_duplicates elimina las filas duplicadas en el dataframe de la derecha basándose en la columna dis_cen
    df_notas_art = merge(
        df_notas,
        art2.drop_duplicates("dis_cen"),
        on="dis_cen",
        how="left",
        suffixes=("_t1", "_t2"),
    )
    df_notas_art["co_art"] = df_notas_art[
        "co_art"
    ].str.strip()  # suprimir espacios en las cadenas de texto
    df_notas_art.rename(columns={"campo1": "cod_art_izq"}, inplace=True)
    df_notas_art = df_notas_art[l_campos]
    return df_notas_art


l_campos_facturacion = [
    "reng_num",
    "doc_num",
    "co_art",
    "cod_art_izq",
    "co_tipo_doc",
    "fec_emis",
    "fec_reg",
    "fec_venc",
    "anio",
    "mes_x",
    "co_ven",
    "co_cli",
    "cli_des",
    "descrip",
    "monto_base_item",
    "iva",
    "igtf",
    "total_item",
    "saldo_total_doc",
    "monto_base_item$",
    "iva_usd$",
    "total_item$",
    "saldo_total_doc$",
    "igtf$",
]


def factura_venta_con_su_detalle_en_usd(**kwargs):
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    l_campos = l_campos_facturacion.copy()
    # l_campos.extend(['monto_base_item$', 'iva_usd$', 'total_item$', 'saldo_total_doc$'])
    fact_detalle = factura_venta_con_su_detalle(anio=anio, mes=mes)
    notas_de_cre = facturacion_notas_credito(anio=anio, mes=mes)
    # verifica que existan notas de crédito antes de hacer la concatenación
    if notas_de_cre.empty is not True:
        fact_detalle_total = concat(
            [fact_detalle, notas_de_cre], axis=0, ignore_index=True
        )
    else:
        fact_detalle_total = fact_detalle

    df_data_bcv = p_est_bcv()  # archivo BCV
    fact_detalle_total["fec_reg"] = to_datetime(
        fact_detalle_total["fec_reg"]
    ).dt.normalize()  # fecha sin hora, minutos y segundos
    fact_detalle_total["descrip"] = fact_detalle_total["descrip"].replace(
        nan, " "
    )  # Permite corregir error al agrupar los datos
    fact_detalle_sort = fact_detalle_total.sort_values(
        by=["fec_reg"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    data_bcv_sort = df_data_bcv.sort_values(
        by=["fecha"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    merge_data = merge_asof(
        fact_detalle_sort,
        data_bcv_sort,
        left_on="fec_reg",
        right_on="fecha",
        direction="nearest",
    )  # Combinar por aproximación
    merge_data["igtf$"] = merge_data.apply(
        lambda x: x["igtf"] / x["venta_ask2"], axis=1
    )
    merge_data["monto_base_item$"] = merge_data.apply(
        lambda x: (
            x["monto_base_item"] / x["venta_ask2"] if conv_usd else x["monto_base_item"]
        ),
        axis=1,
    )
    merge_data["iva_usd$"] = merge_data.apply(
        lambda x: x["iva"] / x["venta_ask2"] if conv_usd else x["iva"], axis=1
    )
    merge_data["total_item$"] = merge_data.apply(
        lambda x: (
            x["total_item"] / x["venta_ask2"] if conv_usd and x["reng_num"] == 1 else 0
        ),
        axis=1,
    )
    merge_data["saldo_total_doc"] = merge_data.apply(
        lambda x: x["saldo_total_doc"] if x["reng_num"] == 1 else 0, axis=1
    )
    merge_data["saldo_total_doc$"] = merge_data.apply(
        lambda x: (
            x["saldo_total_doc"] / x["venta_ask2"]
            if conv_usd and x["reng_num"] == 1
            else 0
        ),
        axis=1,
    )
    return merge_data[l_campos]


def factura_venta_en_usd(**kwargs):
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    l_campos = l_campos_facturacion.copy()
    df_fact = factura_venta_con_su_detalle_en_usd(
        anio=anio, mes=mes, usd=conv_usd
    ).copy()
    # Se eliminan los renglones y articulos para agrupar por los demás campos
    l_campos.remove("reng_num")
    l_campos.remove("co_art")
    l_campos.remove("cod_art_izq")

    lista_cifras = [
        "monto_base_item",
        "iva",
        "total_item",
        "saldo_total_doc",
        "monto_base_item$",
        "iva_usd$",
        "total_item$",
        "saldo_total_doc$",
    ]
    """
        elimina los campos correspondientes a las CIFRAS para que no los agrupe,
        no se incluye los campos 'igtf' y 'igtf$' ya que en este caso si queremos
        que los agrupe por ser montos totales.
    """

    for elem_a_eliminar in lista_cifras:
        l_campos.remove(elem_a_eliminar)

    return df_fact.groupby(l_campos)[lista_cifras].sum().reset_index()


factura_venta_en_usd(anio=2021)


def variacion_tasa_en_cobros(**kwargs):
    anio, mes = kwargs.get("anio", 2023), kwargs.get("mes", "all")
    l_campos = [
        "nro_doc",
        "co_cli",
        "cli_des",
        "f_reg_doc",
        "f_cobro",
        "dias_transc",
        "cob_num",
        "forma_pag",
        "cod_cta",
        "cod_caja",
        "mont_cob_dc",
        "m_base$",
        "m_base_cob$",
        "variacion$",
        "porc_cobrado",
    ]
    where_all = f"WHERE fp.forma_pag IS NOT NULL AND RTrim(d.co_tipo_doc) In ('FACT','N/CR') AND YEAR(d.fec_reg)={anio}"
    where_mes = f"WHERE fp.forma_pag IS NOT NULL AND RTrim(d.co_tipo_doc) In ('FACT','N/CR') AND YEAR(d.fec_reg)={anio} AND MONTH(d.fec_reg)={mes}"
    where = where_all if mes == "all" else where_mes
    sql = (
        """
            SELECT RTRIM(d.nro_doc) AS nro_doc, RTRIM(d.co_cli) AS co_cli, cl.cli_des, d.fec_reg as f_reg_doc,
                cb.fecha AS f_cobro, RTRIM(dcb.cob_num) AS cob_num, fp.forma_pag, RTRIM(fp.cod_cta) as cod_cta, RTRIM(fp.cod_caja) as cod_caja,
                (d.total_bruto-d.monto_desc_glob) as m_base, dcb.mont_cob as mont_cob_dc, d.total_neto AS total_doc,
                Round(dcb.mont_cob/d.total_neto,6) AS porc_cobrado
            FROM (((saDocumentoVenta AS d LEFT JOIN saCobroDocReng AS dcb ON d.nro_doc = dcb.nro_doc)
                LEFT JOIN saCobroTPReng AS fp ON dcb.cob_num = fp.cob_num)
                LEFT JOIN saCobro AS cb ON dcb.cob_num = cb.cob_num)
                INNER JOIN saCliente AS cl ON d.co_cli = cl.co_cli
          """
        + where
    )
    df = get_read_sql(sql, **dict_con_admin)
    df["f_reg_doc"] = to_datetime(
        df["f_reg_doc"]
    ).dt.normalize()  # fecha sin hora, minutos y segundos
    df_bcv = p_est_bcv()[["venta_ask2", "fecha"]]  # archivo BCV
    bcv_tasas = df_bcv.sort_values(
        by=["fecha"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    dc = df.sort_values(
        by=["f_reg_doc"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    merge_data1 = merge_asof(
        dc, bcv_tasas, left_on="f_reg_doc", right_on="fecha", direction="nearest"
    )  # Combinar por aproximación
    merge_data1.rename(columns={"venta_ask2": "venta_ask2_doc"}, inplace=True)
    merge_data1.rename(columns={"fecha": "fecha_bcv_doc"}, inplace=True)
    merge_data1["mont_cob_doc$"] = merge_data1.apply(
        lambda x: x["mont_cob_dc"] / x["venta_ask2_doc"], axis=1
    )
    merge_data1["total_doc$"] = merge_data1.apply(
        lambda x: x["total_doc"] / x["venta_ask2_doc"], axis=1
    )
    merge_data1["m_base$"] = merge_data1.apply(
        lambda x: (x["m_base"] * x["porc_cobrado"]) / x["venta_ask2_doc"], axis=1
    )
    merge_data_sort = merge_data1.sort_values(
        by=["f_cobro"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    data = merge_asof(
        merge_data_sort,
        bcv_tasas,
        left_on="f_cobro",
        right_on="fecha",
        direction="nearest",
    )  # Combinar por aproximación
    data.rename(columns={"venta_ask2": "venta_ask2_cob"}, inplace=True)
    data.rename(columns={"fecha": "fecha_bcv_cob"}, inplace=True)
    data["mont_cob$"] = data.apply(
        lambda x: x["mont_cob_dc"] / x["venta_ask2_cob"], axis=1
    )
    data["m_base_cob$"] = data.apply(
        lambda x: (x["m_base"] * x["porc_cobrado"]) / x["venta_ask2_cob"], axis=1
    )
    data_sort = data.sort_values(
        by=["nro_doc"], ascending=[False]
    )  # se debe ordenar el df para poder conbinar
    data_sort["variacion$"] = data_sort.apply(
        lambda x: round(x["m_base$"] - x["m_base_cob$"], ndigits=2), axis=1
    )
    data_sort["dias_transc"] = (
        data_sort["f_cobro"] - data_sort["f_reg_doc"]
    ).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
    print(
        "\n" * 1, "Diferencia total$= ", round(data_sort["variacion$"].sum(), ndigits=2)
    )
    return data_sort[l_campos]


def variacion_tasa_en_cobros_por_mes(**kwargs):
    anio = kwargs.get("anio", 2023)
    df = variacion_tasa_en_cobros(anio=anio)
    df["anio"] = df["f_reg_doc"].dt.year
    df["mes"] = df["f_reg_doc"].dt.month
    group = df.groupby(["anio", "mes"])["variacion$"].sum().reset_index()
    print(
        "\n" * 1,
        "Variacion de tasa promedio mensual$= ",
        round(group["variacion$"].mean(), ndigits=2),
    )
    return group


def facturacion_por_cod_art(**kwargs) -> DataFrame:
    """
    --> Obtiene la facturación resumida de los campos
        'cod_art_izq' y 'monto_base_item$'
    """
    anio, mes, conv_usd = (
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
        kwargs.get("usd", True),
    )
    det_fact = factura_venta_con_su_detalle_en_usd(anio=anio, mes=mes, usd=conv_usd)
    return det_fact.groupby("cod_art_izq")[["monto_base_item$"]].sum().reset_index()


def facturacion_x_cliente(anio=2023):
    doc = factura_venta_con_su_detalle_en_usd(anio=anio, mes="all", usd=True)
    # Listado de tipos de Documentos que deben ser tomados en cuenta para el calculo del impuesto CONATEL
    docs_tipos = ["FACT", "N/CR", "N/DB"]
    # Varifica si los elementos o valores de la columna "co_tipo_doc" existen dentro de la lista "docs_tipos"
    doc_leg = doc[doc["co_tipo_doc"].isin(docs_tipos)]
    doc_leg["anio"] = doc_leg["fec_reg"].dt.year  # Obtiene el año
    doc_g2 = (
        doc_leg.groupby(["anio", "co_cli"])[["monto_base_item", "monto_base_item$"]]
        .sum()
        .reset_index()
    )
    return doc_g2.sort_values(
        by=["monto_base_item", "co_cli"], ascending=[False, False]
    ).reset_index(drop=True)


def facturacion_x_anio(usd=False):
    doc = factura_venta_con_su_detalle_en_usd(anio="all", mes="all", usd=usd)
    # Listado de tipos de Documentos que deben ser tomados en cuenta para el calculo del impuesto CONATEL
    docs_tipos = ["FACT", "N/CR", "N/DB"]
    campos_monto_facturacion = ["monto_base_item", "monto_base_item$"]
    campo_select = campos_monto_facturacion[
        int(usd)
    ]  # Selecciona los montos en $ o Bs. ATENCIÓN: este codigo solo funciona con dos campos o dos valores lógicos ((1) VERDADERO (0) FALSO)
    # Varifica si los elementos o valores de la columna "co_tipo_doc" existen dentro de la lista "docs_tipos"
    doc_leg = doc[doc["co_tipo_doc"].isin(docs_tipos)]
    doc_leg["anio"] = doc_leg["fec_reg"].dt.year  # Obtiene el año
    doc_leg["mes"] = doc_leg["fec_reg"].dt.month  # Obtiene el mes
    doc_g2 = doc_leg.groupby(["anio", "mes"])[campo_select].sum().reset_index()
    fact_x_periodos = doc_g2.sort_values(
        by=["anio", "mes", campo_select], ascending=[False, False, False]
    ).reset_index(drop=True)
    fact_x_periodos.set_index(["anio", "mes"], inplace=True)
    return fact_x_periodos


def articulos_profit_con_su_cuenta_contable():
    l_campos = ["co_art", "art_des", "campo1", "co_cta_cont"]
    sql = "Select * from saArticulo"
    df = get_read_sql(sql, **dict_con_admin)
    art_profit = DataFrame(df)
    art_con_cta_asignada = art_profit[art_profit["dis_cen"].notnull()].copy()
    #  Desempaqueta la cuenta contable del texto xml
    art_con_cta_asignada["co_cta_cont"] = art_con_cta_asignada["dis_cen"].apply(
        lambda x: str(xml_tree.fromstring(x).findtext("Carpeta03/CuentaContable"))
    )
    # Filtra los valores duplicados de la columna
    art_con_cta_asignada = art_con_cta_asignada[l_campos]
    return art_con_cta_asignada


def plan_cta():
    return get_read_sql("Select * from sccuenta", **dict_con_contab)


def detalle_comprob():
    return get_read_sql("Select * from scren_co", **dict_con_contab)


def _extrae_numero(string_num):
    # Extrae los números dentro de la cadena de texto
    num = findall("[0-9.]+", string_num)
    return str(int(num[0]) + 1)


def get_id_movbanco(fecha_fin) -> str:
    df = get_read_sql(
        f"Select mov_num From saMovimientoBanco Where origen='BAN' And fecha <= '{fecha_fin}'",
        **dict_con_admin,
    )
    mb = df["mov_num"].max()
    return "MB" + _extrae_numero(mb)


def get_movbanco(fecha_inicio_mes):
    fecha_ini = fecha_inicio_mes
    fecha_final = ultimo_dia_mes(to_datetime(fecha_inicio_mes))
    sql = f"""SELECT mov_num, descrip, cod_cta, co_cta_ingr_egr, fecha, doc_num, monto_d, monto_h, idb, cob_pag,
                     anulado, co_us_in, fe_us_in, co_us_mo, fe_us_mo
              FROM saMovimientoBanco
              WHERE fecha>='{fecha_ini}' AND fecha<='{fecha_final}'
           """
    return get_read_sql(sql, **dict_con_admin)


def search_in_movbanco(**kwargs):
    str_search, anio, mes = (
        kwargs.get("texto_a_buscar"),
        kwargs.get("anio", "all"),
        kwargs.get("mes", "all"),
    )

    fields_mov_bco = [
        "mov_num",
        "fecha",
        "cod_cta",
        "descrip",
        "co_cta_ingr_egr",
        "doc_num",
        "monto_d",
        "monto_h",
        "idb",
        "USD",
    ]

    where_anio = "" if anio == "all" else f"WHERE year(fecha)='{anio}'"
    where_all = "" + where_anio
    where_mes = f"WHERE year(fecha)='{anio}' and month(fecha)='{mes}'"
    where = where_all if mes == "all" else where_mes

    sql = f"""
          SELECT RTRIM(mov_num) as mov_num, descrip, cod_cta, RTRIM(co_cta_ingr_egr) as co_cta_ingr_egr, fecha, doc_num, monto_d, monto_h, idb, cob_pag, anulado,
                 campo1, campo2, campo3, campo4, campo5, campo6, campo7, co_us_in, fe_us_in, co_us_mo, fe_us_mo
          FROM saMovimientoBanco
          {where}
        """
    df = get_read_sql(sql, **dict_con_admin)
    df["descrip"] = df["descrip"].str[
        :80
    ]  # Extrae los primeros 80 caracteres de la izquierda
    file_bcv = p_est_bcv()  # archivo BCV
    file_bcv.rename(columns={"fecha": "fecha2"}, inplace=True)
    resul_sor = df.sort_values(
        by=["fecha"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    tasas_cambio_s = file_bcv.sort_values(
        by=["fecha2"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    merge_data = merge_asof(
        resul_sor,
        tasas_cambio_s,
        left_on="fecha",
        right_on="fecha2",
        direction="nearest",
    )  # Combinar por aproximación
    # es necesario colocar axis=1 para que solo evalue las columnas indicadas en la funcion lambda
    merge_data["USD"] = merge_data.apply(
        lambda x: (x["monto_d"] + x["monto_h"]) / x["venta_ask2"], axis=1
    )
    merge_data["USD"] = merge_data["USD"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    return search_df(str_search, merge_data)[fields_mov_bco]


def clientes():
    sql = """
          SELECT RTRIM(co_cli) as co_cli, RTRIM(cli_des) as cli_des, direc1, direc2, dir_ent2, telefonos, fax, respons, fecha_reg,
                 plaz_pag, rif, email, tipo_per, ciudad, zip, website, contribu_e, porc_esp, horar_caja, inactivo, co_us_in, fe_us_in,
                 co_us_mo, fe_us_mo, campo3, campo8
          FROM saCliente
          """
    return get_read_sql(sql, **dict_con_admin)


def proveedores():
    sql = """
          SELECT  RTRIM(co_prov) as co_prov, RTRIM(prov_des) as prov_des, direc1, direc2, telefonos, fax,
                  respons, fecha_reg, plaz_pag, rif, email, tipo_per, ciudad, zip, website, contribu_e, porc_esp,
                  co_us_in, fe_us_in, co_us_mo, fe_us_mo
          FROM saProveedor
          """
    return get_read_sql(sql, **dict_con_admin)


def search_in_compras(**kwargs) -> DataFrame:
    anio, mes = kwargs.get("anio", "all"), kwargs.get("mes", "all")
    text_to_search = kwargs.get("str_search", "")
    fields_fact = [
        "doc_num",
        "nro_fact",
        "fec_emis",
        "co_prov",
        "prov_des",
        "descrip",
        "monto_base_item",
        "iva",
        "igtf",
        "total_item",
        "USD_BASE",
        "USD_IVA",
        "USD_TOTAL",
        "USD_IGTF",
    ]

    df = factura_compra_con_su_detalle(anio=anio, mes=mes)
    # Permite convertir la fecha o el tiempo a 00:00:00, debes usar dt.normalizeodt.floor
    df["fec_emis"] = to_datetime(df["fec_emis"]).dt.normalize()
    resul = search_df(text_to_search, df)  # df con el resultado de la busqueda
    resul_sor = resul.sort_values(
        by=["fec_emis"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    file_bcv = p_est_bcv()  # archivo BCV
    tasas_cambio_s = file_bcv.sort_values(
        by=["fecha"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    merge_data = merge_asof(
        resul_sor,
        tasas_cambio_s,
        left_on="fec_emis",
        right_on="fecha",
        direction="nearest",
    )  # Combinar por aproximación
    # es necesario colocar axis=1 para que solo evalue las columnas indicadas en la funcion lambda
    merge_data["USD_BASE"] = merge_data.apply(
        lambda x: x["monto_base_item"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_IVA"] = merge_data.apply(
        lambda x: x["iva"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_TOTAL"] = merge_data.apply(
        lambda x: x["total_item"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_IGTF"] = merge_data.apply(
        lambda x: x["igtf"] / x["venta_ask2"], axis=1
    )
    print(round(merge_data["USD_BASE"].sum(), ndigits=2))
    merge_data["USD_BASE"] = merge_data["USD_BASE"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_IVA"] = merge_data["USD_IVA"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_TOTAL"] = merge_data["USD_TOTAL"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_IGTF"] = merge_data["USD_IGTF"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    return merge_data[fields_fact]


def search_in_ventas(**kwargs):
    anio, mes = kwargs.get("anio", "all"), kwargs.get("mes", "all")
    text_to_search = kwargs.get("str_search", "")
    print(
        f"\n Los resultados de '{text_to_search}' en la facturación son los siguientes: "
    )
    campos_fact = [
        "doc_num",
        "fec_emis",
        "co_cli",
        "cli_des",
        "descrip",
        "monto_base_item",
        "iva",
        "igtf",
        "total_item",
        "USD_BASE",
        "USD_IVA",
        "USD_IGTF",
        "USD_TOTAL",
        "saldo_total_doc",
        "saldo_total_doc$",
    ]
    facturas = factura_venta_con_su_detalle_en_usd(anio=anio, mes=mes, usd=True)
    facturas["fec_emis"] = to_datetime(
        facturas["fec_emis"]
    ).dt.normalize()  # fecha sin hora, minutos y segundos
    resul = search_df(text_to_search, facturas)
    resul_sor = resul.sort_values(
        by=["fec_emis"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    file_bcv = p_est_bcv()  # archivo BCV
    tasas_cambio_s = file_bcv.sort_values(
        by=["fecha"], ascending=[True]
    )  # se debe ordenar el df para poder conbinar
    merge_data = merge_asof(
        resul_sor,
        tasas_cambio_s,
        left_on="fec_emis",
        right_on="fecha",
        direction="nearest",
    )  # Combinar por aproximación
    # es necesario colocar axis=1 para que solo evalue las columnas indicadas en la funcion lambda
    merge_data["USD_BASE"] = merge_data.apply(
        lambda x: x["monto_base_item"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_IVA"] = merge_data.apply(
        lambda x: x["iva"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_TOTAL"] = merge_data.apply(
        lambda x: x["total_item"] / x["venta_ask2"], axis=1
    )
    merge_data["USD_IGTF"] = merge_data.apply(
        lambda x: x["igtf"] / x["venta_ask2"], axis=1
    )
    print("monto_base_item:", round(merge_data["monto_base_item"].sum(), 2))
    print("total_item:", round(merge_data["total_item"].sum(), 2))
    merge_data["saldo_total_doc"] = merge_data.apply(
        lambda x: x["total_item"] if x["saldo_total_doc"] != 0.0 else 0.0, axis=1
    )
    print("saldo_total_doc:", round(merge_data["saldo_total_doc"].sum(), 2))
    print("USD_BASE:", round(merge_data["USD_BASE"].sum(), 2))
    print("USD_TOTAL:", round(merge_data["USD_TOTAL"].sum(), 2))
    merge_data["saldo_total_doc$"] = merge_data.apply(
        lambda x: x["USD_TOTAL"] if x["saldo_total_doc$"] != 0.0 else 0.0, axis=1
    )
    print("saldo_total_doc$:", round(merge_data["saldo_total_doc$"].sum(), 2))
    merge_data["USD_TOTAL"] = merge_data["USD_TOTAL"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_BASE"] = merge_data["USD_BASE"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_IVA"] = merge_data["USD_IVA"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["USD_IGTF"] = merge_data["USD_IGTF"].apply(
        "${:,.2f}".format
    )  # Se aplica formato de $ float
    merge_data["cli_des"] = merge_data["cli_des"].str[
        :50
    ]  # Extrae los primeros 50 caracteres de la izquierda
    return merge_data[campos_fact]


def conjunto_ref_mov_bcrios(fecha_inicio_mes):
    df = get_movbanco(fecha_inicio_mes)
    return set(df["doc_num"])


def get_monto_tasa_bcv_del_dia():
    df_data_bcv = p_est_bcv()  # archivo BCV
    fila_tasa_dia = df_data_bcv[df_data_bcv["fecha"] == df_data_bcv["fecha"].max()]
    return float(fila_tasa_dia["venta_ask2"].iloc[0])


def get_fecha_tasa_bcv_del_dia():
    df_data_bcv = p_est_bcv()  # archivo BCV
    return df_data_bcv["fecha"].iloc[0]


def get_monto_tasa_bcv_fecha(fecha_oper):
    fecha_operacion = to_datetime(fecha_oper)
    df_data_bcv = p_est_bcv()  # archivo BCV
    fila_tasa_dia = df_data_bcv[df_data_bcv["fecha"] == fecha_operacion]
    print("Tasa BCV al:", fila_tasa_dia["fecha"].iloc[0])
    return float(fila_tasa_dia["venta_ask2"].iloc[0])


def factura_compra_con_su_detalle(**kwargs):
    anio, mes = kwargs.get("anio", "2023"), kwargs.get("mes", "all")
    where_anio = "" if anio == "all" else f" AND year(fact.fec_reg)='{anio}'"
    where_all = "WHERE fact.[anulado]=0 " + where_anio
    where_mes = f"WHERE fact.[anulado]=0 AND year(fact.fec_reg)='{anio}' and month(fact.fec_reg)='{mes}'"
    where = where_all if mes == "all" else where_mes
    sql = f"""
          SELECT RTRIM(fact.doc_num) as doc_num, RTRIM(fact.nro_fact) as nro_fact, RTRIM(dfact.co_art) as co_art, RTRIM(art.campo1) as cod_art_izq,
                fact.fec_emis, fact.fec_reg, fact.fec_venc, fact.descrip,
                year(fact.fec_reg) AS anio, month(fact.fec_reg) AS mes, RTRIM(fact.co_prov) as co_prov,
                RTRIM(c.prov_des) as prov_des, (dfact.reng_neto-dfact.monto_desc_glob) AS monto_base_item,
                (dfact.monto_imp+dfact.monto_imp_afec_glob) as iva,
                ((dfact.reng_neto-dfact.monto_desc_glob)+(dfact.monto_imp+dfact.monto_imp_afec_glob)) as total_item,
                fact.otros1 as igtf, fact.saldo as saldo_total_doc
          FROM saFacturaCompra AS fact INNER JOIN saFacturaCompraReng AS dfact ON
                fact.doc_num = dfact.doc_num LEFT JOIN saArticulo AS art ON
                dfact.co_art = art.co_art LEFT JOIN saProveedor AS c ON fact.co_prov = c.co_prov
          {where}
          ORDER BY fact.fec_reg, fact.doc_num
          """
    fact_det = get_read_sql(sql, **dict_con_admin)
    fact_det["co_tipo_doc"] = "FACT"
    return fact_det


def get_last__nro_fact_venta():
    sql = """
            SELECT RTRIM(doc_num) as doc_num, RTRIM(n_control) as n_control
            FROM saFacturaVenta
            WHERE doc_num in (SELECT MAX(RTRIM(doc_num))
                              FROM saFacturaVenta)
          """
    return get_read_sql(sql, **dict_con_admin)


if __name__ == "__main__":
    print(get_id_movbanco(fecha_fin="20241231"))
