import os

Ruta_base = "C:/Users/jdorantes/Documents"
Ruta_Rel = "../Documents/Analisis/Revision Contabilidad.xlsm"
Ruta_Sol = os.path.join(Ruta_base, Ruta_Rel)
Ruta_Salida = os.path.abspath(Ruta_Sol)
print("Ruta:", Ruta_Salida)
