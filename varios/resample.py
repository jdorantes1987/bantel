"""
1 Frecuencias de Pandas
Pandas ofrece una variedad de cadenas de frecuencia, también conocidas como alias de desplazamiento, para definir la frecuencia de una serie temporal. A continuación, se muestran algunas cadenas de frecuencia comunes que se utilizan en Pandas:

'B' : Día hábil
'D' : Día del calendario
'W' : Semanal
'M' : Fin de mes
'BM' : Fin de mes comercial
'MS' : inicio del mes
'BMS' : Inicio del mes comercial
'Q' : Fin del cuarto
'BQ' : Fin del trimestre comercial
'QS' : Inicio del trimestre
'BQS' : Inicio del trimestre comercial
'A' o 'Y' : Fin de año
'BA' o 'BY' : Fin del año comercial
'AS' o 'YS' : Año de inicio
'BAS' o 'BYS' : Inicio del año comercial
'H' : Por hora
'T' o 'min' : Minuciosamente
'S' : En segundo lugar
'L' o 'ms' : Milisegundos
'U' : Microsegundos
'N' : Nanosegundos
Frecuencias personalizadas:
También puedes crear frecuencias personalizadas combinando frecuencias base, como:
'2D' : Cada 2 días
'3W' : Cada 3 semanas
'4H' : Cada 4 horas
'1H30T' : Cada 1 hora y 30 minutos
"""

from pandas import read_excel

df = read_excel('C:/Users/jdorantes/Documents/Analisis/Analisis Ventas.xlsm', sheet_name='saDocumentoVenta')
ventas = df[(df['anulado']==False) & (df['co_tipo_doc'].isin(['FACT', 'N/CR']))]
ventas.set_index('fec_emis', inplace=True) # ejemplo colocando la columna 'fec_emis' como indice del DataFrame
ventas_suma = ventas['saldo'].resample('BM').sum()  # BM para sumar todos los días hábiles del mes y M para todos los dias del mes
#  indicando la columna que tiene la serie de fechas
# ventas_suma = ventas.resample('BM', on='fec_emis')['saldo'].sum()  # BM para sumar todos los días hábiles del mes y M para todos los dias del mes
print(ventas_suma.to_string())