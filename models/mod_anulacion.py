from sqlalchemy.sql import text
from db import db
from flask import request
from flask import session
import shlex
from flask import current_app as app
import traceback
from utils import helpers
    
def guardar_anulacion():
    try:
        with db.db.session.begin():
            insertion_sql = text("""
                        INSERT INTO
                        anulacion
                        (numero_unico, observaciones, responsable, fecha_registro)
                        VALUES
                        (:numero_unico, :observaciones, :responsable, CURRENT_TIMESTAMP)
                    """
                    )
            insertion_params =  {
                                    "numero_unico": request.form["numero_unico"],
                                    "observaciones": request.form["observaciones"],
                                    "responsable": session["id"]
                                }
            

            numero_unico = request.form.get("numero_unico")

            if numero_unico and 'T1' in numero_unico and helpers.authorized_to("mercaderia"):
                deletion_sql = text("""DELETE FROM mercaderia WHERE numero_unico=:numero_unico""")
            elif numero_unico and 'H1' in numero_unico and helpers.authorized_to("hojalata"):
                deletion_sql = text("""DELETE FROM hojalata WHERE numero_unico=:numero_unico""")
            elif numero_unico and 'E1' in numero_unico and helpers.authorized_to("mercaderia"):
                deletion_sql = text("""DELETE FROM extracto WHERE numero_unico=:numero_unico""")
            elif numero_unico and 'T2' in numero_unico and helpers.authorized_to("mercaderia"):
                # 1. devolver unicades
                form_items = list(request.form.items())[4:]  # Saltamos las primeras 4 claves fijas
                items = {}
                for key, value in form_items:
                    # key tiene formato: items[0][cantidad] o items[1][destino], etc.
                    parts = key.replace('items[', '').replace(']', '').split('[')  # ['0', 'cantidad']
                    if len(parts) == 2:
                        index, field = parts
                        if index not in items:
                            items[index] = {}
                        items[index][field] = value

                for item in items.values():
                    # cantidad es igual para todos
                    cantidad = int(item.get('cantidad', 0))
                    # destino es para T1 y E1, trae los numeros unicos
                    destino = item.get('destino')
                    # origen es para T2, trae los ids 
                    origen = item.get('origen')
                    original_mercaderia = True if "T1" in destino else False
                    original_extracto = True if "E1" in destino else False
                    
                    if original_mercaderia:
                        update_sql = text("""UPDATE mercaderia
                                SET cantidad= cantidad + :cantidad
                                WHERE numero_unico=:destino""")
                        update_params = {
                            "cantidad": cantidad,
                            "destino": destino
                        }
                    elif original_extracto:
                        update_sql = text("""UPDATE extracto
                                SET cantidad= cantidad + :cantidad
                                WHERE numero_unico=:destino""")
                        update_params = {
                            "cantidad": cantidad,
                            "destino": destino
                        }
                    else:
                        update_sql = text("""UPDATE reacondicionado_detalle
                                SET cantidad= cantidad + :cantidad
                                WHERE id=:origen""")
                        update_params = {
                            "cantidad": cantidad,
                            "origen": origen
                        }
                    db.db.session.execute(update_sql, update_params)
                # ahora borramos el T2
                deletion_sql = text("""DELETE FROM reacondicionado WHERE numero_unico=:numero_unico""")
                
            deletion_params =   {
                                    "numero_unico": request.form["numero_unico"]
                                }

            db.db.session.execute(deletion_sql, deletion_params)
            db.db.session.execute(insertion_sql, insertion_params)
        return True
    except Exception as e:
        db.db.session.rollback()
        error_traceback = traceback.format_exc()
        print(f"e: {e}")
        print(f"tb: {error_traceback}")
        app.logger.debug(f"e: {e}")
        app.logger.debug(f"tb: {traceback}")
        return False

def detalle_t2():
    try:
        query = text("""
                    select 
                    r.numero_unico,
                    r.nueva_den,
                    r.tipo_reacondicionado,
                    rd.cantidad,
                    m.numero_unico as m_nu_a_dev,
                    e.numero_unico as e_nu_a_dev,
                    rd2.id as rd2_id_a_dev,
                    r2.numero_unico as r_nu_a_dev,
                    m2.numero_unico as m_original,
                    e2.numero_unico as e_original 
                    from reacondicionado r 
                    inner join reacondicionado_detalle rd on r.id = rd.reacondicionado
                    left join mercaderia m on m.id = rd.mercaderia 
                    left join extracto e on e.id = rd.extracto
                    left join reacondicionado_detalle rd2 on rd2.id = rd.reacondicionado_detalle 
                    left join reacondicionado r2 on r2.id = rd2.reacondicionado 
                    left join mercaderia m2 on m2.id = rd2.mercaderia_original 
                    left join extracto e2 on e2.id = rd2.extracto_original 
                    where r.numero_unico = :numero_unico
                """
                )
        params = {
            "numero_unico": request.json.get("numero_unico")
        }
        resultado = db.db.session.execute(query, params)
        return [dict(row) for row in resultado.mappings().all()]
    except Exception as e:
        db.db.session.rollback()
        error_traceback = traceback.format_exc()
        print(f"e: {e}")
        print(f"tb: {error_traceback}")
        app.logger.debug(f"e: {e}")
        app.logger.debug(f"tb: {traceback}")
        return None

def get_listado_anulacion(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"a.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"a.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"a.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
            a.numero_unico,
            a.observaciones,
            a.responsable,
            a.fecha_registro,
            u.nombre
            FROM anulacion a
            JOIN usuario u ON a.responsable = u.id
            WHERE 
                {condicion_final_ilike}
            ORDER BY a.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                    a.numero_unico,
                                    a.observaciones,
                                    a.responsable,
                                    a.fecha_registro,
                                    u.nombre
                                    FROM anulacion a
                                    JOIN usuario u ON a.responsable = u.id
                                    WHERE 
                                        {condicion_final_ilike}
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