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
                    :responsable, :fecha)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "mercaderia": form['id_unico'],
                                                "hojalata": None,
                                                "extracto": None,
                                                "estado": True,
                                                "numero_planilla": form['numero_planilla'],
                                                "motivo": form['id_motivo'],
                                                "observaciones": form['observaciones'],
                                                "responsable": form['user_id'],
                                                "fecha": f"{form['fecha']} {form['hora']}",
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def insert_liberacion(data):
    try:
        sql = text("""
                    INSERT INTO
                    bloqueado
                   (mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones,   
                    responsable, fecha_registro)
                    VALUES
                    (:mercaderia, :hojalata, :extracto, :estado, :numero_planilla, :motivo, :observaciones,
                    :responsable, :fecha)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "mercaderia": data.get('numero_unico'),
                                                "hojalata": None,
                                                "extracto": None,
                                                "estado": False,
                                                "numero_planilla": 9999,
                                                "motivo": 24,
                                                "observaciones": data.get('observaciones'),
                                                "responsable": data.get('id_usuario'),
                                                "fecha": data.get('fecha_actual'),
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
                    SELECT b.mercaderia AS bloqueado_mercaderia, u.*, mb.*, m.*
                    FROM bloqueado b
                    JOIN usuario u ON b.responsable = u.id
                    JOIN motivo_bloqueo mb ON b.motivo = mb.id
                    JOIN mercaderia m ON b.mercaderia = m.numero_unico
                    WHERE b.mercaderia = :id_unico
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
            LEFT JOIN bloqueado b ON m.numero_unico = CAST(b.mercaderia AS text)
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
                                    LEFT JOIN bloqueado b ON m.numero_unico = CAST(b.mercaderia AS text)
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
    
def get_listado_bloqueados(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = terminos_de_busqueda.split()
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"b.mercaderia::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.motivo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.responsable::TEXT ILIKE '%{termino}%'")
            
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")


            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT DISTINCT ON (COALESCE(b.mercaderia, b.hojalata, b.extracto)) 
            b.*, 
            u.*, 
            mb.motivo AS mbmotivo, 
            m.den AS denmercaderia, 
            m2.den AS mercaderia_den, 
            h.den AS hojalata_den, 
            e.den AS extracto_den
            FROM bloqueado b
            JOIN usuario u ON b.responsable = u.id
            JOIN motivo_bloqueo mb ON b.motivo = mb.id
            LEFT JOIN mercaderia m ON b.mercaderia = m.numero_unico
            LEFT JOIN mercaderia m2 ON m2.numero_unico = b.mercaderia
            LEFT JOIN hojalata h ON h.numero_unico = b.hojalata
            LEFT JOIN extracto e ON e.numero_unico = b.extracto
            WHERE {condicion_final_ilike}
              AND b.estado = TRUE
              ORDER BY COALESCE(b.mercaderia, b.hojalata, b.extracto), b.fecha_registro DESC
              LIMIT :limit OFFSET :offset;
            
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT b.*, u.*
                                    FROM bloqueado b
                                    JOIN usuario u ON b.responsable = u.id
                                    WHERE {condicion_final_ilike}
                                    AND b.estado = True
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
    
def get_listado_motivo():
    try:
        sql = text("""
            SELECT id, motivo, mercaderia
            FROM motivo_bloqueo
            WHERE mercaderia = True;
        """)

        # Ejecutar la consulta
        resultados = db.db.session.execute(sql)

        # Convertir los resultados de CursorResult en una lista de motivos
        motivos = [(row[0], row[1]) for row in resultados.fetchall()]  # Usamos [0] porque solo hay una columna en la consulta
        print(motivos)

        # Verificar si no hay resultados
        if not motivos:
            print("No se encontraron motivos.")
        

        return motivos  # Devuelve la lista de motivos

    except Exception as e:
        print(f"Error al obtener el listado de motivos: {e}")
        return []  # Si ocurre un error, devolvemos una lista vacía