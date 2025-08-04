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
                        m.fecha_elaboracion + INTERVAL '1 month' * v.meses AS vto,
                        m.fecha_registro, 
                        m.den,
                        m.llenadora_botella,
                        u.nombre,
                        d.fecha_registro as fecha_despacho
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    LEFT JOIN despacho d ON m.numero_unico = d.mercaderia
                    LEFT JOIN vencimiento v ON v.id  = m.vto
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
                        m.fecha_etiquetado + INTERVAL '1 month' * v.meses AS vto, 
                        m.fecha_registro, 
                        m.den,
                        m.llenadora_botella,
                        u.nombre,
                        d.fecha_registro as fecha_despacho
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    LEFT JOIN despacho d ON m.numero_unico = d.mercaderia
                    LEFT JOIN vencimiento v ON v.id = m.vto
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
                            e.fecha_elaboracion + INTERVAL '1 month' * v.meses AS vto, 
                            u.nombre,
                            e.fecha_registro, 
                            e.den,
                            d.fecha_registro as fecha_despacho
                        FROM extracto e
                        inner join usuario u on e.responsable = u.id
                        left join despacho d on d.extracto = e.numero_unico 
                        left join vencimiento v on v.id = e.vto_meses
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
    
def get_hojalata():
    try:
        sql = text("""
                    SELECT 
                        h.den as denominacion,
                        h.numero_unico,
                        h.numero_pallet_interno,
                        h.cantidad,
                        h.lote as lote,
                        h.fecha_elaboracion as elaboracion,
                        h.fecha_elaboracion + INTERVAL '1 month' * v.meses AS vencimiento,
                        h.observacion
                    FROM hojalata h
                    inner join usuario u on h.responsable = u.id
                    left join vencimiento v on v.id = h.vto_meses
                        where 
                        (:fecha_inicial IS NULL OR h.fecha_registro >= :fecha_inicial) and
                        (:fecha_final IS NULL OR h.fecha_registro <= :fecha_final) and
                        (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                        (:denominacion IS NULL OR h.den ILIKE '%' || :denominacion || '%') and
                        (:lote_inicial IS NULL OR h.lote >= :lote_inicial) and
                        (:lote_final IS NULL OR h.lote >= :lote_final) and
                        (:numero_pallet_interno_inicial IS NULL OR h.numero_pallet_interno >= :numero_pallet_interno_inicial) and
                        (:numero_pallet_interno_final IS NULL OR h.numero_pallet_interno >= :numero_pallet_interno_final)
                    order by h.fecha_registro DESC;
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
                                            "numero_pallet_interno_inicial": request.form["numero_pallet_interno_inicial"] if request.form["numero_pallet_interno_inicial"].strip() else None,
                                            "numero_pallet_interno_final": request.form["numero_pallet_interno_final"] if request.form["numero_pallet_interno_final"].strip() else None,
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
    
def get_bloqueo():
    try:
        sql = text("""
                    SELECT 
                        b.mercaderia, 
                        m.den as m_den,
                        m.lote as m_lote,
                        b.hojalata, 
                        h.den as h_den,
                        h.lote as h_lote,
                        b.extracto, 
                        e.den as e_den,
                        e.lote as e_lote,
                        b.estado, 
                        b.numero_planilla, 
                        mb.motivo, 
                        b.observaciones, 
                        u.nombre, 
                        b.fecha_registro, 
                        b.fecha_cambio
                    FROM bloqueado b
                    inner join usuario u on b.responsable = u.id 
                    inner join motivo_bloqueo mb on b.motivo = mb.id
                    left join mercaderia m on b.mercaderia = m.numero_unico 
                    left join hojalata h on b.hojalata = h.numero_unico 
                    left join extracto e on b.extracto = e.numero_unico 
                    where 
                        (:fecha_inicial IS NULL OR b.fecha_registro >= :fecha_inicial) and
                        (:fecha_final IS NULL OR b.fecha_registro <= :fecha_final) and
                        (:estado IS NULL OR b.estado ILIKE '%' || :estado || '%') and
                        (:numero_planilla IS NULL OR b.numero_planilla ILIKE '%' || :numero_planilla || '%') and
                        (:motivo IS NULL OR mb.motivo ILIKE '%' || :motivo || '%') and
                        (:observaciones IS NULL OR b.observaciones ILIKE '%' || :observaciones || '%') and
                        (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                        (
                         (
	                            (:numero_unico IS NULL OR b.mercaderia ILIKE '%' || :numero_unico || '%') and
	                            (:denominacion IS NULL OR m.den ILIKE '%' || :denominacion || '%') and
	                            (:lote IS NULL OR m.lote ILIKE '%' || :lote || '%') 
	                        ) or
	                        (
	                            (:numero_unico IS NULL OR b.hojalata ILIKE '%' || :numero_unico || '%') and
	                            (:denominacion IS NULL OR h.den ILIKE '%' || :denominacion || '%') and
	                            (:lote IS NULL OR h.lote ILIKE '%' || :lote || '%') 
	                        ) or
	                        ( 
	                            (:numero_unico IS NULL OR b.extracto ILIKE '%' || :numero_unico || '%') and
	                            (:denominacion IS NULL OR e.den ILIKE '%' || :denominacion || '%') and
	                            (:lote IS NULL OR e.lote ILIKE '%' || :lote || '%')
	                        )
						)
                    order by b.fecha_registro DESC;
                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"] if request.form["fecha_inicial"].strip() else None,
                                            "fecha_final": request.form["fecha_final"] if request.form["fecha_final"].strip() else None,
                                            "estado": request.form["estado"] if request.form["estado"].strip() else None,
                                            "numero_planilla": request.form["numero_planilla"] if request.form["numero_planilla"].strip() else None,
                                            "motivo": request.form["motivo"] if request.form["motivo"].strip() else None,
                                            "observaciones": request.form["observaciones"] if request.form["observaciones"].strip() else None,
                                            "responsable": request.form["responsable"] if request.form["responsable"].strip() else None,
                                            "numero_unico": request.form["numero_unico"] if request.form["numero_unico"].strip() else None,
                                            "denominacion": request.form["denominacion"] if request.form["denominacion"].strip() else None,
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
                m.llenadora_botella as llenadora,
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
                mra.fecha_elaboracion + INTERVAL '1 month' * v.meses AS reac_env_vto,
                mra.fecha_etiquetado + INTERVAL '1 month' * v.meses AS reac_eti_vto,
                mra.fecha_encajonado + INTERVAL '1 month' * v.meses AS reac_encaj_vto,
                mra.llenadora_botella as reac_llenadora,
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
                   (e.vto_meses = v.id) or
                   (mra.vto = v.id)
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
                m.cantidad as mercaderia_cantidad,
                d.hojalata,
                h.den as hojalata_den,
                h.lote as hojalata_lote,
                h.cantidad as hojalata_cantidad,
                d.extracto,
                e.den as extracto_den,
                e.lote as extracto_lote,
                e.cantidad as extracto_cantidad,
                d.reacondicionado,
                r.nueva_den as reacondicionado_den,
                mrd.numero_unico as reac_mercaderia_nu,
                mrd.lote as reac_mercaderia_lote,
                rd.cantidad as reacondicionado_cant,
                erd.numero_unico as reac_extracto_nu,
                erd.lote as reac_extracto_lote,
                d.fletero_codigo,
                d.fletero_nombre,
                d.patente,
                d.pin,
                d.observaciones,
                u.nombre,
                d.fecha_registro
            FROM despacho d
            LEFT JOIN usuario u ON d.responsable = u.id
            LEFT JOIN mercaderia m ON d.mercaderia = m.numero_unico
            LEFT JOIN hojalata h ON d.hojalata = h.numero_unico
            LEFT JOIN extracto e ON d.extracto = e.numero_unico
            LEFT JOIN reacondicionado r ON d.reacondicionado = r.numero_unico
            LEFT JOIN reacondicionado_detalle rd ON r.id = rd.reacondicionado
            LEFT JOIN mercaderia mrd ON rd.mercaderia_original = mrd.id
            LEFT JOIN extracto erd ON rd.extracto_original = erd.id
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
			ORDER BY d.fecha_registro DESC, rd.fecha_registro DESC;
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