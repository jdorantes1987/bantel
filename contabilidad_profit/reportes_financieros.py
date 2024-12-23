import pandas as pd

from accesos.datos import get_monto_tasa_bcv_del_dia
from accesos.files_excel import p_data_revision_contabilidad as p_rev_contab

pd.options.display.float_format = (
    "   Bs.{:,.2f}".format
)  # Configuramos separadores de miles y 2 decimales


def edo_finan_por_niv():
    l_campos = [
        "co_base",
        "grupo",
        "descripcion_cod_base",
        "monto",
        "monto$",
        "es_detalle",
        "sum_x_grupo",
        "sum_x_grupo$",
        "porce_x_grupo",
        "descripcion_grupo",
    ]
    balance_comprob = pd.read_excel(p_rev_contab, sheet_name="rptBalance")
    pla_cue = pd.read_excel(p_rev_contab, sheet_name="pCuenta")
    pla_cue_ph = pd.merge(
        pla_cue,
        pla_cue,
        left_on="co_cuepadre",
        right_on="co_cue",
        suffixes=("_p", "_h"),
    )
    join = pd.merge(
        balance_comprob, pla_cue, how="left", left_on="co_cue", right_on="co_cue"
    )
    join1 = pd.merge(
        join, pla_cue_ph, how="left", left_on="co_cue", right_on="co_cue_p"
    )

    join1 = join1.rename(
        columns={
            "co_cue": "co_base",
            "detalle": "es_detalle",
            "co_cuepadre": "grupo",
            "des_cue_x": "descripcion_cod_base",
            "des_cue_h": "descripcion_grupo",
            "TOTAL": "monto",
        }
    )

    join1["sum_x_grupo"] = join1.apply(
        lambda x: (
            join1[(join1["co_base"].str[: len(x["co_base"])] == x["co_base"])][
                "monto"
            ].sum()
            if x["es_detalle"] is False
            else x["monto"]
        ),
        axis=1,
    )

    join1["porce_x_grupo"] = join1.apply(
        lambda x: (
            (x["monto"] / join1[join1["grupo"] == x["grupo"]]["monto"].sum())
            if x["es_detalle"] is True and x["sum_x_grupo"] != 0
            else (
                (
                    x["sum_x_grupo"]
                    / join1[(join1["co_base"] == x["grupo"])]["sum_x_grupo"].sum()
                )
                if (x["sum_x_grupo"] != 0) and len(x["co_base"]) != 2
                else x["sum_x_grupo"] / x["sum_x_grupo"] if x["sum_x_grupo"] != 0 else 0
            )
        ),
        axis=1,
    )

    tasa_dia = get_monto_tasa_bcv_del_dia()
    join1["monto$"] = join1["monto"].apply(lambda x: x / tasa_dia)
    join1["sum_x_grupo$"] = join1["sum_x_grupo"].apply(lambda x: x / tasa_dia)
    join1[["monto$", "sum_x_grupo$"]] = join1[["monto$", "sum_x_grupo$"]].apply(
        lambda x: x[["monto$", "sum_x_grupo$"]].apply("${:,.2f}".format), axis=1
    )  # Formato $ en varias columnas
    join1 = join1[l_campos]
    join1["porce_x_grupo"] = join1["porce_x_grupo"].apply("{:.2%}".format)
    print(join1.to_string())


edo_finan_por_niv()
