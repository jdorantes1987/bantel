import leer_json_chess_com as rj
import time

this_year = [('2019', '09'), ('2019', '10'), ('2019', '11'), ('2019', '12')]
all_months = []
for date in this_year:
    year = date[0]
    month = date[1]
    df = rj.get_data_by_month('JDorantes', year, month)
    all_months.append(df)
    time.sleep(10)
    print("Cargando data...")

all_months = rj.combine_months(all_months)
all_months = rj.drop_not_required_columns(all_months)
all_months = rj.create_wins_column(all_months)
all_months = rj.column_by_month(all_months)
# ver mi apertura más común
print(all_months[all_months["playing_as_white"] == 1].groupby(["first_move", "my_result"])["my_result"].count())
# Aquellas de mis oponentes

print(all_months[all_months["playing_as_white"] == 0].groupby(["first_move", "my_result"])["my_result"].count())
# acerca de estas aperturas y cómo respondo
print(all_months[(all_months["playing_as_white"] == 0) & ((all_months["first_move"] == "e2e4") | (all_months["first_move"] == "d2d4"))].groupby(["first_move", "response", "my_result"])["my_result"].count())
print(all_months.groupby(["month", "my_result"])["my_result"].count())






