import pandas as pd
from datetime import date

hoy = date.today()
docCompras = pd.read_csv("./varios/saDocumentoCompra.csv", delimiter=";", encoding='ISO-8859-1', on_bad_lines='skip')

docCompras['fec_reg'] = pd.to_datetime(docCompras['fec_reg'], dayfirst=True)

docCompras['año'] = docCompras['fec_reg'].apply(lambda x: x.year)
print(docCompras.info())

# Forma de crear y acceder a un Diccionario con fuente de datos (dataframe)
year_revenue_dict = docCompras.groupby(['año']).agg({'total_bruto': "mean"}).to_dict()
print(year_revenue_dict['total_bruto'][2023])


def mes_actual():
    doc = pd.DataFrame(docCompras)
    return doc[
        (
            (doc['co_tipo_doc'].str.contains('FACT'))
            | (doc['co_tipo_doc'].str.contains('N/CR'))
        )
    ]


def mes_actual_total():
    doc = pd.DataFrame(docCompras)
    facturas = doc[(doc['fec_reg'].dt.year == hoy.year) &
                   (doc['fec_reg'].dt.month == hoy.month) &
                   ((doc['co_tipo_doc'].str.contains('FACT')) | (doc['co_tipo_doc'].str.contains('N/CR')))]

    retiva = doc[(doc['co_tipo_doc'].str.contains('IVAN'))]

    # Agrupa los tipos de documentos
    totl_fact = facturas.groupby('co_tipo_doc')[['total_bruto', 'monto_imp', 'total_neto']].sum()
    totl_retiva = retiva.groupby('co_tipo_doc')[['total_bruto', 'monto_imp', 'total_neto']].sum()

    # Une los dos DataFrame
    # Con axix=1 indicamos que queremos unirlo por filas, si ponemos axis=0 se uniría por columnas.
    documentos = pd.concat([totl_fact, totl_retiva])

    for ind in documentos.index:
        if ind == 'N/CR':
            # Cambia a negativo los montos correspondientes a los documentos Notas de Crédito
            documentos.at[ind, 'total_bruto'] = - float(documentos['total_bruto'][ind])
            documentos.at[ind, 'monto_imp'] = - float(documentos['monto_imp'][ind])
            documentos.at[ind, 'total_neto'] = - float(documentos['total_neto'][ind])
    return documentos
