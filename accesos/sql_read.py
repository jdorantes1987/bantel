from pandas import DataFrame
from pandas import read_sql_query
from pandas import NA
from sqlalchemy import text
from accesos.conexion import ConexionBD

def get_read_sql(sql, **kwargs) -> DataFrame:  
    try:
        conex = ConexionBD(**kwargs)
        engine = conex.c_engine()
        df = read_sql_query(text(sql), engine)
    except Exception as e:
        df = NA
        print("Ocurrió un error al consultar: ", e)
    return df