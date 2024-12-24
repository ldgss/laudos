from sqlalchemy.sql import text
from db import db
from flask import request
from flask import session

    
def guardar_anulacion():
    try:
        sql = text("""
                    INSERT INTO
                    anulacion
                    (numero_unico, observaciones, responsable, fecha_registro)
                    VALUES
                    (:numero_unico, :observaciones, :responsable, CURRENT_TIMESTAMP)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "numero_unico": request.form["numero_unico"],
                                                "observaciones": request.form["observaciones"],
                                                "responsable": session["id"]
                                            })
        db.db.session.commit()

        # CUIDADO - DANGER - DELETE ZONE
        if 'T1' in request.form["numero_unico"]:
            deletion_sql = text("""DELETE FROM mercaderia WHERE numero_unico=:numero_unico""")
            print(f"anulando mercaderia: {request.form["numero_unico"]}")
        elif 'H1' in request.form["numero_unico"]:
            deletion_sql = text("""DELETE FROM hojalata WHERE numero_unico=:numero_unico""")
            print(f"anulando hojalata: {request.form["numero_unico"]}")
        elif 'E1' in request.form["numero_unico"]:
            deletion_sql = text("""DELETE FROM extracto WHERE numero_unico=:numero_unico""")
            print(f"anulando extracto: {request.form["numero_unico"]}")
        elif 'I1' in request.form["numero_unico"]:
            deletion_sql = text("""DELETE FROM insumo_envase WHERE numero_unico=:numero_unico""")
            print(f"anulando insumo: {request.form["numero_unico"]}")
        
        deletion_params = db.db.session.execute(deletion_sql, 
                                                {"numero_unico": request.form["numero_unico"]
                                                })
        db.db.session.commit()
        
        # CUIDADO - DANGER - DELETE ZONE

        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_listado_anulacion(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = terminos_de_busqueda.split()
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