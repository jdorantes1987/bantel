import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar

# Lee un archivo .csv
docCompras = pd.read_csv("saDocumentoCompra.csv", delimiter=";", encoding='ISO-8859-1', on_bad_lines='skip')
docCompras['fec_reg'] = pd.to_datetime(docCompras['fec_reg'], dayfirst=True)
docCompras['mes'] = docCompras['fec_reg'].dt.month
docCompras['año'] = docCompras['fec_reg'].dt.year
docCompras['mes_l'] = docCompras['fec_reg'].dt.month_name(locale='es_ES.utf8')  # CONVIERTE EL MES DE LA FECHA A LETRAS
docCompras_n = docCompras[docCompras['co_tipo_doc'] == 'FACT']
print('\n' * 2)
print('Infomación esquema de las columnas')
print(docCompras_n.info())

print('\n' * 2)
print('Infomación de estadísticas básicas generales')
print(docCompras_n.describe())


def get_ventas():
    fact = docCompras_n.sort_values(by=['año', 'mes'], ascending=[True, True])
    return fact


def datos_ventas(imprimir_graf):
    vtas = get_ventas()
    vtas['total_neto'] = vtas['total_neto'].astype('float64')
    if imprimir_graf:
        # reshape flights dataeset in proper format to create seaborn heatmap
        flights_df = pd.pivot_table(vtas, values='total_neto', index=['mes_l'], columns=['año'], aggfunc='sum',
                                    sort=False)
        print('\n' * 1, flights_df)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(flights_df, linewidths=1.5, annot=True, cmap='RdYlGn', annot_kws={'size': 10}, fmt=',.2f')  # create seaborn heatmap, usar parametro center=True para colocar derivados de un color
        title = "Ventas BANTEL"
        plt.title(title, fontsize=12)
        ttl = ax.title
        ttl.set_position([0.5, 0.5])
        plt.show()


datos_ventas(True)

months = [month[:3] for month in calendar.month_name[1:]]
print(months)

print(calendar.monthrange(2023, 7)[1])

