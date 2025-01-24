from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from flask import session
import shlex
import traceback


def get_productores():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                select cod_mae, den, cod_cls from genmae
                where lower(cod_cls) like '%finca%' or cod_cls =  'AGRICO'  
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_variedades():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                select cod_mae, den, cod_cls 
                from genmae
                where 
                lower(cod_cls) like '%hm7883%'
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None
    
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
  
def guardar_materia():
    try:
        sql = text("""
                    INSERT INTO public.materia
                        (productor_codigo, productor_razon_social, productor_zona, 
                        productor_tipo_cosecha, fletero_codigo, fletero_nombre, 
                        fletero_patente_camion, fletero_patente_acoplado, fletero_chofer, 
                        variedad_codigo, variedad_nombre, variedad_codigo_acoplado, 
                        variedad_nombre_acoplado, responsable, fecha, 
                        fecha_registro, observacion)
                    VALUES
                        (:productor_codigo, :productor_razon_social, :productor_zona, 
                        :productor_tipo_cosecha, :fletero_codigo, :fletero_nombre, 
                        :fletero_patente_camion, :fletero_patente_acoplado, :fletero_chofer, 
                        :variedad_codigo, :variedad_nombre, :variedad_codigo_acoplado, 
                        :variedad_nombre_acoplado, :responsable, :fecha, 
                        CURRENT_TIMESTAMP, :observacion)
                    RETURNING id
                """
                )
        
        result = db.db.session.execute(sql,
                                            {
                                                "productor_codigo" : request.form["productor_codigo"], 
                                                "productor_razon_social" : request.form["productor_razon_social"], 
                                                "productor_zona" : request.form["productor_zona"], 
                                                "productor_tipo_cosecha" : request.form["productor_tipo_cosecha"], 
                                                "fletero_codigo" : request.form["fletero_codigo"], 
                                                "fletero_nombre" : request.form["fletero_nombre"], 
                                                "fletero_patente_camion" : request.form["fletero_patente_camion"], 
                                                "fletero_patente_acoplado" : request.form["fletero_patente_acoplado"], 
                                                "fletero_chofer" : request.form["fletero_chofer"], 
                                                "variedad_codigo" : request.form["variedad_codigo"], 
                                                "variedad_nombre" : request.form["variedad_nombre"], 
                                                "variedad_codigo_acoplado" : request.form["variedad_codigo_acoplado"], 
                                                "variedad_nombre_acoplado" : request.form["variedad_nombre_acoplado"], 
                                                "responsable" : session["id"], 
                                                "fecha" : request.form["fecha"], 
                                                "observacion" : request.form["observacion"]
                                            }).fetchone()
        db.db.session.commit()
        return result[0]
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()  # Obtiene la traza completa del error
        print(f"Error: {error_message}")  # Imprime toda la información
        return None
    
def get_materia(id):
    try:
        sql = text("""
                    SELECT m.*, u.nombre
                    FROM materia m
                    JOIN usuario u ON m.responsable = u.id
                    WHERE m.id = :id 
                """
                )
        
        materia = db.db.session.execute(sql,{"id": id})
        return materia.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_materia(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"m.productor_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.productor_razon_social::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.productor_zona::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.productor_tipo_cosecha::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fletero_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fletero_nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fletero_patente_camion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fletero_patente_acoplado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fletero_chofer::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.variedad_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.variedad_nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.variedad_codigo_acoplado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.variedad_nombre_acoplado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fecha::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.observacion::TEXT ILIKE '%{termino}%'")
            
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT m.*, u.nombre
            FROM materia m
            JOIN usuario u ON m.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY m.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT m.*, u.nombre
                                    FROM materia m
                                    JOIN usuario u ON m.responsable = u.id
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