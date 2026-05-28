from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from flask import session
import shlex
import traceback


def get_clientes_proveedores():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                select 
                    cc.denominacion as den,
                    cc.numero_documento as cuit
                from cog_cliente cc 
                where denominacion != '~VARIOS~'
                union
                select
                    cp.denominacion as den,
                    cp.numero_documento as cuit
                from cog_proveedor cp 
                where denominacion != '~VARIOS~'
            """))
            return result.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return None

def guardar_retiro():
    try:
        sql = text("""
                    INSERT INTO public.retiro
                        (transporte, cuit, fecha, 
                        chofer, cuil_chofer, celular, 
                        cliente, patente_tractor, marca_tractor, 
                        patente_semi, observaciones, responsable, 
                        fecha_registro)
                    VALUES
                        (:transporte, :cuit, :fecha, 
                        :chofer, :cuil_chofer, :celular, 
                        :cliente, :patente_tractor, :marca_tractor, 
                        :patente_semi, :observaciones, :responsable, 
                        CURRENT_TIMESTAMP)
                    RETURNING id
                """
                )
        
        result = db.db.session.execute(sql,
                                            {
                                                "transporte": request.form["transporte"],
                                                "cuit": request.form["cuit"],
                                                "fecha": request.form["fecha"],
                                                "chofer": request.form["chofer"],
                                                "cuil_chofer": request.form["cuil_chofer"],
                                                "celular": request.form["celular"],
                                                "cliente": request.form["cliente"],
                                                "patente_tractor": request.form["patente_tractor"],
                                                "marca_tractor": request.form["marca_tractor"],
                                                "patente_semi": request.form["patente_semi"],
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
    
def get_retiro(id):
    try:
        sql = text("""
                    SELECT r.*, u.nombre as responsable
                    FROM public.retiro r
                    join usuario u ON r.responsable = u.id
                    where r.id = :id;
                """
                )
        
        materia = db.db.session.execute(sql,{"id": id})
        return materia.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_retiro(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"r.transporte::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.cuit::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.fecha::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.chofer::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.cuil_chofer::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.celular::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.cliente::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.patente_tractor::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.marca_tractor::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.patente_semi::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.fecha_registro::TEXT ILIKE '%{termino}%'")
            
            
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT r.*, u.nombre as responsable
            FROM retiro r
            JOIN usuario u ON r.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY r.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT r.*, u.nombre as responsable
                                    FROM retiro r
                                    JOIN usuario u ON r.responsable = u.id
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