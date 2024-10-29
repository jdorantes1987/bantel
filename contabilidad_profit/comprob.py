from accesos.data_base import get_read_sql
from accesos.data_base import insert_sql
from accesos.datos import dict_con_contab
from accesos.datos import get_identificador_unicos

def get_comprobantes(**kwargs):
    cuenta = kwargs.get('cuenta', '1.1.02.01.0003')
    fecha_desde = kwargs.get('fecha_desde', '2023-11-01')
    fecha_hasta = kwargs.get('fecha_hasta', '2023-11-30')
    strsql = "Select reng_num, fec_emis, descri, co_cue, RTRIM(docref) as docref, monto_d, monto_h " \
             "From scren_co " \
             "Where co_cue = '{cta}' and " \
             "fec_emis >= '{f_desde}' and " \
             "fec_emis <= '{f_hasta}'".format(cta=cuenta, f_desde=fecha_desde, f_hasta=fecha_hasta)
    return get_read_sql(strsql, **dict_con_contab)


def new_encab_comprobante(id_cbte, descrip, fecha_emision, fecha_insert, fecha_mod):
    strsql = "INSERT sccompro (comp_num, fec_emis, tipo, procesado, descrip, origen, inte_num, inte_num2, " \
             "aju_fis_ini, co_us_in, fe_us_in, co_us_mo, fe_us_mo, campo1, campo2, campo3, campo4, campo5, " \
             "campo6, campo7, campo8) VALUES ('{id_Cbte}', '{fech_emi}', 1, 0, '{descr}', " \
             "NULL, NULL, NULL, 0, 'JACK', '{fech_ins}', 'JACK  ', '{fech_mod}', " \
             "NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)".format(id_Cbte=id_cbte, fech_emi=fecha_emision,
                                                                      descr=descrip, fech_ins=fecha_insert,
                                                                      fech_mod=fecha_mod)
    insert_sql(strsql, **dict_con_contab)

def new_line_comprobante(id_cbte, fecha_emision, renglon, m_debe, m_haber, descrip, cod_cta, doc_refer, fecha_insert, fecha_mod, auxiliar):
    strsql = "INSERT scren_co (comp_num, fec_emis, reng_num, monto_h, monto_d, descri, docref, fec_doc, " \
             "co_cue, co_cen, co_mone, tasa, tipo_doc, co_aux, co_adi, co_adi2, co_adi3, cu_gasto, co_acti, " \
             "fec_ini_dep, regla, fec_desde, fec_hasta, monto_no_efectivo, monto_fis, monto_dpc, afecta_pm, " \
             "monto_exc_pm, co_sucu, co_cont, var_patri, afecta_efectivo, comp_num_aju, fec_emis_aju, reng_num_aju, " \
             "co_us_in, fe_us_in, co_us_mo, fe_us_mo) " \
             "VALUES ('{id_Cbte}', '{fech_emi}', '{reng}', {m_hab}, {m_deb}, " \
             "'{descr}', '{ref}', NULL, '{c_cta}', 'PPAL', 'BSS', 1.00000000, NULL, {aux}, NULL, " \
             "NULL, NULL, NULL, NULL, NULL,  NULL, NULL, NULL, 0.00, 0.00, 0.00, 0, 0.00, NULL, NULL, 0, 0, NULL, " \
             "NULL, NULL, 'JACK', '{fech_ins}', " \
             "'JACK', '{fech_mod}')".format(id_Cbte=id_cbte, fech_emi=fecha_emision, reng=renglon, c_cta=cod_cta,
                                            descr=descrip, m_deb=m_debe, m_hab=m_haber, fech_ins=fecha_insert,
                                            fech_mod=fecha_mod, aux=auxiliar, ref=doc_refer)
    insert_sql(strsql, **dict_con_contab)

def eliminar_comprobante(id_cbte):
    strsql = f"""
             DELETE 
             FROM sccompro 
             WHERE comp_num IN (SELECT c1.comp_num 
                               FROM sccompro as c1 
                               WHERE EXISTS(SELECT c2.comp_num 
                                            FROM sccompro as c2 
                                            WHERE c1.comp_num=c2.comp_num AND c2.comp_num={id_cbte}));
             """
    insert_sql(strsql, **dict_con_contab)

# param_consulta = dict()
# param_consulta['cuenta'] = '1.3.05.01.0001'
# param_consulta['fecha_desde'] = '2023-01-01'
# param_consulta['fecha_hasta'] = '2023-12-31'
# print(get_comprobantes(**param_consulta).to_string())
