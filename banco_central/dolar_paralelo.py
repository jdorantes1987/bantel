import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

import varios.utilidades as ut
from accesos.files_excel import p_data_estadisticas_par as p_est_par

url_base = "https://itsca.net/app/util/historico1.php?pagina="


#  DESCARGA LA INFORMACIÓN DE LAS TASAS DE CAMBIO
def bajar_data_dolar_par():
    df_arr_pg = []
    for i in range(1, 2, 1):
        pagina = i
        url = url_base + "{pag}".format(pag=pagina)
        cols = ["fecha", "venta_ask2"]
        session_obj = requests.Session()
        response = session_obj.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        all_tables = pd.read_html(
            response.text, header=0
        )  # header=0 indica que la lista tiene encabezados
        response.close()
        df_arr_pg.append(all_tables[0])
        print("se descargo:", url)
    df = pd.concat(df_arr_pg, axis=0, ignore_index=True)
    data = df.rename(
        columns={"Fecha": "fecha", "Precio": "venta_ask2"}
    )  # Renombrar o cambiar nombres a las columnas
    data["var_tasas"] = data["venta_ask2"].diff(
        periods=-1
    )  # Permite calcular la diferencia que existe entre el valor de la celda actual con respecto a la anterior
    data.to_excel("tasas_Par.xlsx")


# ACTUALIZA EL HISTÓRICO DE TASAS CON LA ÚLTIMA PUBLICACIÓN
def get_data_usd_par_web_last_qt():
    df_arr_pg = []
    for i in range(1, 2, 1):
        pagina = i
        url = url_base + "{pag}".format(pag=1)
        cols = ["fecha", "venta_ask2"]
        session_obj = requests.Session()
        response = session_obj.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        all_tables = pd.read_html(
            response.text, header=0
        )  # header=0 indica que la lista tiene encabezados
        response.close()
        df_arr_pg.append(all_tables[0])
        print("se descargo:", url)
    df = pd.concat(df_arr_pg, axis=0, ignore_index=True)
    data = df.rename(
        columns={"Fecha": "fecha", "Precio": "venta_ask2"}
    )  # Renombrar o cambiar nombres a las columnas
    # Permite calcular la diferencia que existe entre el valor de la celda actual con respecto a la anterior
    data["var_tasas"] = data["venta_ask2"].diff(periods=-1)
    data["fecha"] = pd.to_datetime(
        data["fecha"], dayfirst=True
    )  # convierte a fecha formato datetime
    return data


# Actualiza el archivo tasas_Par.xlsx
def actulizar_file_tasas():
    df_file_tasa = datos_estadisticas_tasas()
    df_file_tasa_new = get_data_usd_par_web_last_qt()
    new_file_tasa = [df_file_tasa_new, df_file_tasa]
    df = pd.concat(new_file_tasa).reset_index(drop=True)
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.day
    df["mes_"] = df["mes"].apply(lambda x: ut.month(x))
    df["var_tasas"] = df["venta_ask2"].diff(periods=-1)
    dolar_par_max_diario = df.set_index("fecha").resample("1D").max()
    dolar_par_max_diario["fecha"] = (
        dolar_par_max_diario.index
    )  # Convierte los valores de los indices a columna
    dolar_par_max_diario = dolar_par_max_diario[
        ["fecha", "venta_ask2", "var_tasas", "año", "mes", "dia", "mes_"]
    ]  # Reordenación de columnas
    data = dolar_par_max_diario.reset_index(drop=True)
    data_sort = data.sort_values(by=["fecha"], ascending=[False]).reset_index(drop=True)
    # data_sort.to_excel(ruta_file_data_estadist_par)


def datos_estadisticas_tasas():
    hist_tc = pd.read_excel(p_est_par)
    hist_tc = hist_tc.drop(hist_tc.columns[0], axis=1).reset_index(
        drop=True
    )  # Elimina la primera columna del dataframe
    hist_tc["fecha"] = pd.to_datetime(hist_tc["fecha"])
    return hist_tc


#  PREPARA EL ARCHIVO DE HISTÓRICO DE TASAS DEL DOLAR PARALELO
def preparar_file_estadisticas_tasas():
    hist_tc = pd.read_excel(p_est_par)
    hist_tc["fecha"] = pd.to_datetime(hist_tc["fecha"])
    hist_tc = hist_tc.drop(hist_tc.columns[0], axis=1).reset_index(
        drop=True
    )  # Elimina la primera columna del dataframe
    dolar_par_max_diario = hist_tc.set_index("fecha").resample("1D").max()
    dolar_par_max_diario["fecha"] = (
        dolar_par_max_diario.index
    )  # Convierte los valores de los indices a columna
    dolar_par_max_diario = dolar_par_max_diario[
        ["fecha", "venta_ask2"]
    ]  # Reordenación de columnas
    data = dolar_par_max_diario.reset_index(drop=True)
    data_sort = data.sort_values(by=["fecha"], ascending=[False]).reset_index(drop=True)
    # Permite calcular la diferencia que existe entre el valor de la celda actual con respecto a la anterior
    data_sort["var_tasas"] = data_sort["venta_ask2"].diff(periods=-1)
    data_sort.to_excel(p_est_par)


def variacion_tasas_por_dia():
    df = datos_estadisticas_tasas()
    return df


def grafic(anio, valores_eval):
    var_tasa = variacion_tasas_por_dia()
    df = var_tasa[var_tasa["año"] == anio]
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(16, 7))
    multi = sns.lineplot(
        x="fecha",
        y=valores_eval,
        hue="año",
        marker="o",
        linewidth=0.7,
        data=df,
        palette="deep",
    )  # crest
    plt.xticks(rotation=90)
    plt.title("Variación Tasas Dólar paralelo", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.show()
