from sqlalchemy.sql import text
from db import db

def log_user(usuario, password):
    try:
        sql = text("""
                    SELECT u.*,
                    p.mercaderia, 
                    p.hojalata, 
                    p.ubicacion, 
                    p.bloqueo, 
                    p.usuario, 
                    p.despacho, 
                    p.insumo, 
                    p.extracto, 
                    p.acceso, 
                    p.motivo_bloqueo, 
                    p.permiso, 
                    p.vencimiento, 
                    p.responsable, 
                    p.fecha_registro,
                    p.anulacion,
                    p.correccion,
                    p.materia
                    FROM usuario u
                    INNER JOIN permiso p ON u.id = p.responsable
                    WHERE u.nombre ILIKE :usuario AND u.password = :password;
                   """
                )
        
        result = db.db.session.execute(sql,{"usuario": usuario, "password": password})
        return result.mappings().first()
    except Exception as e:
        return None