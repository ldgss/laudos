from sqlalchemy.sql import text
from db import db
from datetime import datetime
import shlex


def insert_bloqueados_hojalata(form):
    try:
        sql = text("""
                    INSERT INTO
                    bloqueado
                   (mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones,   
                    responsable, fecha_registro)
                    VALUES
                    (:mercaderia, :hojalata, :extracto, :estado, :numero_planilla, :motivo, :observaciones,
                    :responsable, CURRENT_TIMESTAMP)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "mercaderia": form['id_unico'],
                                                "hojalata": form['id_unico'],
                                                "extracto": form['id_unico'],
                                                "estado": True,
                                                "numero_planilla": form['numero_planilla'],
                                                "motivo": form['Motivo'],
                                                "observaciones": form['observaciones'],
                                                "responsable": form['user_id'],
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def insert_bloqueados_envasado(form):
    try:
        sql = text("""
                    INSERT INTO
                    bloqueado
                   (mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones,   
                    responsable, fecha_registro)
                    VALUES
                    (:mercaderia, :hojalata, :extracto, :estado, :numero_planilla, :motivo, :observaciones,
                    :responsable, CURRENT_TIMESTAMP)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "mercaderia": form['id_unico'],
                                                "hojalata": form['id_unico'],
                                                "extracto": form['id_unico'],
                                                "estado": True,
                                                "numero_planilla": form['numero_planilla'],
                                                "motivo": form['Motivo'],
                                                "observaciones": form['observaciones'],
                                                "responsable": form['user_id'],
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_bloqueados(id_unico):
    try:
        sql = text("""
                    SELECT b.*, u.*
                    FROM bloqueado b
                    JOIN usuario u ON b.responsable = u.id
                    WHERE hojalata = :id_unico
                """
                )
        
        bloqueados = db.db.session.execute(sql,{"id_unico": id_unico})
        return bloqueados.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_hojalata(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"h.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT h.*, u.*, v.*
            FROM hojalata h
            JOIN usuario u ON h.responsable = u.id
            JOIN vencimiento v ON h.vto_meses = v.id
            WHERE {condicion_final_ilike}
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT h.*, u.*, v.*
                                    FROM hojalata h
                                    JOIN usuario u ON h.responsable = u.id
                                    JOIN vencimiento v ON h.vto_meses = v.id
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
    
def get_listado_envasado(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"m.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en bloqueados
            


            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT m.*, u.*, v.*
            FROM mercaderia m
            JOIN usuario u ON m.responsable = u.id
            JOIN vencimiento v ON m.vto = v.id
            LEFT JOIN bloqueado b ON m.numero_unico = b.mercaderia
            WHERE {condicion_final_ilike}
            AND b.mercaderia IS NULL
            AND fecha_etiquetado IS NULL
            AND fecha_encajonado IS NULL
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT m.*, u.*, v.*
                                    FROM mercaderia m
                                    JOIN usuario u ON m.responsable = u.id
                                    JOIN vencimiento v ON m.vto = v.id
                                    LEFT JOIN bloqueado b ON m.numero_unico = b.mercaderia
                                    WHERE {condicion_final_ilike}
                                    AND b.mercaderia IS NULL
                                    AND fecha_etiquetado IS NULL
                                    AND fecha_encajonado IS NULL
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