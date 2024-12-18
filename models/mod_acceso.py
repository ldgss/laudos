from sqlalchemy.sql import text
from db import db

def guardar_login(ip, dispositivo, id):
    try:
        sql = text("""
                    INSERT INTO
                    acceso
                    (ip, dispositivo, usuario, fecha_registro)
                    VALUES
                    (:ip, :dispositivo, :usuario, CURRENT_TIMESTAMP)
                """
                )
        
        acceso = db.db.session.execute(sql,
                                            {
                                                "ip" : ip,
                                                "dispositivo" : dispositivo,
                                                "usuario" : id
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None