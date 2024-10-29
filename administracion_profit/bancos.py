from datetime import date
from varios.utilidades import date_today
from accesos.data_base import insert_sql
from accesos.datos import dict_con_admin

# Día actual
d = date.today()

def new_movbanco(id_m, descrip, c_ingegr, fecha_emision, ref_bco, monto_mov, monto_idb):
    monto_d, monto_h = 0.0, 0.0
    if monto_mov < 0.0:
        monto_d = abs(monto_mov)
        tip_mov = 'TR'
    else:
        monto_h = monto_mov
        tip_mov = 'TP'
    strsql = "INSERT saMovimientoBanco (mov_num, descrip, cod_cta, co_cta_ingr_egr, fecha, tasa, tipo_op, doc_num, " \
             "monto_d, monto_h, idb, saldo_ini, origen, cob_pag, dep_num, conciliado, ori_dep, anulado, dep_con, " \
             "fec_con, cod_ingben, fecha_che, feccom, numcom, dis_cen, campo1, campo2, campo3, campo4, campo5, " \
             "campo6, campo7, campo8, co_us_in, co_sucu_in, fe_us_in, co_us_mo, co_sucu_mo, fe_us_mo) VALUES " \
             "('{id_Mov}', '{descr}', '0134', '{CIE}', '{fech_emi}', '1.0', '{t_mov}', '{ref_bcaria}', '{monto_deb}', " \
             "'{monto_hab}','{deb_bcario}', '0', 'BAN', NULL, NULL, '0', '0', '0', '0', NULL, NULL, '{fech_cheq}', " \
             "NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'JACK', '01', '{fech_ins}', " \
             "'JACK', '01', '{fech_mo}')".format(id_Mov=id_m, descr=descrip, CIE=c_ingegr, fech_emi=fecha_emision,
                                                 t_mov=tip_mov, ref_bcaria=ref_bco, monto_deb=monto_d, monto_hab=monto_h,
                                                 deb_bcario=monto_idb, fech_cheq=d, fech_ins=date_today(),
                                                 fech_mo=date_today())
    insert_sql(strsql, **dict_con_admin)



