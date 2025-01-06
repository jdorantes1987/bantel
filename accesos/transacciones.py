class GestorTransacciones:
    #  Se le pasa como parámetro un objeto conexión
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def iniciar_transaccion(self):
        self.conexion.conn.autocommit = False

    def confirmar_transaccion(self):
        self.conexion.conn.commit()
        self.conexion.conn.autocommit = True

    def revertir_transaccion(self):
        self.conexion.conn.rollback()
        self.conexion.conn.autocommit = True

    def get_cursor(self):
        try:
            cursor = self.conexion.conn.cursor()
        except Exception as e:
            print("Error al crear cursor: ", e)
        return cursor


## Ejemplo de uso:
# conexion = cnn.ConexionBD(host='10.22.22.3') #  Crea un objeto conexión
# conexion.conectar()  # inicia la conexión
# gestor = GestorTransacciones(conexion)
# gestor.iniciar_transaccion()
# cursor = gestor.get_cursor()
# try:
#     # Realiza operaciones en la base de datos...
#     strsql = "INSERT INTO saColor (co_color ,des_color ,co_us_in ,co_sucu_in ,fe_us_in ,co_us_mo ,co_sucu_mo ,fe_us_mo) VALUES ('00002' ,'prueba' ,'999' ,'01' ,'2024-04-22' ,'999' ,'01' ,'2024-04-22')"
#     cursor.execute(strsql)
#     strsql2 = "INSERT INTO saColor (co_color ,des_color ,co_us_in ,co_sucu_in ,fe_us_in ,co_us_mo ,co_sucu_mo ,fe_us_mo) VALUES ('00003' ,'prueba' ,'999' ,'01' ,'2024-04-22' ,'999' ,'01' ,'2024-04-22')"
#     cursor.execute(strsql2)
#     gestor.confirmar_transaccion()
#     print("Transacción confirmada.")
# except Exception as e:
#     gestor.revertir_transaccion()
#     print(f"Error en la transacción: {e}")
# finally:
#     conexion.desconectar()

# print('Listo')
