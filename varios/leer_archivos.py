from pandas import read_csv, read_excel
from utilidades import search_df

# Lee un archivo .xlsx
pagos = read_excel("./varios/RepFormatoPago.xlsx")
# Lee un archivo .csv
docCompras = read_csv(
    "./varios/saDocumentoCompra.csv",
    delimiter=";",
    encoding="ISO-8859-1",
    on_bad_lines="skip",
)


print(pagos.info())
s = search_df("jackson", pagos)[
    ["co_tipo_doc", "co_prov", "prov_des", "mont_cob"]
].to_string()
print(s)
