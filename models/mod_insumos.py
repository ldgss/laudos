from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
from flask import session
import shlex

def get_buscar_insumo_para_guardar():
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

def buscar_insumo_con_laudo():
    numero_unico = request.form.get("numero_unico")

    try:
        sql_consumido = text("""
            SELECT 1
            FROM hojalata h
            JOIN insumo_envase ie ON h.numero_unico = ie.insumo
            WHERE h.numero_unico = :numero_unico
            LIMIT 1
        """)

        consumido = db.db.session.execute(
            sql_consumido,
            {"numero_unico": numero_unico}
        ).first()

        if consumido:
            return {
                "error": True,
                "mensaje": "El pallet ya se consumió"
            }

        if 'T1' in numero_unico:
            sql = text("SELECT * FROM mercaderia WHERE numero_unico = :numero_unico")
        elif 'H1' in numero_unico:
            sql = text("SELECT * FROM hojalata WHERE numero_unico = :numero_unico")
        elif 'E1' in numero_unico:
            sql = text("SELECT * FROM extracto WHERE numero_unico = :numero_unico")
        elif 'T2' in numero_unico:
            sql = text("SELECT * FROM reacondicionado WHERE numero_unico = :numero_unico")
        else:
            return {
                "error": True,
                "mensaje": "Tipo de pallet inválido"
            }

        result = db.db.session.execute(
            sql,
            {"numero_unico": numero_unico}
        )

        return result.mappings().first()

    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": True,
            "mensaje": "Error interno al buscar el pallet"
        }


# def buscar_insumo_con_laudo():
#     numero_unico = request.form.get("numero_unico")
#     try:
#         sql = ""
#         if 'T1' in numero_unico:
#             sql = text(""" SELECT * FROM mercaderia WHERE numero_unico = :numero_unico """)
#         elif 'H1' in numero_unico:
#             sql = text(""" SELECT * FROM hojalata WHERE numero_unico = :numero_unico """)
#         elif 'E1' in numero_unico:
#             sql = text(""" SELECT * FROM extracto WHERE numero_unico = :numero_unico """)
#         elif 'T2' in numero_unico:
#             sql = text(""" SELECT * FROM reacondicionado WHERE numero_unico = :numero_unico """)

        
#         result = db.db.session.execute(sql,
#                                             {
#                                                 "numero_unico": numero_unico,
#                                             })
#         return result.mappings().first()
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

def guardar_insumos():
    try:
        reacondicionado = text("""
                    INSERT INTO
                    insumo_envase
                    (insumo, codigo_insumo, fecha_consumo, responsable, fecha_registro, 
                    lote_insumo, cantidad)
                    VALUES
                    (:insumo, :codigo_insumo, :fecha_consumo, :responsable, CURRENT_TIMESTAMP, 
                    :lote_insumo, :cantidad)
                """
                )
        
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "insumo": request.form["den_fac"],
                                                "codigo_insumo": request.form["cta_alm"],
                                                "fecha_consumo": request.form["fecha_hora"],
                                                "responsable": session["id"],
                                                "lote_insumo": request.form["cod_lot"],
                                                "cantidad": request.form["can"]
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None

def get_listado_insumos(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de extracto
            subcondicion = []
            subcondicion.append(f"i_e.insumo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.codigo_insumo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.fecha_consumo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.lote_insumo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i_e.cantidad::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT i_e.*, u.*, i_e.id as insumo_envase_id
            FROM insumo_envase i_e
            JOIN usuario u ON i_e.responsable = u.id
            WHERE {condicion_final_ilike}
            ORDER BY i_e.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT i_e.*, u.*
                                    FROM insumo_envase i_e
                                    JOIN usuario u ON i_e.responsable = u.id
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

def anular_insumos():
    # CUIDADO - DANGER - DELETE ZONE
    try:
        anulacion = text("""
                    DELETE FROM insumo_envase
                    WHERE id=:id;
                """
                )
        anulacion = db.db.session.execute(anulacion,
                                            {
                                                "id": request.form["insumo_envase_id"]                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None