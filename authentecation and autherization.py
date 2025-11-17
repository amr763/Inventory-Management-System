default_user_name = "admin"
default_password = "Admin1236"
def  hash_password(password):
    import hashlib

    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

def compare(hashed_password, password):
    
    import hashlib

    return hashed_password == hashlib.sha256(password.encode()).hexdigest()

def user_login(username, password):
    if username==default_user_name and password==default_password:
        return True , "admin"

    import sqlite3 as sql

    dp = sql.connect('database.db')
    cr = dp.cursor()
    cr.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cr.fetchone()
    dp.close()
    if result:
        stored_hashed_password = result[0]
        if compare(stored_hashed_password, password):
            cr.execute("SELECT role FROM users WHERE username=?", (username,))
            role_result = cr.fetchone()
            return True, role_result[0]
    return False, None
               


def add_user(username, password, role):
    if role not in ['admin', 'user']:
        raise ValueError("Role must be either 'admin' or 'user'")
    if username.isalpha() == False:
        raise ValueError("Username must contain only alphabetic characters")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    import sqlite3 as sql

    dp = sql.connect('database.db')
    cr = dp.cursor()

    hashed_password = hash_password(password)
    cr.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    dp.commit()
    dp.close()

def change_password(username, old_password, new_password):
    if len(new_password) < 8:
        raise ValueError("New password must be at least 8 characters long")
    
    import sqlite3 as sql

    dp = sql.connect('database.db')
    cr = dp.cursor()

    cr.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cr.fetchone()
    if result:
        stored_hashed_password = result[0]
        if compare(stored_hashed_password, old_password):
            new_hashed_password = hash_password(new_password)
            cr.execute("UPDATE users SET password=? WHERE username=?", (new_hashed_password, username))
            dp.commit()
            dp.close()
            return True
    dp.close()
    return False
