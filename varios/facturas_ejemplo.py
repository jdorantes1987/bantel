import facturas_en_excel

print("Indique el libro a consultar:")
typedTipoDoc = input()
tabla = (
    "saDocumentoVenta" if typedTipoDoc == "v" else "saDocumentoCompra"
)  # Operador ternario 'if'
print(
    "Se imprimirá el ", "Libro de Ventas" if typedTipoDoc == "v" else "Libro de Compras"
)  # Operador ternario 'if'
facturas = facturas_en_excel.mes_actual_total(tabla)
print(facturas)
