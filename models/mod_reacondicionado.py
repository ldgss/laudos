from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
import shlex
from collections import defaultdict
from utils import helpers

def get_ultimo_id():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM reacondicionado
                    ORDER BY numero_unico DESC
                    LIMIT 1
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        ultimo_id = result.scalar()
        year = datetime.now().year

        return helpers.next_id(ultimo_id, "T2", year)
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
        responsable = request.form["user_id"]
        denominacion = request.form["denominacion"]
        numero_unico = request.form["numero_unico"]
        tipo_reacondicionado = request.form["tipo_reacondicionado"]
        observaciones = request.form["observaciones"]

        print(f"form: {request.form}")
        detalle = build_detalle(request.form)
        print(f"detalle: {detalle}")

        # UNA SOLA TRANSACCIÓN
        with db.db.session.begin():
            # insert maestro
            rec_id = db.db.session.execute(
                text("""
                    INSERT INTO reacondicionado
                        (numero_unico, responsable, fecha_registro, nueva_den,
                         observaciones, tipo_reacondicionado)
                    VALUES
                        (:numero_unico, :responsable, CURRENT_TIMESTAMP,
                         :nueva_den, :observaciones, :tipo_reacondicionado)
                    RETURNING id
                """),
                {
                    "numero_unico": numero_unico,
                    "responsable": responsable,
                    "nueva_den": denominacion,
                    "observaciones": observaciones,
                    "tipo_reacondicionado": tipo_reacondicionado,
                },
            ).scalar()

            # insert detalle
            for rd in detalle:
                db.db.session.execute(
                    text("""
                        INSERT INTO reacondicionado_detalle
                            (reacondicionado, mercaderia, cantidad,
                             reacondicionado_detalle, fecha_registro,
                             mercaderia_original, extracto, extracto_original)
                        VALUES
                            (:reacondicionado, :mercaderia, :cantidad,
                             :reacondicionado_detalle, CURRENT_TIMESTAMP,
                             :mercaderia_original, :extracto, :extracto_original)
                    """),
                    {
                        "reacondicionado": rec_id,
                        "mercaderia": rd["id_a_tomar"] if "T1" in rd["numero"] else None,
                        "cantidad": rd["tomar"],
                        "reacondicionado_detalle": rd["id_a_tomar"] if "T2" in rd["numero"] else None,
                        "mercaderia_original": rd["mercaderia_original"] or None,
                        "extracto": rd["id_a_tomar"] if "E1" in rd["numero"] else None,
                        "extracto_original": rd["extracto_original"] or None,
                    },
                )

            # updates de cantidad
            for rd in detalle:
                nueva_cantidad = int(rd["disponible"]) - int(rd["tomar"])
                if "T1" in rd["numero"]:
                    db.db.session.execute(
                        text("UPDATE mercaderia SET cantidad = :nueva WHERE id = :id"),
                        {"nueva": nueva_cantidad, "id": rd["id_a_tomar"]},
                    )
                elif "E1" in rd["numero"]:
                    db.db.session.execute(
                        text("UPDATE extracto SET cantidad = :nueva WHERE id = :id"),
                        {"nueva": nueva_cantidad, "id": rd["id_a_tomar"]},
                    )
                else:
                    db.db.session.execute(
                        text("UPDATE reacondicionado_detalle SET cantidad = :nueva WHERE id = :id"),
                        {"nueva": nueva_cantidad, "id": rd["id_a_tomar"]},
                    )

        # si llegó hasta acá, se hace commit automático
        return numero_unico

    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None

def build_detalle(form):
    # 1) Agrupar por numero_unico
    grupos = defaultdict(lambda: defaultdict(list))

    for key, value in form.items(multi=True):
        # solo claves con el patrón <numero_unico>_<campo>
        if "_" in key:
            numero, campo = key.split("_", 1)
            grupos[numero][campo].append(value)

    # 2) Convertir a la estructura detalle
    detalle = []
    for numero, campos in grupos.items():
        # Aseguramos que todas las listas tengan la misma longitud
        filas = len(campos["id_a_tomar"])
        for i in range(filas):
            detalle.append({
                "id_a_tomar":       campos["id_a_tomar"][i],
                "numero":           numero,
                "mercaderia_original": campos["mercaderia_original"][i],
                "extracto_original":   campos["extracto_original"][i],
                "disponible":       campos["cantidad_disponible"][i],
                "tomar":            campos["cantidad_tomar"][i],
            })
    return detalle

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
                (m.fecha_elaboracion + INTERVAL '1 month' * vm.meses)::date AS m_vto_elaboracion,
                (m.fecha_etiquetado + INTERVAL '1 month' * vm.meses)::date AS m_vto_etiquetado,
                m.lote as m_lote,
                m.observacion as m_observacion,
                u_m.nombre as m_responsable,
                /* extracto a un paso */
                e.den as e_den,
                e.numero_unico as e_numero_unico,
                to_char(e.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as e_fecha_elaboracion,
                (e.fecha_elaboracion + INTERVAL '1 month' * ve.meses)::date AS e_vto,
                e.lote as e_lote,
                e.observaciones as e_observaciones,
                u_e.nombre as e_responsable,
                /* mercaderia a dos pasos */
                m2.den as m2_den,
                m2.numero_unico as m2_numero_unico,
                to_char(m2.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as m2_fecha_elaboracion,
                to_char(m2.fecha_etiquetado, 'YYYY-MM-DD HH24:MI') as m2_fecha_etiquetado,
                (m2.fecha_elaboracion + INTERVAL '1 month' * vm2.meses)::date AS m2_vto_elaboracion,
                (m2.fecha_etiquetado + INTERVAL '1 month' * vm2.meses)::date AS m2_vto_etiquetado,
                m2.lote as m2_lote,
                m2.observacion as m2_observacion,
                u_m2.nombre as m2_responsable,
                /* extracto a dos pasos */
                e2.den as e2_den,
                e2.numero_unico as e2_numero_unico,
                to_char(e2.fecha_elaboracion, 'YYYY-MM-DD HH24:MI') as e2_fecha_elaboracion,
                (e2.fecha_elaboracion + INTERVAL '1 month' * ve2.meses)::date AS e2_vto,
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
            left join vencimiento vm on vm.id = m.vto
            left join vencimiento vm2 on vm2.id = m2.vto
            left join vencimiento ve on ve.id = e.vto_meses
            left join vencimiento ve2 on ve2.id = e2.vto_meses
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