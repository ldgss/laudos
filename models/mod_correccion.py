from sqlalchemy.sql import text
from db import db
from flask import request
from flask import session
import shlex
import traceback
    
def guardar_correccion():
    # T1
    numero_unico_modal1 = request.form.get("numero_unico_modal1")
    # H1
    numero_unico_modal2 = request.form.get("numero_unico_modal2")
    # E1
    numero_unico_modal3 = request.form.get("numero_unico_modal3")
    # T2
    numero_unico_modal4 = request.form.get("numero_unico_modal4")

    # antes de corregir chequear que el T1, E1, H1, no sean parte de un T2
    # si es asi, cancelar, y el usuario debe borrar primero el T2

    try:
        sql_check = text("""
            SELECT 1
            FROM reacondicionado_detalle rd
            LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
            LEFT JOIN extracto e  ON e.id = rd.extracto_original
            WHERE
                (:t1 IS NOT NULL AND m.numero_unico = :t1)
            OR (:e1 IS NOT NULL AND e.numero_unico = :e1)
            LIMIT 1
        """)

        result = db.db.session.execute(
            sql_check,
            {
                "t1": numero_unico_modal1,
                "h1": numero_unico_modal2,
                "e1": numero_unico_modal3
            }
        ).fetchone()

        if result:
            raise ValueError("El T1 es parte de un T2")
            

    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return None

    try:
        if numero_unico_modal1 and 'T1' in numero_unico_modal1:
            sql = text(""" 
                        UPDATE mercaderia
                        SET 
                            producto=:producto, 
                            observacion=:observacion, 
                            cantidad=:cantidad, 
                            lote=:lote, 
                            fecha_elaboracion=:fecha_elaboracion, 
                            fecha_etiquetado=:fecha_etiquetado,  
                            fecha_encajonado=:fecha_encajonado, 
                            den=:den,
                            llenadora_botella=:llenadora_botella,
                            vto = (SELECT id FROM vencimiento WHERE producto = :cod_cls)
                        WHERE 
                            numero_unico=:numero_unico; 
                       """)
        
            result = db.db.session.execute(sql,
                                            {
                                                "producto":request.form["cod_mae_modal1"],
                                                "observacion":request.form["observaciones_modal1"],
                                                "cantidad":request.form["cantidad_modal1"],
                                                "lote": f"{request.form["lote_a_modal1"]}-{request.form["lote_b_modal1"]}-{request.form["lote_c_modal1"]}",
                                                "fecha_elaboracion": f"{request.form["fecha_modal1"]} {request.form["hora_modal1"]}" if 'tipo_fecha_elaboracion' in request.form["tipo_fecha_modal1"] else None,
                                                "fecha_etiquetado":f"{request.form["fecha_modal1"]} {request.form["hora_modal1"]}" if 'tipo_fecha_etiquetado' in request.form["tipo_fecha_modal1"] else None,
                                                "fecha_encajonado":f"{request.form["fecha_modal1"]} {request.form["hora_modal1"]}" if 'tipo_fecha_encajonado' in request.form["tipo_fecha_modal1"] else None,
                                                "den":request.form["denominacion_modal1"],
                                                "numero_unico":request.form["numero_unico_modal1"],
                                                "llenadora_botella":request.form.get("llenadora_botella") or None,
                                                "cod_cls":request.form["cod_cls_modal1"]
                                            })
        elif numero_unico_modal2 and 'H1' in numero_unico_modal2:
            sql = text(""" 
                        UPDATE hojalata
                        SET 
                            producto=:producto, 
                            observacion=:observacion, 
                            cantidad=:cantidad, 
                            lote=:lote, 
                            lote_cuerpo=:lote_cuerpo, 
                            lote_tapa=:lote_tapa, 
                            fecha_elaboracion=:fecha_elaboracion, 
                            den=:den,
                            vto_meses = (SELECT id FROM vencimiento WHERE producto = :cod_cls)
                        WHERE 
                            numero_unico=:numero_unico; 
                       """)
        
            result = db.db.session.execute(sql,
                                            {
                                                "producto":request.form["cod_mae_modal2"],
                                                "observacion":request.form["observaciones_modal2"],
                                                "cantidad":request.form["cantidad_modal2"],
                                                "lote": request.form["lote_modal2"],
                                                "lote_cuerpo": None,
                                                "lote_tapa": None,
                                                "fecha_elaboracion": f"{request.form["fecha_modal2"]} {request.form["hora_modal2"]}",
                                                "den":request.form["denominacion_modal2"],
                                                "numero_unico":request.form["numero_unico_modal2"],
                                                "cod_cls":request.form["cod_cls_modal2"]
                                            })
        elif numero_unico_modal3 and 'E1' in numero_unico_modal3:
            sql = text(""" 
                        UPDATE extracto
                        SET 
                            producto=:producto, 
                            observaciones=:observacion, 
                            fecha_elaboracion=:fecha_elaboracion, 
                            lote=:lote, 
                            brix=:brix,
                            numero_recipiente=:numero_recipiente, 
                            den=:den,
                            vto_meses = (SELECT id FROM vencimiento WHERE producto = :cod_cls)
                        WHERE 
                            numero_unico=:numero_unico; 
                    """)
        
            result = db.db.session.execute(sql,
                                            {
                                                "producto":request.form["cod_mae_modal3"],
                                                "observacion":request.form["observaciones_modal3"],
                                                "fecha_elaboracion": f"{request.form["fecha_modal3"]} {request.form["hora_modal3"]}",
                                                "lote": f"{request.form["lote_a_modal3"]}-{request.form["lote_b_modal3"]}-{request.form["lote_c_modal3"]}",
                                                "brix": request.form["brix_modal3"] or None,
                                                "numero_recipiente": request.form["numero_recipiente_modal3"],
                                                "den":request.form["denominacion_modal3"],
                                                "numero_unico":request.form["numero_unico_modal3"],
                                                "cod_cls":request.form["cod_cls_modal3"]
                                            })
        elif numero_unico_modal4 and 'T2' in numero_unico_modal4:
            sql = text(""" 
                        UPDATE reacondicionado
                        SET 
                            nueva_den=:nueva_den, 
                            observaciones=:observaciones, 
                            tipo_reacondicionado=:tipo_reacondicionado 
                        WHERE 
                            numero_unico=:numero_unico; 
                    """)
        
            result = db.db.session.execute(sql,
                                            {
                                                "nueva_den":request.form["denominacion_modal4"],
                                                "observaciones":request.form["observaciones_modal4"],
                                                "tipo_reacondicionado":request.form["tipo_reacondicionado_modal4"],
                                                "numero_unico":request.form["numero_unico_modal4"]
                                            })
        
        if(result):
            sql = text(
                """
                INSERT INTO correccion
                (numero_unico, observaciones, responsable, fecha_registro)
                VALUES(:numero_unico, :observaciones, :responsable, CURRENT_TIMESTAMP);
                """
            )

            numero_unico = request.form.get("numero_unico_modal1") or request.form.get("numero_unico_modal2") or request.form.get("numero_unico_modal3") or request.form.get("numero_unico_modal4")
            observaciones = request.form.get("observaciones_modal1") or request.form.get("observaciones_modal2") or request.form.get("observaciones_modal3") or request.form.get("observaciones_modal4")
            result = db.db.session.execute(sql, 
                                                {
                                                    "numero_unico": numero_unico,
                                                    "observaciones": observaciones,
                                                    "responsable": session["id"]
                                                })
            db.db.session.commit()
            return True
    except Exception as e:
        db.db.session.rollback()
        error_message = traceback.format_exc()  # Obtiene la traza completa del error
        print(f"Error: {error_message}")  # Imprime toda la información
        return None
    
