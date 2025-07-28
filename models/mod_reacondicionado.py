from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
import shlex

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
            prefijo = str(datetime.now().year)
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = f"{prefijo}-T2-{nuevo_numero_str}"

            return nuevo_codigo
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
    
def guardar_reacondicionado():
    try:
        # insert 1 vars
        responsable = request.form["user_id"]
        denominacion = request.form["denominacion"]
        numero_unico = request.form["numero_unico"]
        tipo_reacondicionado = request.form["tipo_reacondicionado"]
        observaciones = request.form["observaciones"]
        # insert 2 vars T1|T2
        ids_a_tomar = request.form.getlist('id_a_tomar')
        numeros_unicos = request.form.getlist('numeros_unicos')
        mercaderias_originales = request.form.getlist('mercaderia_original')
        cantidades_disponibles = request.form.getlist('cantidad_disponible')
        cantidades_tomar = request.form.getlist('cantidad_tomar')
        reacondicionado_detalle = []

        # extendemos numeros_unicos ya que es un array mas corto, sino no coinciden el numero para zip
        numeros_unicos_exp = [next(cycle(numeros_unicos)) for _ in range(len(ids_a_tomar))]

        # agrupar los detalles
        for id_a_tomar, numero, mercaderia_original, disponible, tomar in zip(ids_a_tomar, numeros_unicos_exp, mercaderias_originales,cantidades_disponibles, cantidades_tomar):
            print(f"appending: {id_a_tomar}, {numero}, {disponible}, {tomar}, {mercaderia_original}")
            reacondicionado_detalle.append({"id_a_tomar":id_a_tomar,"numero": numero, "mercaderia_original": mercaderia_original, "disponible": disponible, "tomar": tomar})

        print(f"reacondicionado detalle: {reacondicionado_detalle}")

        # insert 1
        reacondicionado = text("""
                    INSERT INTO
                    reacondicionado
                    (numero_unico, responsable, fecha_registro, nueva_den, observaciones, tipo_reacondicionado)
                    VALUES
                    (:numero_unico, :responsable, CURRENT_TIMESTAMP, :nueva_den, :observaciones, :tipo_reacondicionado)
                    RETURNING id;
                """
                )
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "numero_unico": numero_unico,
                                                "responsable": responsable,
                                                "nueva_den": denominacion,
                                                "observaciones": observaciones,
                                                "tipo_reacondicionado": tipo_reacondicionado
                                            })
        db.db.session.commit()
        reacondicionado = reacondicionado.scalar() # obtengo el id insertado
        
        # insert 2
        for rd in reacondicionado_detalle:
            reacondicionado_detalle_sql = text("""
                        INSERT INTO
                        reacondicionado_detalle
                        (reacondicionado, mercaderia, cantidad, 
                        reacondicionado_detalle, fecha_registro, mercaderia_original,
                        extracto, extracto_original)
                        VALUES
                        (:reacondicionado, :mercaderia, :cantidad, 
                        :reacondicionado_detalle, CURRENT_TIMESTAMP, :mercaderia_original,
                        :extracto, :extracto_original)
                    """
                    )
            db.db.session.execute(reacondicionado_detalle_sql,
                                                {
                                                    "reacondicionado": reacondicionado,
                                                    "mercaderia": rd["id_a_tomar"] if "T1" in rd["numero"] else None,
                                                    "cantidad": rd["tomar"],
                                                    "reacondicionado_detalle":rd["id_a_tomar"] if "T2" in rd["numero"] else None,
                                                    "mercaderia_original": rd["mercaderia_original"] if "T1" in rd["numero"] else None,
                                                    "extracto": rd["id_a_tomar"] if "E1" in rd["numero"] else None,
                                                    "extracto_original": rd["mercaderia_original"] if "E1" in rd["numero"] else None,
                                                })
        db.db.session.commit()

        # actualizar las cantidades, tanto si es mercaderia T1 como reacondicionados T2
        
        for rd in reacondicionado_detalle:
            nueva_cantidad = int(rd["disponible"]) - int(rd["tomar"])
            if "T1" in rd["numero"]:
                update_mercaderia = text("""
                    UPDATE mercaderia
                    SET cantidad = :nueva_cantidad
                    WHERE id = :id;
                """)
                db.db.session.execute(
                    update_mercaderia,
                    {
                        "nueva_cantidad": nueva_cantidad,  
                        "id": rd["id_a_tomar"]         
                    }
                )
            elif "E1" in rd["numero"]:
                update_mercaderia = text("""
                    UPDATE extracto
                    SET cantidad = :nueva_cantidad
                    WHERE id = :id;
                """)
                db.db.session.execute(
                    update_mercaderia,
                    {
                        "nueva_cantidad": nueva_cantidad,  
                        "id": rd["id_a_tomar"]         
                    }
                )
            else:
                update_reacondicionado_detalle = text("""
                    UPDATE reacondicionado_detalle
                    SET cantidad = :nueva_cantidad
                    WHERE id = :id
                """)
                db.db.session.execute(
                    update_reacondicionado_detalle, 
                    {
                        "nueva_cantidad": nueva_cantidad,
                        "id": rd["id_a_tomar"]
                    }
                )

        # Hacemos un solo commit al final
        db.db.session.commit()

        
        return numero_unico
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_reacondicionado(numero_unico):
    try:
        sql = text("""
                    SELECT *
                    FROM mercaderia
                    WHERE numero_unico = :numero_unico 
                """
                )
        
        t1 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        t1 = t1.mappings().first() or {}
        
        sql = text("""
                    SELECT *
                    FROM extracto
                    WHERE numero_unico = :numero_unico 
                """
                )
        
        e1 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        e1 = e1.mappings().first() or {}
    
        g1 = t1 or e1

        sql = text(""" 
            SELECT m.*, e.*, r.*, rd.*, 
                   m.den as mden,
                   m.lote as mlote,
                   e.den as eden,
                   e.lote as elote, 
                   v.meses, u.nombre, m.numero_unico AS numero_unico_original,
                   e.numero_unico AS numero_unico_original_extracto,
                   e.fecha_elaboracion AS extracto_fecha_elaboracion,
                   ve.meses AS extracto_vto
            FROM reacondicionado r
            RIGHT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
            LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
            LEFT JOIN extracto e ON e.id = rd.extracto_original
            LEFT JOIN vencimiento v ON v.id = m.vto
            LEFT JOIN vencimiento ve ON ve.id = e.vto_meses
            LEFT JOIN usuario u ON r.responsable = u.id
            WHERE r.numero_unico = :numero_unico
         """)
        
        t2 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        t2 = [dict(row) for row in t2.mappings().all() or {}]
        return {**g1, "reacondicionado": t2}
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def imprimir(numero_unico):
    try:
        sql = text("""
                    SELECT *
                    FROM mercaderia
                    WHERE numero_unico = :numero_unico 
                """
                )
        
        t1 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        t1 = t1.mappings().first() or {}
        
        sql = text("""
                    SELECT *
                    FROM extracto
                    WHERE numero_unico = :numero_unico 
                """
                )
        
        e1 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        e1 = e1.mappings().first() or {}
    
        g1 = t1 or e1

        sql = text(""" 
            SELECT 
                /* reacondicionado */
                r.numero_unico,
                r.nueva_den,
                r.tipo_reacondicionado,
                rd.cantidad,
                r.observaciones,
                u_r.nombre,
                to_char(r.fecha_registro, 'YYYY-MM-DD HH24:MI') as fecha_registro,
                /* mercaderia a un paso */
                m.den as m_den,
                m.numero_unico as m_numero_unico,
                to_char(m.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as m_fecha_elaboracion,
                to_char(m.fecha_etiquetado, 'YYYY-MM-DD HH24:MI') as m_fecha_etiquetado,
                vm.meses as m_vto,
                m.lote as m_lote,
                m.observacion as m_observacion,
                u_m.nombre as m_responsable,
                /* extracto a un paso */
                e.den as e_den,
                e.numero_unico as e_numero_unico,
                to_char(e.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as e_fecha_elaboracion,
                ve.meses as e_vto,
                e.lote as e_lote,
                e.observaciones as e_observaciones,
                u_e.nombre as e_responsable,
                /* mercaderia a dos pasos */
                m2.den as m2_den,
                m2.numero_unico as m2_numero_unico,
                to_char(m2.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as m2_fecha_elaboracion,
                to_char(m2.fecha_etiquetado, 'YYYY-MM-DD HH24:MI') as m2_fecha_etiquetado,
                vm2.meses as m2_vto,
                m2.lote as m2_lote,
                m2.observacion as m2_observacion,
                u_m2.nombre as m2_responsable,
                /* extracto a dos pasos */
                e2.den as e2_den,
                e2.numero_unico as e2_numero_unico,
                to_char(e2.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as e2_fecha_elaboracion,
                ve2.meses as e2_vto,
                e2.lote as e2_lote,
                e2.observaciones as e2_observaciones,
                u_e2.nombre as e2_responsable
            FROM reacondicionado r
            left JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
            LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
            LEFT JOIN extracto e ON e.id = rd.extracto_original
            left join reacondicionado_detalle rd2 on rd2.id = rd.reacondicionado_detalle
            left join mercaderia m2 on m2.id = rd2.mercaderia_original 
            left join extracto e2 on e2.id = rd2.extracto_original 
            left join usuario u_r on u_r.id = r.responsable 
            left join usuario u_m on u_m.id = m.responsable
            left join usuario u_m2 on u_m2.id = m2.responsable
            left join usuario u_e on u_e.id = e.responsable
            left join usuario u_e2 on u_e2.id = e2.responsable
            left join vencimiento vm on vm.id = m.id
            left join vencimiento vm2 on vm2.id = m2.id
            left join vencimiento ve on ve.id = e.id
            left join vencimiento ve2 on ve2.id = e2.id
            WHERE r.numero_unico = :numero_unico
         """)
        
        t2 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        t2 = [dict(row) for row in t2.mappings().all() or {}]
        return {**g1, "reacondicionado": t2}
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_listado_reacondicionado(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            # chequear cada termino en mercaderia
            subcondicion.append(f"m.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en extracto
            subcondicion.append(f"e.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.brix::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_recipiente::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.cantidad::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en reacondicionado
            subcondicion.append(f"r.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.nueva_den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"r.tipo_reacondicionado::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en reacondicionado_detalle
            subcondicion.append(f"rd.fecha_registro::TEXT ILIKE '%{termino}%'")

            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        # query_sql = f"""
        #     SELECT m.*, r.*, rd.*, v.producto, v.meses, u.nombre, m.numero_unico AS numero_unico_original
        #     FROM reacondicionado r
        #     RIGHT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
        #     LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
        #     LEFT JOIN vencimiento v ON v.id = m.vto
        #     LEFT JOIN usuario u ON r.responsable = u.id
        #     WHERE {condicion_final_ilike}
        #     LIMIT :limit OFFSET :offset;
        # """
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
            LEFT JOIN extracto e ON e.id = rd.extracto_original
            LEFT JOIN vencimiento v ON v.id = m.vto
            WHERE {condicion_final_ilike}
            GROUP BY r.id, u.nombre
            ORDER BY r.fecha_registro DESC
            LIMIT :limit OFFSET :offset;

        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
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
                                    LEFT JOIN extracto e ON e.id = rd.extracto_original
                                    LEFT JOIN vencimiento v ON v.id = m.vto
                                    WHERE {condicion_final_ilike}
                                    GROUP BY r.id, u.nombre
                                    ORDER BY r.fecha_registro DESC
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