from sqlalchemy.sql import text

def log_user(db, usuario, password):
    try:
        sql = text("SELECT * FROM usuarios WHERE nombre = :usuario AND password = :password")
        result = db.session.execute(sql,{"usuario": usuario, "password": password})
        print(result)
        return result.fetchone()
    except Exception as e:
        print(e)
        return None