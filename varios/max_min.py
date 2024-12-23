import pandas as pd

f_pagos = pd.read_excel("RepFormatoPago.xlsx")

print('Obtiene el valor maximo de los montos en la columna "mont_doc"')
maxi_mont_doc = f_pagos["mont_doc"].max()
print(maxi_mont_doc)
print("Obtiene el indice dentro de la matriz del valor maximo de los documentos")
idMax_mont_doc = f_pagos["mont_doc"].idxmax()
print(idMax_mont_doc)
nroDocIdmax = f_pagos._get_value(
    idMax_mont_doc, "nro_doc"
)  # Obtiene el valor de la fila por indice
print(nroDocIdmax)
print("Obtiene la fila del valor maximo de la columna 'mont_doc'")
print(f_pagos.iloc[idMax_mont_doc])
