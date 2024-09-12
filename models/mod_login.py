from sqlalchemy.sql import text
from db import db

def log_user(usuario, password):
    try:
        sql = text("""
                    SELECT *
                    FROM usuario
                    FULL OUTER JOIN permiso ON usuario.id = permiso.responsable
                    WHERE usuario.nombre = :usuario AND usuario.password = :password;
                """
                )
        
        result = db.db.session.execute(sql,{"usuario": usuario, "password": password})
        return result.mappings().first()
    except Exception as e:
        return None