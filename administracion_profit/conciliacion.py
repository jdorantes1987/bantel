from pandas import merge, read_excel

from accesos.datos import get_identificador_unicos
from accesos.files_excel import p_data_edo_cta_banesco as p_edo_cta_banesco
from contabilidad_profit.comprob import get_comprobantes

"""
    ES IMPORTANTE TENER EN CUENTA QUE ESTE MÓDULO SE CREÓ PARA REALIZAR UN ANÁLISIS POR MONTOS ENTRE 
    EL ESTADO DE CUENTA BANESCO Y LOS MOVIMIENTOS DE LA CUENTA DE BANCO BANESCO, CON LA FINALIDAD DE DETERMINAR
    AQUELLAS CIFRAS QUE NO SE CRUZAN EN AMBOS LISTADOS, PERMITIENDO IDENTIFICAR LAS PARTIDAS QUE
    CORRESPONDEN A ITF DE UNA MANERA MAS EFICIENTE.
"""


def get_edo_cta_con_identificador():
    lista_columnas = ["Fecha", "Referencia", "Descripción", "Monto", "identificador"]
    df_edo_cta = read_excel(p_edo_cta_banesco, dtype={"Referencia": str})
    df_edo_cta_sin_null = df_edo_cta[df_edo_cta["Fecha"].notnull()].copy()
    return get_identificador_unicos(df_edo_cta_sin_null, "Monto")[lista_columnas]


def get_comprobantes_con_identif(fecha_ini, fecha_fin):
    lista_columnas = ["fec_emis", "docref", "descri", "monto", "identificador"]
    df = get_comprobantes(
        cuenta="1.1.02.01.0003", fecha_desde=fecha_ini, fecha_hasta=fecha_fin
    )
    df["descri"] = df["descri"].str[
        :40
    ]  # Extrae los primeros 50 caracteres de la izquierda
    df["monto"] = df.apply(lambda x: x["monto_d"] - x["monto_h"], axis=1)
    df_monto_ident = get_identificador_unicos(df, "monto")
    return df_monto_ident[lista_columnas]


def conjunto_montos_por_identificar_en_edo_cta(fecha_ini, fecha_fin):
    conjunto_edo_cta = set(get_edo_cta_con_identificador()["identificador"])
    conjunto_comprobantes = set(
        get_comprobantes_con_identif(fecha_ini=fecha_ini, fecha_fin=fecha_fin)[
            "identificador"
        ]
    )
    return conjunto_edo_cta - conjunto_comprobantes


def conjunto_montos_por_identificar_en_comprobantes(fecha_ini, fecha_fin):
    conjunto_edo_cta = set(get_edo_cta_con_identificador()["identificador"])
    conjunto_comprobantes = set(
        get_comprobantes_con_identif(fecha_ini=fecha_ini, fecha_fin=fecha_fin)[
            "identificador"
        ]
    )
    return conjunto_comprobantes - conjunto_edo_cta


def partidas_por_identificar_edo_cta(fecha_ini, fecha_fin):
    mov_cta = (
        get_edo_cta_con_identificador()
    )  # Movimientos del edo cta banesco con el identificador unico en los montos
    # Al obtener las referencias repetidas en los mov de la cuenta, podré saber si el monto que no se cruza correponde al itf.
    cant_repeticiones_ref = mov_cta[
        "Referencia"
    ].value_counts()  # Cantidad de veces que se repiten los numeros de referencias bancarias
    # Obtiene las referencias que no se cruzan con el libro
    mov_edo_cta_banesco_ptes = mov_cta[
        mov_cta["identificador"].isin(
            conjunto_montos_por_identificar_en_edo_cta(
                fecha_ini=fecha_ini, fecha_fin=fecha_fin
            )
        )
    ]
    #  Combina el dataframe de los mov del edo cta banesco con la serie que contiene las repeticiones de las referencias bancarias
    mov_edo_cta_banesco_ptes2 = merge(
        mov_edo_cta_banesco_ptes,
        cant_repeticiones_ref,
        how="left",
        left_on="Referencia",
        right_on="Referencia",
    )
    mov_edo_cta_banesco_ptes2.rename(columns={"count": "count_ref"}, inplace=True)
    return mov_edo_cta_banesco_ptes2


def partidas_por_identificar_libro(fecha_ini, fecha_fin):
    mov_cta = get_comprobantes_con_identif(
        fecha_ini=fecha_ini, fecha_fin=fecha_fin
    )  # Movimientos de la cuenta contable banesco con el identificador unico en los montos
    # Al obtener las referencias repetidas en los mov de la cuenta, podré saber si el monto que no se cruza correponde al itf.
    cant_repeticiones_ref = mov_cta[
        "docref"
    ].value_counts()  # Cantidad de veces que se repiten los numeros de referencias bancarias
    # Obtiene las referencias que no se cruzan con el edo de cta
    mov_cta_banco_banesco_ptes = mov_cta[
        mov_cta["identificador"].isin(
            conjunto_montos_por_identificar_en_comprobantes(
                fecha_ini=fecha_ini, fecha_fin=fecha_fin
            )
        )
    ]
    #  Combina el dataframe de los mov de cuenta contable banesco con la serie que contiene las repeticiones de las referencias bancarias
    mov_cta_banco_banesco_pte2 = merge(
        mov_cta_banco_banesco_ptes,
        cant_repeticiones_ref,
        how="left",
        left_on="docref",
        right_on="docref",
    )
    mov_cta_banco_banesco_pte2.rename(columns={"count": "count_ref"}, inplace=True)
    return mov_cta_banco_banesco_pte2


if __name__ == "__main__":
    fecha_i, fecha_f = "20250101", "20250131"
    print(
        "Partidas por identificar edo. cta:\n",
        partidas_por_identificar_edo_cta(
            fecha_ini=fecha_i, fecha_fin=fecha_f
        ).to_string(),
    )
    partidas_por_identificar_edo_cta(fecha_ini=fecha_i, fecha_fin=fecha_f).to_excel(
        "partidas_por_identificar_edo_cta.xlsx"
    )
    print(
        "Partidas por identificar libro:\n",
        partidas_por_identificar_libro(
            fecha_ini=fecha_i, fecha_fin=fecha_f
        ).to_string(),
    )
    partidas_por_identificar_libro(fecha_ini=fecha_i, fecha_fin=fecha_f).to_excel(
        "partidas_por_identificar_libro.xlsx"
    )
