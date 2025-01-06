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
            prefijo = ultimo_id[:-6]
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = prefijo + nuevo_numero_str
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
                        (reacondicionado, mercaderia, cantidad, reacondicionado_detalle, fecha_registro, mercaderia_original)
                        VALUES
                        (:reacondicionado, :mercaderia, :cantidad, :reacondicionado_detalle, CURRENT_TIMESTAMP, :mercaderia_original)
                    """
                    )
            db.db.session.execute(reacondicionado_detalle_sql,
                                                {
                                                    "reacondicionado": reacondicionado,
                                                    "mercaderia": rd["id_a_tomar"] if "T1" in rd["numero"] else None,
                                                    "cantidad": rd["tomar"],
                                                    "reacondicionado_detalle":rd["id_a_tomar"] if "T2" in rd["numero"] else None,
                                                    "mercaderia_original": rd["mercaderia_original"]
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
            SELECT m.*, r.*, rd.*, v.meses, u.nombre, m.numero_unico AS numero_unico_original
            FROM reacondicionado r
            RIGHT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
            LEFT JOIN mercaderia m ON m.id = rd.mercaderia_original
            LEFT JOIN vencimiento v ON v.id = m.vto
            LEFT JOIN usuario u ON r.responsable = u.id
            WHERE r.numero_unico = :numero_unico
         """)
        
        t2 = db.db.session.execute(sql,{"numero_unico": numero_unico})
        t2 = [dict(row) for row in t2.mappings().all() or {}]
        return {**t1, "reacondicionado": t2}
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