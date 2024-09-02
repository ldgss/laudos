from sqlalchemy.sql import text
from db import db

def log_user(usuario, password):
    try:
        sql = text("SELECT * FROM usuarios WHERE nombre = :usuario AND password = :password")
        result = db.db.session.execute(sql,{"usuario": usuario, "password": password})
        return result.fetchone()
    except Exception as e:
        return None