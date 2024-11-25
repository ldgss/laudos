from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
from flask import session

def get_ultimo_id():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM reacondicionado
                    ORDER BY id DESC
                    LIMIT 1
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        ultimo_id = result.scalar()
        
        if not ultimo_id:
            # si es el primer pallet
            year = datetime.now().year
            return f"{year}-T2-000000"
        else:
            # si ya existen pallets, aumentar el numero del id
            prefijo = ultimo_id[:-6]
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = prefijo + nuevo_numero_str
            return nuevo_codigo
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_ubicacion_nombre():
    try:
        sql = text("""
                    SELECT *
                    FROM ubicacion_nombre
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        return result.mappings().all()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_vencimiento(form):
    try:
        sql = text("""
                    SELECT *
                    FROM vencimiento
                    WHERE producto = :producto
                    ORDER BY id DESC;
                """
                )
        
        vencimiento = db.db.session.execute(sql,{"producto": form["cod_cls"]})
        return vencimiento.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def guardar_ubicaciones():
    try:
        reacondicionado = text("""
                    INSERT INTO
                    ubicacion
                    (ubicacion_fila, mercaderia, hojalata, extracto, 
                    responsable, fecha_registro, insumo_envase, ubicacion_profundidad, ubicacion_altura, reacondicionado)
                    VALUES
                    (:ubicacion_fila, :mercaderia, :hojalata, :extracto, 
                    :responsable, CURRENT_TIMESTAMP, :insumo_envase, :ubicacion_profundidad, :ubicacion_altura, :reacondicionado)
                """
                )
        print(request.form)
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "ubicacion_fila": request.form["id_ubicacion"],
                                                "mercaderia": request.form["numero_unico"] if 'T1' in request.form["numero_unico"] else None,
                                                "reacondicionado": request.form["numero_unico"] if 'T2' in request.form["numero_unico"] else None,
                                                "hojalata": request.form["numero_unico"] if 'H1' in request.form["numero_unico"] else None,
                                                "extracto": request.form["numero_unico"] if 'E1' in request.form["numero_unico"] else None,
                                                "responsable": session["id"],
                                                "insumo_envase": request.form["numero_unico"] if 'I1' in request.form["numero_unico"] else None,
                                                "ubicacion_profundidad": request.form["profundidad"],
                                                "ubicacion_altura": request.form["altura"],
                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_ubicaciones(numero_unico):
    try:
        sql = text("""
                    SELECT u.*, un.posicion, un.sector, us.nombre AS responsable_de_movimiento
                    FROM ubicacion u
                    JOIN ubicacion_nombre un ON u.ubicacion_fila = un.id
                    JOIN usuario us ON u.responsable = us.id
                    WHERE 
					    u.mercaderia = :numero_unico OR
						u.hojalata = :numero_unico OR
						u.extracto = :numero_unico OR
						u.insumo_envase = :numero_unico OR
						u.reacondicionado = :numero_unico
						ORDER BY u.fecha_registro DESC	
                """
                )
        
        result = db.db.session.execute(sql,{"numero_unico": numero_unico})
        result = result.mappings().all() or {}
        return result 
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_ubicaciones(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = terminos_de_busqueda.split()
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            # chequear cada termino en cada columna de mercaderia
            subcondicion.append(f"m.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en nombre reacondicionado
            subcondicion.append(f"r.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.nueva_den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.tipo_reacondicionado::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en nombre reacondicionado_detalle
            subcondicion.append(f"rd.fecha_registro::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        
        query_sql = f"""
            SELECT 
                r.*, 
                u.nombre AS responsable_nombre, 
                array_agg(json_build_object(
                    'mercaderia_id', m.id,
                    'numero_unico_original', m.numero_unico,
                    'producto', v.producto,
                    'meses', v.meses,
                    'detalle_id', rd.id
                )) AS detalles
            FROM reacondicionado r
            LEFT JOIN usuario u ON r.responsable = u.id
            RIGHT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
            LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
            LEFT JOIN vencimiento v ON v.id = m.vto
            WHERE {condicion_final_ilike}
            GROUP BY r.id, u.nombre
            LIMIT :limit OFFSET :offset;

        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT m.*, r.*, rd.*, v.meses, u.nombre, m.numero_unico AS numero_unico_original
                                    FROM reacondicionado r
                                    RIGHT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
                                    LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
                                    LEFT JOIN vencimiento v ON v.id = m.vto
                                    LEFT JOIN usuario u ON r.responsable = u.id
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