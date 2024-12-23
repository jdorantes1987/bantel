import urllib.request

import xlrd

file_name, headers = urllib.request.urlretrieve(
    "https://www.bcv.org.ve/sites/default/files/EstadisticasGeneral/2_1_2c23_smc.xls"
)
wb = xlrd.open_workbook(file_name)
sheets = wb.sheet_names()
print(sheets)

for i in range(len(sheets)):
    sh = wb.sheet_by_index(0)
    print(sheets[i])
