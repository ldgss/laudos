from sqlalchemy.sql import text
from db import db
from flask import request
from flask import session
import shlex
from flask import current_app as app
import traceback
    
def guardar_anulacion():
    try:
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

        if numero_unico and 'T1' in numero_unico:
            deletion_sql = text("""DELETE FROM mercaderia WHERE numero_unico=:numero_unico""")
        elif numero_unico and 'H1' in numero_unico:
            deletion_sql = text("""DELETE FROM hojalata WHERE numero_unico=:numero_unico""")
        elif numero_unico and 'E1' in numero_unico:
            deletion_sql = text("""DELETE FROM extracto WHERE numero_unico=:numero_unico""")
        
        deletion_params =   {
                                "numero_unico": request.form["numero_unico"]
                            }

        db.db.session.execute(deletion_sql, deletion_params)
        db.db.session.execute(insertion_sql, insertion_params)
        db.db.session.commit()
        
        return True
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