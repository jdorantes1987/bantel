# import locale
# from pandas import options
from accesos.conexion_mkwsp import ConexionBDMysql

# options.display.float_format = '{:,.2f}'.format  # Configuramos separadores de miles y 2 decimales
# locale.setlocale(locale.LC_ALL, 'es_ES')

class DatosMikrowisp:

    def __init__(self):
            self.oconn = ConexionBDMysql()
            
    def clientes(self):
            self.oconn.conectar()
            return self.oconn.get_read_sql("Select * from usuarios")
    
    def clientes_aviso_user(self):
            self.oconn.conectar()
            sql = """SELECT u.id, u.nombre, u.codigo_cliente, avi.id, z.zona 
                     FROM usuarios AS u INNER JOIN (zonas AS z INNER JOIN tblavisouser AS avi ON z.id = avi.zona) ON u.id = avi.cliente
                  """
            return self.oconn.get_read_sql(sql)
    
        
            
    

# Ejemplo de uso:
# obj = DatosMikrowisp()
# print(obj.clientes())