from sqlalchemy.sql import text
from flask import session
from db import db
from datetime import datetime
import shlex
from flask import request
import traceback

def get_lineas_mantenimiento():
    try:
        sql = text("""
                    SELECT 
                    id, denominacion
                    FROM lineas_mantenimiento
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_tipo_de_fallo():
    try:
        sql = text("""
                    SELECT 
                    id, descripcion
                    FROM tipo_de_fallo
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None

def anular_energia():
    # CUIDADO - DANGER - DELETE ZONE
    try:
        anulacion = text("""
                    DELETE FROM mediciones_de_energia
                    WHERE id=:id;
                """
                )
        anulacion = db.db.session.execute(anulacion,
                                            {
                                                "id": request.form["energia_id"]                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None   

def guardar_energia():
    try:
        sql = text("""
                    INSERT INTO mediciones_de_energia
                    (electricidad_acometida_norte_kw, electricidad_acometida_este_kw, gas_natural_m3, 
                    agua_pozo_m3x100, agua_caldera1_m3, agua_caldera2_m3, 
                    agua_caldera3_m3, efluente_generado_m3, responsable, 
                    fecha_registro, observaciones)
                    VALUES(
                    :acometida_norte, :acometida_este, :gas_natural,
                    :agua_pozo, :agua_caldera_1, :agua_caldera_2, :agua_caldera_3,
                    :efluente_generado, :responsable, CURRENT_TIMESTAMP, :observaciones
                    )
                   RETURNING id;
                """
                )
        
        medicion = db.db.session.execute(sql,
                                            {
                                                "acometida_norte": request.form.get("acometida_norte"),
                                                "acometida_este": request.form.get("acometida_este"),
                                                "gas_natural": request.form.get("gas_natural"),
                                                "agua_pozo": request.form.get("agua_pozo"),
                                                "agua_caldera_1": request.form.get("agua_caldera_1"),
                                                "agua_caldera_2": request.form.get("agua_caldera_2"),
                                                "agua_caldera_3": request.form.get("agua_caldera_3"),
                                                "efluente_generado": request.form.get("efluente_generado"),
                                                "responsable": session["id"],
                                                "observaciones": request.form.get("observaciones")
                                            })
        new_id = medicion.scalar()
        db.db.session.commit()
        return new_id
    except Exception as e:
        db.db.session.rollback()
        error_traceback = traceback.format_exc()
        print(f"e: {e}")
        print(f"tb: {error_traceback}")
        return None
    
def get_energia(id_medicion_energia):
    try:
        sql = text("""
                    SELECT 
                    m.electricidad_acometida_norte_kw,
                    m.electricidad_acometida_este_kw,
                    m.gas_natural_m3,
                    m.agua_pozo_m3x100,
                    m.agua_caldera1_m3,
                    m.agua_caldera2_m3,
                    m.agua_caldera3_m3,
                    m.efluente_generado_m3,
                    u.nombre as responsable,
                    m.fecha_registro,
                    observaciones
                    FROM mediciones_de_energia m
                    inner join usuario u on u.id = m.responsable
                    WHERE m.id = :id
                """
                )
        
        medicion = db.db.session.execute(sql,{
                                                "id": id_medicion_energia
                                        })
        return medicion.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_estadisticas():
    try:
        sql = text("""
                    SELECT 
                    m.electricidad_acometida_norte_kw,
                    m.electricidad_acometida_este_kw,
                    m.gas_natural_m3,
                    m.agua_pozo_m3x100,
                    m.agua_caldera1_m3,
                    m.agua_caldera2_m3,
                    m.agua_caldera3_m3,
                    m.efluente_generado_m3,
                    u.nombre as responsable,
                    m.fecha_registro,
                    observaciones
                    FROM mediciones_de_energia m
                    inner join usuario u on u.id = m.responsable
                    ORDER BY m.id ASC
                    LIMIT 12;
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_energia(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            subcondicion.append(f"med.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"med.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")
        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
            med.id, 
            med.electricidad_acometida_norte_kw, 
            med.electricidad_acometida_este_kw, 
            med.gas_natural_m3, 
            med.agua_pozo_m3x100, 
            med.agua_caldera1_m3, 
            med.agua_caldera2_m3, 
            med.agua_caldera3_m3, 
            med.efluente_generado_m3, 
            med.fecha_registro, 
            med.observaciones, 
            u.nombre as responsable
            FROM mediciones_de_energia med
            JOIN usuario u ON med.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY med.id DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                    med.id, 
                                    med.electricidad_acometida_norte_kw, 
                                    med.electricidad_acometida_este_kw, 
                                    med.gas_natural_m3, 
                                    med.agua_pozo_m3x100, 
                                    med.agua_caldera1_m3, 
                                    med.agua_caldera2_m3, 
                                    med.agua_caldera3_m3, 
                                    med.efluente_generado_m3, 
                                    med.fecha_registro, 
                                    med.observaciones, 
                                    u.nombre as responsable
                                    FROM mediciones_de_energia med
                                    JOIN usuario u ON med.responsable = u.id
                                    WHERE {condicion_final_ilike}
                                ) AS total_count;
                            """

        total_resultados_scalar = db.db.session.execute(text(total_resultados)).scalar()
        total_paginas = total_resultados_scalar // resultados_por_pagina
        if total_resultados_scalar % resultados_por_pagina != 0:
            total_paginas += 1
        return [resultados.fetchall(), total_paginas]

    except Exception as e:
        print(f"Error: {e}")
        return None

    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de extracto
            subcondicion = []
            subcondicion.append(f"e.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.brix::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_recipiente::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT e.*, u.*, v.*
            FROM extracto e
            JOIN usuario u ON e.responsable = u.id
            JOIN vencimiento v ON e.vto_meses = v.id
            WHERE {condicion_final_ilike}
            ORDER BY e.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT e.*, u.*, v.*
                                    FROM extracto e
                                    JOIN usuario u ON e.responsable = u.id
                                    JOIN vencimiento v ON e.vto_meses = v.id
                                    WHERE {condicion_final_ilike}
                                ) AS total_count;
                            """

        total_resultados_scalar = db.db.session.execute(text(total_resultados)).scalar()
        total_paginas = total_resultados_scalar // resultados_por_pagina
        if total_resultados_scalar % resultados_por_pagina != 0:
            total_paginas += 1
        return [resultados.fetchall(), total_paginas]

    except Exception as e:
        print(f"Error: {e}")
        return None