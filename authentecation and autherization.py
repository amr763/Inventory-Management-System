def user_login(username, password):
    import sqlite3 as sql

    dp = sql.connect('database.db')
    cr = dp.cursor()

    cr.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cr.fetchone()

    dp.close()

    if result and result[0] == password:
        return True
    else:
        return False