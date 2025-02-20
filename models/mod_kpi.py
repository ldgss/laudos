from sqlalchemy.sql import text
from db import db
import traceback
from flask import jsonify

    
def get_listado_kpi(producto):
    try:
        if producto == 'extracto':
            sql = f"""
                SELECT 
                    e.id, 
                    e.numero_unico, 
                    e.producto as cod, 
                    e.den, 
                    e.lote, 
                    e.brix, 
                    e.numero_recipiente as recipiente, 
                    e.fecha_elaboracion as elaboracion, 
                    e.fecha_elaboracion + INTERVAL '1 month' * v.meses AS vto,
                    e.fecha_registro as registro,  
                    u.nombre as responsable,
                    e.observaciones
                FROM extracto e
                JOIN usuario u ON e.responsable = u.id
                JOIN vencimiento v ON v.id = e.vto_meses
                ORDER BY e.fecha_registro DESC
            """
        if producto == 'mercaderia':
            sql = f"""
                SELECT 
                    m.id, 
                    m.numero_unico, 
                    m.producto as cod, 
                    m.den, 
                    m.lote, 
                    m.cantidad, 
                    m.fecha_elaboracion as elaboracion, 
                    m.fecha_elaboracion + INTERVAL '1 month' * v.meses AS env_vto,
                    m.fecha_etiquetado as etiquetado,
                    m.fecha_etiquetado + INTERVAL '1 month' * v.meses AS etiq_vto,
                    m.fecha_registro as registro, 
                    u.nombre as responsable,
                    m.observacion 
                FROM mercaderia m
                JOIN usuario u ON m.responsable = u.id
                JOIN vencimiento v ON v.id = m.vto
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