from accesos.datos import get_monto_tasa_bcv_del_dia, get_monto_tasa_bcv_fecha, get_fecha_tasa_bcv_del_dia

def get_tasa():
    # all_rates = currency.get_rate()  # obtener todas las tasas de cambio de moneda
    # usd_rate = currency.get_rate(currency_code=cod_moneda, prettify=False)  # obtener la tasa de cambio del dólar estadounidense sin símbolo de moneda
    usd_rate = get_monto_tasa_bcv_del_dia()
    return usd_rate

def get_tasa_fecha(fecha):
    return get_monto_tasa_bcv_fecha(fecha)

def get_date_value():
    # last_update = currency.get_rate(currency_code='Fecha')  # obtener la hora de la última actualización
    last_update = get_fecha_tasa_bcv_del_dia()
    return last_update

#  Obtener la cantidad de bolívares por la tasa establecida
def a_bolivares(cantidad):
    print('fecha {}'.format(get_date_value())) 
    tasa_dia= get_monto_tasa_bcv_del_dia()
    monto = round(tasa_dia * cantidad, 2)
    print('tasa del día {}'.format(tasa_dia)) 
    return monto

# Obtener la cantidad de Divisas entre la tasa establecida
def a_divisas(cantidad):
    print('fecha {}'.format(get_date_value())) 
    tasa_dia= get_monto_tasa_bcv_del_dia()
    monto = round(cantidad/float(tasa_dia), 2)
    print('tasa del día {}'.format(tasa_dia)) 
    return monto

def a_divisas_segun_fecha(monto_en_bs, fecha):
    # all_rates = currency.get_rate()  # obtener todas las tasas de cambio de moneda
    # usd_rate = currency.get_rate(currency_code=cod_moneda, prettify=False)  # obtener la tasa de cambio del dólar estadounidense sin símbolo de moneda
    usd_rate = get_monto_tasa_bcv_fecha(fecha)
    print('Valor tasa:', usd_rate)
    cant_usd = monto_en_bs / usd_rate
    return cant_usd
