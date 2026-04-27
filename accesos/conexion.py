import os

import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

#  Valores por defecto
args = {
    "driver": "mssql+pyodbc",
    "proveedor": "{SQL Server}",
    "tipo_c": "odbc_connect",
    "host": os.getenv("HOST_PRODUCCION_PROFIT"),
    "puerto": "27017",
    "usuario": os.getenv("DB_USER_PROFIT"),
    "pword": os.getenv("DB_PASSWORD_PROFIT"),
    "base_de_datos": os.getenv("DB_NAME_DERECHA_PROFIT"),
}


class ConexionBD:
    def __init__(self, **kwargs):
        self.driver = kwargs.get("driver", args["driver"])
        self.proveedor = kwargs.get("proveedor", args["proveedor"])
        self.tipo_con = kwargs.get("tipo_c", args["tipo_c"])
        self.servidor = kwargs.get("host", args["host"])
        self.bddatos = kwargs.get("base_de_datos", args["base_de_datos"])
        self.usuario = kwargs.get("usuario", args["usuario"])
        self.clave = kwargs.get("pword", args["pword"])
        self.conn = None

    def conectar(self):
        try:
            self.conn = pyodbc.connect(
                f"DRIVER={{FreeTDS}};"
                f"SERVER={self.servidor};"
                f"PORT=1433;"
                f"DATABASE={self.bddatos};"
                f"UID={self.usuario};"
                f"PWD={self.clave};"
                f"TDS_Version=7.4;"  # Versión para SQL Server 2008 en adelante
                f"Mars_Connection=Yes;"
            )
            # print("Conexión exitosa a la base de datos.")
        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        if self.conn:
            self.conn.close()
            # print("Conexión cerrada.")

    def c_engine(self):
        url_sqlserver = (
            f"DRIVER={{FreeTDS}};"
            f"SERVER={self.servidor};"
            f"PORT=1433;"
            f"DATABASE={self.bddatos};"
            f"UID={self.usuario};"
            f"PWD={self.clave};"
            f"TDS_Version=7.4;"  # Versión para SQL Server 2008 en adelante
            f"Mars_Connection=Yes;"
        )
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": url_sqlserver}
        )
        return create_engine(connection_url)


# # Ejemplo de uso:
# conexion = ConexionBD()
# conexion.conectar()
# Realiza operaciones en la base de datos...
# conexion.desconectar()
