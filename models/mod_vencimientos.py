from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from flask import session
import shlex
import traceback


def get_vencimientos():
    try:
        sql = text("""
                    SELECT 
                        v.producto,
                        v.meses,
                        v.fecha_registro as ultima_actualizacion
                    FROM vencimiento v
                """
                )
        
        materia = db.db.session.execute(sql)
        return materia.mappings().all()
    except Exception as e:
        print(f"Error: {e}")
        return None