from sqlalchemy.sql import text
from db import db
from datetime import datetime



def insert_bloqueados(form):
    try:
        sql = text("""
                    INSERT INTO
                    bloqueado
                   (mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones,   
                    responsable, fecha_registro)
                    VALUES
                    (:mercaderia, :hojalata, :extracto, :estado, :numero_planilla, :motivo, :observaciones,
                    :responsable, CURRENT_TIMESTAMP)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "mercaderia": form['id_unico'],
                                                "hojalata": form['id_unico'],
                                                "extracto": form['id_unico'],
                                                "estado": True,
                                                "numero_planilla": form['numero_planilla'],
                                                "motivo": form['Motivo'],
                                                "observaciones": form['observaciones'],
                                                "responsable": form['user_id'],
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_bloqueados(id_unico):
    try:
        sql = text("""
                    SELECT b.*, u.*
                    FROM bloqueado b
                    JOIN usuario u ON b.responsable = u.id
                    WHERE hojalata = :id_unico
                """
                )
        
        bloqueados = db.db.session.execute(sql,{"id_unico": id_unico})
        return bloqueados.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None