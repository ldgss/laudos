from sqlalchemy.sql import text
from db import db
from flask import request
import pandas as pd
from io import BytesIO
    
def get_envasado():
    try:
        sql = text("""
                    SELECT 
                        m.producto, 
                        m.observacion, 
                        m.cantidad, 
                        m.lote, 
                        m.fecha_elaboracion, 
                        m.numero_unico, 
                        m.vto, 
                        m.fecha_registro, 
                        m.den,
                        u.nombre,
                        d.fecha_registro as fecha_despacho
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    LEFT JOIN despacho d ON m.numero_unico = d.mercaderia
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_elaboracion >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_elaboracion <= :fecha_final)
                        AND (m.fecha_etiquetado is null)
                        AND (m.fecha_encajonado is null)
                        AND (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%')
                        AND (:denominacion IS NULL OR m.den ILIKE '%' || :denominacion || '%')
                        AND (:lote_inicial IS NULL OR m.lote >= :lote_inicial)
                        AND (:lote_final IS NULL OR m.lote <= :lote_final)
                    ORDER BY m.fecha_registro DESC;
                    

                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
                                            "lote_inicial": request.form["lote_inicial"] if request.form["lote_inicial"].strip() else None,
                                            "lote_final": request.form["lote_final"] if request.form["lote_final"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)

        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_etiquetado():
    try:
        sql = text("""
                    SELECT 
                        m.producto, 
                        m.observacion, 
                        m.cantidad, 
                        m.lote, 
                        m.fecha_etiquetado, 
                        m.numero_unico, 
                        m.vto, 
                        m.fecha_registro, 
                        m.den,
                        u.nombre,
                        d.fecha_registro as fecha_despacho
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    LEFT JOIN despacho d ON m.numero_unico = d.mercaderia
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_etiquetado >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_etiquetado <= :fecha_final)
                        AND (m.fecha_elaboracion IS NULL)
                        AND (m.fecha_encajonado IS NULL)
                        AND (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%')
                        AND (:denominacion IS NULL OR m.den ILIKE '%' || :denominacion || '%')
                        AND (:lote_inicial IS NULL OR m.lote >= :lote_inicial)
                        AND (:lote_final IS NULL OR m.lote <= :lote_final)
                    ORDER BY m.fecha_registro DESC;
                    

                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
                                            "lote_inicial": request.form["lote_inicial"] if request.form["lote_inicial"].strip() else None,
                                            "lote_final": request.form["lote_final"] if request.form["lote_final"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_encajonado():
    try:
        sql = text("""
                    SELECT 
                        m.producto, 
                        m.observacion, 
                        m.cantidad, 
                        m.lote, 
                        m.fecha_encajonado, 
                        m.numero_unico, 
                        m.vto, 
                        m.fecha_registro, 
                        m.den,
                        u.nombre,
                        d.fecha_registro as fecha_despacho
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    LEFT JOIN despacho d ON m.numero_unico = d.mercaderia
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_encajonado >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_encajonado <= :fecha_final)
                        AND (m.fecha_elaboracion IS NULL)
                        AND (m.fecha_etiquetado IS NULL)
                        AND (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%')
                        AND (:denominacion IS NULL OR m.den ILIKE '%' || :denominacion || '%')
                        AND (:lote_inicial IS NULL OR m.lote >= :lote_inicial)
                        AND (:lote_final IS NULL OR m.lote <= :lote_final)
                    ORDER BY m.fecha_registro DESC;
                    

                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
                                            "lote_inicial": request.form["lote_inicial"] if request.form["lote_inicial"].strip() else None,
                                            "lote_final": request.form["lote_final"] if request.form["lote_final"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_reacondicionado():
    try:
        sql = text("""
                        SELECT 
                            r.numero_unico, 
                            r.nueva_den, 
                            r.observaciones, 
                            r.tipo_reacondicionado,
                            m.lote,
                            m.numero_unico,
                            rd.cantidad,
                            u.nombre as nombre_responsable, 
                            r.fecha_registro,
                            d.fecha_registro as fecha_despacho
                        FROM reacondicionado r
                        inner join usuario u on r.responsable = u.id	
                        inner join reacondicionado_detalle rd on r.id  = rd.reacondicionado
                        inner join mercaderia m on rd.mercaderia_original = m.id 
                        left join despacho d on d.reacondicionado = r.numero_unico 
                        where 
                        (:fecha_inicial IS NULL OR r.fecha_registro >= :fecha_inicial) and
                        (:fecha_final IS NULL OR r.fecha_registro <= :fecha_final) and
                        (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                        (:denominacion IS NULL OR r.nueva_den ILIKE '%' || :denominacion || '%') and
                        (:lote_inicial IS NULL OR m.lote >= :lote_inicial) and
                        (:lote_final IS NULL OR m.lote <= :lote_final)
                        order by r.fecha_registro DESC;
                    """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
                                            "lote_inicial": request.form["lote_inicial"] if request.form["lote_inicial"].strip() else None,
                                            "lote_final": request.form["lote_final"] if request.form["lote_final"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_extracto():
    try:
        sql = text("""
                        SELECT 
                            e.numero_unico, 
                            e.producto, 
                            e.fecha_elaboracion, 
                            e.lote, 
                            e.brix, 
                            e.numero_recipiente, 
                            e.observaciones, 
                            e.vto_meses, 
                            u.nombre,
                            e.fecha_registro, 
                            e.den,
                            d.fecha_registro as fecha_despacho
                        FROM extracto e
                        inner join usuario u on e.responsable = u.id
                        left join despacho d on d.extracto = e.numero_unico 
                        where 
                            (:fecha_inicial IS NULL OR e.fecha_registro >= :fecha_inicial) and
                            (:fecha_final IS NULL OR e.fecha_registro <= :fecha_final) and
                            (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                            (:denominacion IS NULL OR e.den ILIKE '%' || :denominacion || '%') and
                            (:brix_inicial IS NULL OR e.brix >= :brix_inicial) and
                            (:brix_final IS NULL OR e.brix <= :brix_final) and
                            (:lote_inicial IS NULL OR e.lote >= :lote_inicial) and
                            (:lote_final IS NULL OR e.lote <= :lote_final)
                        order by e.fecha_elaboracion DESC;
                    """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
                                            "brix_inicial": request.form["brix_inicial"] if request.form["brix_inicial"].strip() else None,
                                            "brix_final": request.form["brix_final"] if request.form["brix_final"].strip() else None,
                                            "lote_inicial": request.form["lote_inicial"] if request.form["lote_inicial"].strip() else None,
                                            "lote_final": request.form["lote_final"] if request.form["lote_final"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_insumo():
    try:
        sql = text("""
                    SELECT 
                        i.insumo, 
                        i.codigo_insumo, 
                        i.fecha_consumo, 
                        u.nombre, 
                        i.fecha_registro, 
                        i.lote_insumo, 
                        i.cantidad
                    FROM insumo_envase i
                    inner join usuario u on i.responsable = u.id
                        where 
                        (:fecha_inicial IS NULL OR i.fecha_registro >= :fecha_inicial) and
                        (:fecha_final IS NULL OR i.fecha_registro <= :fecha_final) and
                        (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                        (:insumo IS NULL OR i.insumo ILIKE '%' || :insumo || '%') and
                        (:codigo IS NULL OR i.codigo_insumo ilike '%' || :codigo || '%') and
                        (:lote is null or i.lote_insumo ilike '%' || :lote || '%')
                    order by i.fecha_registro DESC;
                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "insumo": request.form["insumo"] if request.form["insumo"].strip() else None,
                                            "codigo": request.form["codigo"] if request.form["codigo"].strip() else None,
                                            "lote": request.form["lote"] if request.form["lote"].strip() else None,
                                          }
                                         ).fetchall()
        # Crear un DataFrame a partir de envasado, las columnas se infieren automáticamente
        df = pd.DataFrame(envasado)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_ubicacion():
    
    try:
        sql = text("""
            SELECT 
                ub.mercaderia,
                m.den AS mercaderia_den,
                m.lote as mercaderia_lote,
                m.cantidad as mercaderia_cdad,
                m.fecha_elaboracion + INTERVAL '1 month' * v.meses AS env_vto,
                m.fecha_etiquetado + INTERVAL '1 month' * v.meses AS eti_vto,
                m.fecha_encajonado + INTERVAL '1 month' * v.meses AS encaj_vto,
                ub.hojalata,
                h.den AS hojalata_den,
                h.lote as hojalata_lote,
                h.cantidad as hojalata_cdad,
                h.fecha_elaboracion + INTERVAL '1 month' * v.meses AS hoj_vto,
                ub.extracto,
                e.den AS extracto_den,
                e.lote as extracto_lote,
                e.fecha_elaboracion + INTERVAL '1 month' * v.meses AS ext_vto,
                ub.reacondicionado,
                r.nueva_den AS reacondicionado_den,
                ra.cantidad AS reac_cantidad,
                mra.lote AS reac_lote,
                un.posicion,
                un.sector,
                ub.ubicacion_profundidad,
                ub.ubicacion_altura,
                ub.fecha_registro,
                us.nombre AS responsable,
                d.fecha_registro as fecha_despacho
            FROM ubicacion ub
            LEFT JOIN ubicacion_nombre un ON ub.ubicacion_fila = un.id
            LEFT JOIN usuario us ON ub.responsable = us.id
            LEFT JOIN mercaderia m ON ub.mercaderia = m.numero_unico
            LEFT JOIN hojalata h ON ub.hojalata = h.numero_unico
            LEFT JOIN extracto e ON ub.extracto = e.numero_unico
            LEFT JOIN reacondicionado r ON ub.reacondicionado = r.numero_unico
            LEFT JOIN reacondicionado_detalle ra ON r.id = ra.reacondicionado
            LEFT JOIN mercaderia mra ON mra.id = ra.mercaderia_original
            left join despacho d on 
            	(
            		(d.mercaderia = ub.mercaderia) or
            		(d.hojalata = ub.hojalata) or
            		(d.extracto = ub.extracto) or
            		(d.reacondicionado = ub.reacondicionado)
            	)
            left join vencimiento v on
                (
                   (m.vto = v.id) or
                   (h.vto_meses = v.id) or
                   (e.vto_meses = v.id)
                )
            WHERE 
               (:fecha_inicial IS NULL OR ub.fecha_registro >= :fecha_inicial) AND
			    (:fecha_final IS NULL OR ub.fecha_registro <= :fecha_final) AND
			    
			    (
			        (:lote_inicial IS NULL OR m.lote >= :lote_inicial) OR
			        (:lote_inicial IS NULL OR h.lote >= :lote_inicial) OR
			        (:lote_inicial IS NULL OR e.lote >= :lote_inicial)
			    ) AND
			    (
			        (:lote_final IS NULL OR m.lote <= :lote_final) OR
			        (:lote_final IS NULL OR h.lote <= :lote_final) OR
			        (:lote_final IS NULL OR e.lote <= :lote_final)
			    ) AND
                (:responsable IS NULL OR us.nombre ILIKE '%' || :responsable || '%') AND
                (:denominacion IS NULL OR 
                    m.den ILIKE '%' || :denominacion || '%' OR 
                    h.den ILIKE '%' || :denominacion || '%' OR 
                    e.den ILIKE '%' || :denominacion || '%' OR 
                    r.nueva_den ILIKE '%' || :denominacion || '%')
            ORDER BY ub.fecha_registro DESC;
        """)

        # Ejecutar la consulta
        sql_params = db.db.session.execute(
            sql,
            {
                "fecha_inicial": request.form.get("fecha_inicial") or None,
                "fecha_final": request.form.get("fecha_final") or None,
                "lote_inicial": request.form.get("lote_inicial") or None,
                "lote_final": request.form.get("lote_final") or None,
                "responsable": request.form.get("responsable") or None,
                "denominacion": request.form.get("denominacion") or None,
            }
        ).fetchall()

        # Crear un DataFrame a partir de sql_params, las columnas se infieren automáticamente
        df = pd.DataFrame(sql_params)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_despacho():
    
    try:
        sql = text("""
            SELECT 
                d.mercaderia,
                m.den as mercaderia_den,
                m.lote as mercaderia_lote,
                d.hojalata,
                h.den as hojalata_den,
                h.lote as hojalata_lote,
                d.extracto,
                e.den as extracto_den,
                e.lote as extracto_lote,
                d.reacondicionado,
                r.nueva_den as reacondicionado_den,
                d.fletero_codigo,
                d.fletero_nombre,
                d.observaciones,
                u.nombre,
                d.fecha_registro
            FROM despacho d
            LEFT JOIN usuario u ON d.responsable = u.id
            LEFT JOIN mercaderia m ON d.mercaderia = m.numero_unico
            LEFT JOIN hojalata h ON d.hojalata = h.numero_unico
            LEFT JOIN extracto e ON d.extracto = e.numero_unico
            LEFT JOIN reacondicionado r ON d.reacondicionado = r.numero_unico
            WHERE 
			    (:fecha_inicial IS NULL OR d.fecha_registro >= :fecha_inicial) AND
			    (:fecha_final IS NULL OR d.fecha_registro <= :fecha_final) AND
			    
			    (
			        (:lote_inicial IS NULL OR m.lote >= :lote_inicial) OR
			        (:lote_inicial IS NULL OR h.lote >= :lote_inicial) OR
			        (:lote_inicial IS NULL OR e.lote >= :lote_inicial)
			    ) AND
			    (
			        (:lote_final IS NULL OR m.lote <= :lote_final) OR
			        (:lote_final IS NULL OR h.lote <= :lote_final) OR
			        (:lote_final IS NULL OR e.lote <= :lote_final)
			    ) AND
			    
			    (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') AND
			    (:observaciones IS NULL OR d.observaciones ILIKE '%' || :observaciones || '%') AND
			    (:fletero_codigo IS NULL OR d.fletero_codigo ILIKE '%' || :fletero_codigo || '%') AND
			    (:fletero_nombre IS NULL OR d.fletero_nombre ILIKE '%' || :fletero_nombre || '%') AND
			    (:denominacion IS NULL OR 
			        m.den ILIKE '%' || :denominacion || '%' OR 
			        h.den ILIKE '%' || :denominacion || '%' OR 
			        e.den ILIKE '%' || :denominacion || '%' OR 
			        r.nueva_den ILIKE '%' || :denominacion || '%')
			ORDER BY d.fecha_registro DESC;
                    """)

        # Ejecutar la consulta
        sql_params = db.db.session.execute(
            sql,
            {
                "fecha_inicial": request.form.get("fecha_inicial") or None,
                "fecha_final": request.form.get("fecha_final") or None,
                "responsable": request.form.get("responsable") or None,
                "observaciones": request.form.get("observaciones") or None,
                "fletero_codigo": request.form.get("fletero_codigo") or None,
                "fletero_nombre": request.form.get("fletero_nombre") or None,
                "lote_inicial": request.form.get("lote_inicial") or None,
                "lote_final": request.form.get("lote_final") or None,
                "denominacion": request.form.get("denominacion") or None,
            }
        ).fetchall()

        # Crear un DataFrame a partir de sql_params, las columnas se infieren automáticamente
        df = pd.DataFrame(sql_params)
        # Crear un archivo CSV en memoria
        output = BytesIO()
        df.to_csv(output, index=False)

        output.seek(0)  # Mover el puntero al inicio del archivo

        return output
    except Exception as e:
        print(f"Error: {e}")
        return None