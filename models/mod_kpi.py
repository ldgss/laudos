from sqlalchemy.sql import text
from db import db
import traceback
from flask import jsonify

    
def get_listado_kpi(producto):
    try:
        if producto == 'extracto':
            sql = f"""
                SELECT e.*, u.nombre
                FROM extracto e
                JOIN usuario u ON e.responsable = u.id
                ORDER BY e.fecha_registro DESC
            """
        if producto == 'mercaderia':
            sql = f"""
                SELECT m.*, u.nombre
                FROM mercaderia m
                JOIN usuario u ON m.responsable = u.id
                ORDER BY m.fecha_registro DESC
            """
        if producto == 'hojalata':
            sql = f"""
                SELECT h.*, u.nombre
                FROM hojalata e
                JOIN usuario u ON h.responsable = u.id
                ORDER BY h.fecha_registro DESC
            """
        resultado = db.db.session.execute(text(sql)).mappings().all()
        resultado = [dict(row) for row in resultado]
        return jsonify(resultado)
    except Exception as e:
        print(f"Error: {e}")
        return None