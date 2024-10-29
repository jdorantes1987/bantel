import datetime
import urllib.request
import pandas as pd
from pandas import to_datetime
# ----------------------------------------------------------------------------------------------------------------------
# ruta = "https://onedrive.live.com/download?resid=4B273DC2C3014B9E%2118937&authkey=!AIAl7jewXs44QbI&em=2"
# file_name, headers = urllib.request.urlretrieve(ruta)
file_name = '.\celulas\Registro Ofrendas_Python.xlsx'
today = datetime.datetime.now()
df1 = pd.read_excel(file_name, sheet_name="T_Liderazgo")

