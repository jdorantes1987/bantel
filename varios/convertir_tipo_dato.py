import numpy as np
import pandas as pd

# Lee un archivo .xlsx
pagos = pd.read_excel("RepFormatoPago.xlsx")

pagos2 = pagos["mont_cob"].iloc[3:6].astype("float64")
print(pagos2.describe())
