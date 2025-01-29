from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from flask import session
import shlex
import traceback

def get_fleteros():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                select cod_mae, den, cod_cls
                from genmae
                where 
                lower(cod_cls) like '%flete%' or lower(cod_cls) like '%logis%' 
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None
  
def guardar_despacho():
    try:
        productos = []
        productos = [value for key, value in request.form.items() if key.startswith('numero_unico')]

        if productos:
            sql = text("""
                INSERT INTO despacho
                    (mercaderia, hojalata, extracto, reacondicionado, 
                    fletero_codigo, fletero_nombre, 
                    observaciones, responsable, fecha_registro)
                VALUES
                    (:mercaderia, :hojalata, :extracto, :reacondicionado, 
                    :fletero_codigo, :fletero_nombre, 
                    :observaciones, :responsable, CURRENT_TIMESTAMP)
            """)

            for producto in productos:
                db.db.session.execute(sql, {
                    "mercaderia" : producto if 'T1' in producto else None,
                    "hojalata" : producto if 'H1' in producto else None,
                    "extracto" : producto if 'E1' in producto else None,
                    "reacondicionado" : producto if 'T2' in producto else None,
                    "fletero_codigo" : request.form["fletero_codigo"],
                    "fletero_nombre" : request.form["fletero_nombre"],
                    "observaciones" : request.form["observaciones"],
                    "responsable" : session["id"],
                })

            db.db.session.commit()

        return True
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()  # Obtiene la traza completa del error
        print(f"Error: {error_message}")  # Imprime toda la información
        return None
    
def get_listado_despacho(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"d.mercaderia::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.hojalata::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.extracto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.reacondicionado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.fletero_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.fletero_nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"d.fecha_registro::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.nueva_den::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
                d.id as despacho_id,
                d.mercaderia, 
                d.hojalata, 
                d.extracto, 
                d.reacondicionado, 
                m.den as mden,
                e.den as eden,
                h.den as hden,
                r.nueva_den as rnueva_den,
                d.fletero_codigo, 
                d.fletero_nombre, 
                d.observaciones, 
                u.nombre, 
                d.fecha_registro
            FROM despacho d
            JOIN usuario u ON d.responsable = u.id
            left JOIN mercaderia m ON m.numero_unico = d.mercaderia
            left JOIN extracto e ON e.numero_unico = d.extracto
            left JOIN hojalata h ON h.numero_unico = d.hojalata
            left JOIN reacondicionado r ON r.numero_unico = d.reacondicionado
            WHERE {condicion_final_ilike}
            ORDER BY d.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                        d.id as despacho_id,
                                        d.mercaderia, 
                                        d.hojalata, 
                                        d.extracto, 
                                        d.reacondicionado, 
                                        m.den as mden,
                                        e.den as eden,
                                        h.den as hden,
                                        r.nueva_den as rnueva_den,
                                        d.fletero_codigo, 
                                        d.fletero_nombre, 
                                        d.observaciones, 
                                        u.nombre, 
                                        d.fecha_registro
                                    FROM despacho d
                                    JOIN usuario u ON d.responsable = u.id
                                    left JOIN mercaderia m ON m.numero_unico = d.mercaderia
                                    left JOIN extracto e ON e.numero_unico = d.extracto
                                    left JOIN hojalata h ON h.numero_unico = d.hojalata
                                    left JOIN reacondicionado r ON r.numero_unico = d.reacondicionado
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
    
def anular_despacho():
    # CUIDADO - DANGER - DELETE ZONE
    try:
        anulacion = text("""
                    DELETE FROM despacho
                    WHERE id=:id;
                """
                )
        anulacion = db.db.session.execute(anulacion,
                                            {
                                                "id": request.form["despacho_id"]                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None