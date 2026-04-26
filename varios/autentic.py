import accesos.data_base as db


def aut_user(user, pw):

    sql = f"""
          select * from usuarios where idusuario ='{user}' and PWDCOMPARE('{pw}', passw)= 1
          """
    users = db.get_read_sql(sql, host="10.22.22.3")
    #     print(users)
    return users


if __name__ == "__main__":
    # Ejemplo de uso
    user = "jdorantes"
    pw = "1832911"
    result = aut_user(user, pw)
    print(result)
