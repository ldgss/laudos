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
                        u.nombre
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_elaboracion >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_elaboracion <= :fecha_final)
                        and (m.fecha_etiquetado is null)
                        and (m.fecha_encajonado is null)
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
                        u.nombre
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_etiquetado >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_etiquetado <= :fecha_final)
                        and (m.fecha_elaboracion IS NULL)
                        and (m.fecha_encajonado IS NULL)
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
                        u.nombre
                    FROM mercaderia m
                    INNER JOIN usuario u
                        ON m.responsable = u.id
                    WHERE 
                        (:fecha_inicial IS NULL OR m.fecha_encajonado >= :fecha_inicial)
                        AND (:fecha_final IS NULL OR m.fecha_encajonado <= :fecha_final)
                        and (m.fecha_elaboracion IS NULL)
                        and (m.fecha_etiquetado IS NULL)
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
                        u.nombre, 
                        r.fecha_registro, 
                        r.nueva_den, 
                        r.observaciones, 
                        r.tipo_reacondicionado,
                        m.lote 
                    FROM reacondicionado r
                    inner join usuario u on r.responsable = u.id	
                    inner join reacondicionado_detalle rd on r.id  = rd.reacondicionado
                    inner join mercaderia m on rd.mercaderia_original = m.id 
                    where 
                    (:fecha_inicial IS NULL OR r.fecha_registro >= :fecha_inicial) and
                    (:fecha_final IS NULL OR r.fecha_registro <= :fecha_final) and
                    (:responsable IS NULL OR u.nombre ILIKE '%' || :responsable || '%') and
                    (:denominacion IS NULL OR r.nueva_den ILIKE '%' || :denominacion || '%') and
                    (:lote_inicial IS NULL OR m.lote >= :lote_inicial) and
                    (:lote_final IS NULL OR m.lote <= :lote_final)
                    order by r.fecha_registro DESC
                    ;

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
                        e.den
                    FROM extracto e
                    inner join usuario u on e.responsable = u.id
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
    # todo
    try:
        sql = text("""
                    
                    ;

                """
                )
        envasado = db.db.session.execute(sql,
                                         {
                                            "fecha_inicial": request.form["fecha_inicial"],
                                            "fecha_final": request.form["fecha_final"],
                                            "responsable": request.form["responsable"],
                                            "denominacion": request.form["denominacion"],
                                            "lote_inicial": request.form["lote_inicial"],
                                            "lote_final": request.form["lote_final"],
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