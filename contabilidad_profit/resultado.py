from accesos.files_excel import p_data_revision_contabilidad as p_rev_contab
from pandas import read_excel
from pandas import DataFrame, melt, Categorical, pivot_table
from numpy import nan
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

def get_data_resultado_x_mes():
    df = read_excel(p_rev_contab, sheet_name='rptBalance')
    df2 = df[df['Tipo'] == 'NOMINAL']  # Filtra sólo las cuentas nominales
    balance_comprob = df2.replace(nan, 0)  # Remplaza los valores nan con ceros
    return balance_comprob

def unpivot_resultado_mes():
    df = get_data_resultado_x_mes()
    columnas = df.columns[5:]
    unpivot = melt(df, value_vars=columnas)  # Convierte las columnas de meses a filas con su valor asociado
    unpivot.rename(columns={'variable': 'mes', 'value': 'monto'}, inplace=True)
    return unpivot

def resultado_x_mes():
    df = unpivot_resultado_mes()
    df2 = df.groupby(['mes'])['monto'].aggregate(['sum']).reset_index()
    meses_ordenados = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    # Ordena el Dataframe por la columna nombre de mes
    df2['mes'] = Categorical(df2['mes'], categories=meses_ordenados, ordered=True)
    df_ordenado = df2.sort_values('mes')
    return df_ordenado

def resultado_graf_map_calor():
    resultado = resultado_x_mes()
    flights_df = pivot_table(resultado, values='sum', observed=True, index=['mes'], aggfunc='sum', sort=False)
    fig, ax = plt.subplots(figsize=(5, 6))
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F56536419%2Fhow-to-set-center-color-in-heatmap&psig=AOvVaw04rJIwSI0sMTuAK81_IEcN&ust=1705611191624000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIis_P2m5YMDFQAAAAAdAAAAABAD
    # create seaborn heatmap, usar parametro center=True para colocar derivados de un color
    # rdgn = sns.diverging_palette(h_neg=130, h_pos=10, s=99, l=55, sep=3, as_cmap=True)
    rdgn = sns.diverging_palette(133, 10, as_cmap=True)
    min = flights_df['sum'].min() if flights_df['sum'].min() != 0.0 else -0.1 
    max = flights_df['sum'].max() if flights_df['sum'].max() != 0.0 else 0.1
    
    offset = mcolors.TwoSlopeNorm(vmin=min, vcenter=0.0, vmax=max)
    sns.heatmap(flights_df, cmap=rdgn, annot_kws={'size': 11}, norm=offset, annot=True, fmt=',.2f',
                linewidths=0.5, cbar=True, cbar_kws={'format': '%.0f', "shrink": 1}, ax=ax)
    title = "Resultado del ejercicio por mes - (Derecha) \n Total resultado anual {:,.2f} \n".format(flights_df['sum'].sum())
    plt.title(title, fontsize=12)
    ttl = ax.title
    ttl.set_position([0.5, 0.5])
    plt.show()


resultado_graf_map_calor()
