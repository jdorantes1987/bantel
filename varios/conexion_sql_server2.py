import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from utilidades import cnn_str_sql_server_admin

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": cnn_str_sql_server_admin()})
engine = create_engine(connection_url)

with engine.begin() as conn:
    df = pd.read_sql_query(sa.text("Select * from saDocumentoCompra"), conn)
print(df)

print('\n' * 2, 'Filtrar dato por una columna "co_tipo_doc" y busca cual es el ultimo registro')
docCompras_filtrado = df[df['co_tipo_doc'] == 'AJPA  ']
print(docCompras_filtrado['nro_doc'].tail().max())