def get_para_corregir(numero_unico):
    try:
        sql = ""
        if 'T1' in numero_unico:
            sql = text(""" SELECT * FROM mercaderia WHERE numero_unico = :numero_unico """)
        elif 'H1' in numero_unico:
            sql = text(""" SELECT * FROM hojalata WHERE numero_unico = :numero_unico """)
        elif 'E1' in numero_unico:
            sql = text(""" SELECT * FROM extracto WHERE numero_unico = :numero_unico """)
        elif 'T2' in numero_unico:
            sql = text(""" SELECT * FROM reacondicionado WHERE numero_unico = :numero_unico """)

        
        result = db.db.session.execute(sql,
                                            {
                                                "numero_unico": numero_unico,
                                            })
        return result.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_listado_correccion(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"c.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"c.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"c.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
            c.numero_unico,
            c.observaciones,
            c.responsable,
            c.fecha_registro,
            u.nombre
            FROM correccion c
            JOIN usuario u ON c.responsable = u.id
            WHERE 
                {condicion_final_ilike}
            ORDER BY c.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                    c.numero_unico,
                                    c.observaciones,
                                    c.responsable,
                                    c.fecha_registro,
                                    u.nombre
                                    FROM correccion c
                                    JOIN usuario u ON c.responsable = u.id
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