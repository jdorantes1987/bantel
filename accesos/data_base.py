from pandas import NA, DataFrame, read_sql_query
from pyodbc import connect
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

#  Valores por defecto
args = {
    "driver": "mssql+pyodbc",
    "proveedor": "{SQL Server}",
    "tipo_c": "odbc_connect",
    "host": "10.100.104.11",
    "puerto": "27017",
    "usuario": "profit",
    "pword": "profit",
    "base_de_datos": "BANTEL_A",
}


def conexion(**kwargs):
    diver = kwargs.get("driver", args["driver"])
    tipo_con = kwargs.get("tipo_c", args["tipo_c"])
    serv = kwargs.get("host", args["host"])
    data_base = kwargs.get("base_de_datos", args["base_de_datos"])
    user = kwargs.get("usuario", args["usuario"])
    pword = kwargs.get("pword", args["pword"])
    driver_con = kwargs.get("proveedor", args["proveedor"])
    con_str = (
        f"DRIVER={driver_con};SERVER={serv};DATABASE={data_base};UID={user};PWD={pword}"
    )
    connection_url = URL.create(diver, query={tipo_con: con_str})
    return create_engine(connection_url)


def get_read_sql(sql, **kwargs) -> DataFrame:
    try:
        with conexion(**kwargs).begin() as conn:
            df = read_sql_query(text(sql), conn)
    except Exception as e:
        df = NA
        print("Ocurrió un error al consultar: ", e)
    finally:
        conn.close()
    return df


def insert_sql(strsql, **kwargs):
    proveedor = args["proveedor"]
    serv = kwargs.get("host", args["host"])
    data_b = kwargs.get("base_de_datos", args["base_de_datos"])
    usuario = args["usuario"]
    pword = args["pword"]
    str_conn = "DRIVER={prov};SERVER={host};DATABASE={db};UID={user};PWD={pw}".format(
        prov=proveedor, host=serv, db=data_b, user=usuario, pw=pword
    )
    conn = connect(str_conn)
    try:
        with conn.cursor() as cursor:
            cursor.execute(strsql)
            cursor.commit()
            print("Registro insertado!")
    except Exception as e:
        print("Ocurrió un error al insertar: ", e)
        print(strsql)
    finally:
        del cursor
        conn.close()
