import pandas as pd
import pyodbc
from utilidades import cnn_str_sql_server_admin

connection = pyodbc.connect(cnn_str_sql_server_admin())
try:
    print('Conexión exitosa')
    cursor = connection.cursor()
    sql_query = pd.read_sql_query('Select * from saDocumentoCompra', connection)
    print(sql_query)
    print(type(sql_query))
except Exception as ex:
    print(ex)
finally:
    connection.close()
    print('Conexión finalizada')

