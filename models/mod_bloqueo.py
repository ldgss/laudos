from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
from flask import session
import shlex
import traceback

def listar_motivo_bloqueo():
    try:
        motivos = text("""
                SELECT 
                    mb.id,
                    mb.motivo,
                    mb.mercaderia as motivo_mercaderia,
                    mb.hojalata as motivo_hojalata,
                    mb.extracto as motivo_extracto
                FROM motivo_bloqueo mb   
        """)
        return db.db.session.execute(motivos).fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_bloqueo():
    # cambiar a sqlserver para llamar a arballon
    try:
        # Conexión al motor de SQL Server
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            # Consulta parametrizada
            query = text("""
                SELECT cta_alm, den_fac, cod_lot, can
                FROM arballon.dbo.almlot_v1
                WHERE 
                    cta_alm = :cta_alm COLLATE SQL_Latin1_General_CP1_CI_AS
                    AND cod_lot COLLATE SQL_Latin1_General_CP1_CI_AS LIKE :cod_lot;
            """)

            data = request.get_json()
            cta_alm = data.get("cta_alm")
            cod_lot = data.get("cod_lot")

            # Ejecutar la consulta con parámetros
            result = connection.execute(query, {
                'cta_alm': cta_alm,
                'cod_lot': f"%{cod_lot}%"
            })
            
            # Usar keys() para mapear columnas y valores manualmente
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]

            return rows  # Retornar la lista de diccionarios

    except Exception as e:
        print(f"Error: {e}")
        return None

def cambiar_bloqueo():
    try:
        reacondicionado = text("""
                    INSERT INTO bloqueado
                    (mercaderia, hojalata, extracto, 
                    estado, numero_planilla, motivo, 
                    observaciones, responsable, fecha_registro)
                    VALUES
                    (:mercaderia, :hojalata, :extracto, 
                    :estado, :numero_planilla, :motivo, 
                    :observaciones, :responsable, CURRENT_TIMESTAMP);
                """
                )
        
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "mercaderia" : request.form.get("numero_unico") if 'T1' in request.form.get("numero_unico") else None, 
                                                "hojalata" : request.form.get("numero_unico") if 'H1' in request.form.get("numero_unico") else None, 
                                                "extracto" : request.form.get("numero_unico") if 'E1' in request.form.get("numero_unico") else None, 
                                                "estado" : "Bloqueado" if request.form.get("estado") else "Liberado",
                                                "numero_planilla" : request.form.get("numero_planilla"),
                                                "motivo" : request.form.get("motivo"),
                                                "observaciones" : request.form.get("observaciones"),
                                                "responsable" : session["id"]
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"tb: {traceback.format_exc()}")
        print(f"Error: {e}")
        return None

def get_listado_bloqueo(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de extracto
            subcondicion = []
            subcondicion.append(f"b.estado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.numero_planilla::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"b.fecha_registro::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"mb.motivo::TEXT ILIKE '%{termino}%'")
            
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.observacion::TEXT ILIKE '%{termino}%'")
            
            subcondicion.append(f"h.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.observacion::TEXT ILIKE '%{termino}%'")
            
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.brix::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.observaciones::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
                m.den as mden,
                m.numero_unico as m_numero_unico,
                h.den as hden,
                h.numero_unico as h_numero_unico,
                e.den as eden,
                e.numero_unico as e_numero_unico,
                b.estado,
                b.numero_planilla,
                mb.motivo,
                b.observaciones,
                u.nombre,
                b.fecha_registro
            FROM bloqueado b
            full outer JOIN mercaderia m ON b.mercaderia = m.numero_unico 
            full outer join hojalata h ON b.hojalata = h.numero_unico
            full outer join extracto e ON b.extracto = e.numero_unico
            left JOIN motivo_bloqueo mb ON b.motivo = mb.id
            left JOIN usuario u ON b.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY b.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                        m.den as mden,
                                        m.numero_unico as m_numero_unico,
                                        h.den as hden,
                                        h.numero_unico as h_numero_unico,
                                        e.den as eden,
                                        e.numero_unico as e_numero_unico,
                                        b.estado,
                                        b.numero_planilla,
                                        mb.motivo,
                                        b.observaciones,
                                        u.nombre,
                                        b.fecha_registro
                                    FROM bloqueado b
                                    full outer JOIN mercaderia m ON b.mercaderia = m.numero_unico 
                                    full outer join hojalata h ON b.hojalata = h.numero_unico
                                    full outer join extracto e ON b.extracto = e.numero_unico
                                    left JOIN motivo_bloqueo mb ON b.motivo = mb.id
                                    left JOIN usuario u ON b.responsable = u.id
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

