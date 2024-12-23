import os

import pymysql

# from dotenv import load_dotenv
from pandas import NA, read_sql_query
from sqlalchemy import create_engine

from accesos.conexion import ConexionBD


# load_dotenv()
class ConexionBDMysql(ConexionBD):
    def __init__(self, **kwargs):
        super().__init__(
            **{
                k: kwargs.get(k, v)
                for k, v in {
                    "proveedor": "{MySQLdb}",
                    "host": os.getenv("HOST_PRODUCCION_MKWSP"),
                    "usuario": os.getenv("DB_USER_MKWSP"),
                    "pword": os.getenv("DB_PASSWORD_MKWSP"),
                    "base_de_datos": os.getenv("DB_NAME_MKWSP"),
                }.items()
            }
        )
        self.url_conexion = (
            f"mysql+mysqlconnector://{self.usuario}:{self.clave}@{self.servidor}/"
            f"{self.bddatos}?auth_plugin=mysql_native_password"
        )

    def conectar(self):
        try:
            self.conn = pymysql.connect(
                host=self.servidor,
                user=self.usuario,
                password=self.clave,
                database=self.bddatos,
            )

            # print("Conexión exitosa a la base de datos.")
        except pymysql.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        if self.conn:
            self.conn.close()
            # print("Conexión cerrada.")

    def get_read_sql(self, sql):
        try:
            datos = read_sql_query(sql, create_engine(self.url_conexion))
        except Exception as e:
            datos = NA
            print("Ocurrió un error al consultar: ", e)
        return datos


# Ejemplo de uso:
# conexion = ConexionBDMysql()
# conexion.conectar()
# Realiza operaciones en la base de datos...
# conexion.desconectar()
