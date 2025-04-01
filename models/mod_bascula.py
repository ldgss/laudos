from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from flask import session
import shlex
import traceback

# guardar devuelve el id para poder imprimir
# ya que no hay otro identificador

def guardar_bascula():
    try:
        sql = text("""
                    INSERT INTO public.bascula
                        (fecha, modo, chofer, 
                        dominio, ipm, peso, 
                        observaciones, responsable, fecha_registro)
                    VALUES
                        (:fecha, :modo, :chofer, 
                        :dominio, :ipm, :peso, 
                        :observaciones, :responsable, CURRENT_TIMESTAMP)
                    RETURNING id
                """
                )
        
        result = db.db.session.execute(sql,
                                            {
                                                "fecha": request.form["fecha"],
                                                "modo": request.form["modo"],
                                                "chofer": request.form["chofer"],
                                                "dominio": request.form["dominio"],
                                                "ipm": request.form["ipm"],
                                                "peso": request.form["peso"],
                                                "observaciones": request.form["observaciones"],
                                                "responsable": session["id"]
                                            }).fetchone()
        db.db.session.commit()
        return result[0]
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()  # Obtiene la traza completa del error
        print(f"Error: {error_message}")  # Imprime toda la información
        return None
    
def get_bascula(id):
    try:
        sql = text("""
                    SELECT 
                        b.id, b.fecha, b.modo, 
                        b.chofer, b.dominio, b.ipm, 
                        b.peso, b.observaciones, u.nombre as responsable, 
                        b.fecha_registro
                    FROM bascula b
                    join usuario u ON b.responsable = u.id
                    where b.id = :id
                    ;
                """
                )
        
        materia = db.db.session.execute(sql,{"id": id})
        return materia.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_bascula(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"b.fecha::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.modo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.chofer::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.dominio::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.ipm::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.peso::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.fecha_registro::TEXT ILIKE '%{termino}%'")
            
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT b.*, u.nombre as responsable
            FROM bascula b
            JOIN usuario u ON b.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY b.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT b.*, u.nombre as responsable
                                    FROM bascula b
                                    JOIN usuario u ON b.responsable = u.id
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