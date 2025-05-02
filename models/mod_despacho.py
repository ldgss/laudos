from sqlalchemy.sql import text
from db import db
from flask import request
from flask import session
import shlex
import traceback
import re

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

        return {
            "status": True,
            "message": "Guardado exitoso"
        }
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()
        match = re.search(r'DETAIL: (.+)', error_message)
        detail_message = match.group(1) if match else "No DETAIL found"
        if 'Key' in detail_message:
            detail_message = re.sub(r"Key \(.*?\)=\((.*?)\) already exists.", r"\1 ya existe.", detail_message)
        return {
            "status": None,
            "message": detail_message
        }
       
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
            SELECT distinct on (d.id)
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
            left JOIN usuario u ON d.responsable = u.id
            left JOIN mercaderia m ON m.numero_unico = d.mercaderia
            left JOIN extracto e ON e.numero_unico = d.extracto
            left JOIN hojalata h ON h.numero_unico = d.hojalata
            left JOIN reacondicionado r ON r.numero_unico = d.reacondicionado
            WHERE {condicion_final_ilike}
            ORDER BY d.id DESC
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
                                    left JOIN usuario u ON d.responsable = u.id
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
    
def detalle_despacho():
    try:
        n = request.json.get("numeroUnico")
        sql = text("""
                    select 
                        /* despacho */
                        to_char(d.fecha_registro, 'YYYY-MM-DD HH24:MI') as despachado, 
                        /* mercaderia */
                        m.den as m_den,
                        m.lote as m_lote,
                        m.cantidad as m_cantidad,
                        /* hojalata */
                        h.den as h_den,
                        h.lote as h_lote,
                        h.cantidad as h_cantidad,
                        /* extracto */
                        e.den as e_den,
                        e.lote as e_lote,
                        e.cantidad as e_cantidad,
                        /* reacondicionado mercaderia */
                        m2.den as m2_den,
                        m2.lote as m2_lote,
                        m2.cantidad as m2_cantidad,
                        /* reacondicionado extracto */
                        e2.den as e2_den,
                        e2.lote as e2_lote,
                        e2.cantidad as e2_cantidad,
                        /* reacondicionado mercaderia rec */
                        m3.den as m3_den,
                        m3.lote as m3_lote,
                        m3.cantidad as m3_cantidad,
                        /* reacondicionado extracto rec */
                        e3.den as e3_den,
                        e3.lote as e3_lote,
                        e3.cantidad as e3_cantidad
                    from despacho d
                    full outer join mercaderia m on m.numero_unico = d.mercaderia
                    full outer join hojalata h on h.numero_unico = d.hojalata 
                    full outer join extracto e on e.numero_unico = d.extracto 
                    full outer join reacondicionado r on r.numero_unico = d.reacondicionado 
                    left join reacondicionado_detalle rd on rd.reacondicionado = r.id 
                    left join mercaderia m2 on m2.id = rd.mercaderia_original 
                    left join extracto e2 on e2.id = rd.extracto_original
                    left join reacondicionado_detalle rd2 on rd2.id = rd.reacondicionado_detalle
                    left join mercaderia m3 on m3.id = rd2.mercaderia_original 
                    left join extracto e3 on e3.id = rd2.extracto_original 
                    where 
                        coalesce(d.mercaderia, d.hojalata, d.extracto, d.reacondicionado, 
                                m.numero_unico, h.numero_unico, e.numero_unico, r.numero_unico) is not null and (
                            m.numero_unico = :mercaderia or
                            h.numero_unico = :hojalata or
                            e.numero_unico = :extracto or
                            r.numero_unico = :reacondicionado
                        )
                """
                )
        
        detalle = db.db.session.execute(sql, 
                                        {
                                            "mercaderia": n if 'T1' in n else None,
                                            "hojalata": n if 'H1' in n else None,
                                            "extracto": n if 'E1' in n else None,
                                            "reacondicionado": n if 'T2' in n else None
                                        }
                                        )
        detalle = [dict(row) for row in detalle.mappings().all()]
        return detalle
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()
        return error_message