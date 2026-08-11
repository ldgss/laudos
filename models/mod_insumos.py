from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
from utils import helpers
from flask import session
import shlex
import re

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
        if 'H1' in numero_unico:
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

            sql = text("""
                        SELECT 
                            h.producto, 
                            h.den AS insumo_den,
                            h.lote,
                            h.numero_unico,
                            h.cantidad,
                            h.fecha_elaboracion + make_interval(months => v.meses) AS vto
                        FROM hojalata h 
                        JOIN vencimiento v ON v.id = h.vto_meses 
                        WHERE h.numero_unico = :numero_unico
                """)
            
            result = db.db.session.execute(
                        sql,
                        {"numero_unico": numero_unico}
                    )
            
            return result.mappings().first()
        elif 'PR' in numero_unico:
            sql_consumido = text("""
                SELECT 1
                FROM sticker_insumo_detalle sid
                JOIN insumo_envase ie ON ie.insumo = sid.numero_unico
                WHERE sid.numero_unico = :numero_unico
                LIMIT 1
            """)

            consumido = db.db.session.execute(
                sql_consumido,
                {"numero_unico": numero_unico}
            ).first()

            if consumido:
                return {
                    "error": True,
                    "mensaje": "El insumo ya se consumió"
                }

            sql = text("""
                    SELECT
                        si.arb_insumo_codigo AS producto,
                        si.arb_insumo_denominacion AS insumo_den,
                        si.lote,
                        sid.numero_unico,
                        sid.cantidad_parcial AS cantidad,
                        si.vto
                    FROM sticker_insumo si 
                    JOIN sticker_insumo_detalle sid ON sid.sticker_insumo_id = si.id 
                    WHERE sid.numero_unico = :numero_unico
                """)

            result = db.db.session.execute(
                        sql,
                        {"numero_unico": numero_unico}
                    )
            
            return result.mappings().first()
        elif 'T1' in numero_unico:
                    sql_consumido = text("""
                        SELECT 1
                        FROM mercaderia m
                        JOIN insumo_envase ie ON ie.insumo = m.numero_unico
                        WHERE m.numero_unico = :numero_unico
                        LIMIT 1
                    """)
        
                    consumido = db.db.session.execute(
                        sql_consumido,
                        {"numero_unico": numero_unico}
                    ).first()
        
                    if consumido:
                        return {
                            "error": True,
                            "mensaje": "El insumo ya se consumió"
                        }
        
                    sql = text("""
                            SELECT
                                m.producto AS producto,
                                m.den AS insumo_den,
                                m.lote,
                                m.numero_unico,
                                m.cantidad,
                                m.vto,
                                m.fecha_registro + make_interval(months => v.meses) AS vto
                            FROM mercaderia m 
                            JOIN vencimiento v ON v.id = m.vto
                            WHERE m.numero_unico = :numero_unico
                        """)
        
                    result = db.db.session.execute(
                                sql,
                                {"numero_unico": numero_unico}
                            )
                    
                    return result.mappings().first()
        else:
            return {
                "error": True,
                "mensaje": "Tipo de pallet inválido"
            }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": True,
            "mensaje": "Error interno al buscar el pallet"
        }

def guardar_insumos():
    try:
        reacondicionado = text("""
                    INSERT INTO
                    insumo_envase
                    (insumo, codigo_insumo, fecha_consumo, responsable, fecha_registro, 
                    lote_insumo, cantidad, den)
                    VALUES
                    (:insumo, :codigo_insumo, :fecha_consumo, :responsable, CURRENT_TIMESTAMP, 
                    :lote_insumo, :cantidad, :den)
                """
                )
        
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "insumo": request.form["den_fac"],
                                                "codigo_insumo": request.form["cta_alm"],
                                                "fecha_consumo": request.form["fecha_hora"],
                                                "responsable": session["id"],
                                                "lote_insumo": request.form["cod_lot"],
                                                "cantidad": request.form["can"],
                                                "den": request.form["insumo_den"],
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
            subcondicion.append(f"i_e.den::TEXT ILIKE '%{termino}%'")
            
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

def get_buscar_insumo_para_guardar_sticker():
    # cambiar a sqlserver para llamar a arballon
    try:
        # Conexión al motor de SQL Server
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            # Consulta parametrizada
            query = text("""
                SELECT
                    gv.cod_mae as arb_insumo_codigo,
                    gv.den as arb_insumo_denominacion
                FROM genmae_v2 gv
                WHERE lower(gv.den) LIKE :insumo_buscar
            """)

            data = request.get_json()
            insumo_buscar = data.get("insumo_buscar")

            # Reemplazar espacios por % para ampliar la query
            insumo_buscar = re.sub(r"\s+", "%", insumo_buscar)
            
            result = connection.execute(query, {
                'insumo_buscar': f'%{insumo_buscar}%'
            })
            
            # Usar keys() para mapear columnas y valores manualmente
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]

            return rows  # Retornar la lista de diccionarios

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_buscar_proveedor_para_guardar_sticker():
    # cambiar a sqlserver para llamar a arballon
    try:
        # Conexión al motor de SQL Server
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            # Consulta parametrizada
            query = text("""
                SELECT 
                    p.codigo as arb_proveedor_codigo, 
                    p.denominacion as arb_proveedor_denominacion, 
                    p.codigo_clase  as arb_proveedor_clase
                FROM proveedores p
                WHERE
                    (
                    lower(p.codigo_clase) LIKE '%agrico%' OR
                    lower(p.codigo_clase) LIKE '%calida%' OR
                    lower(p.codigo_clase) LIKE '%comerc%' OR
                    lower(p.codigo_clase) LIKE '%deposi%' OR
                    lower(p.codigo_clase) LIKE '%flete%' OR
                    lower(p.codigo_clase) LIKE '%generi%' OR
                    lower(p.codigo_clase) LIKE '%hojala%' OR
                    lower(p.codigo_clase) LIKE '%logist%' OR
                    lower(p.codigo_clase) LIKE '%manten%' OR
                    lower(p.codigo_clase) LIKE '%produc%'
                    )
                and
                lower(p.denominacion) LIKE :proveedor_buscar
            """)

            data = request.get_json()
            proveedor_buscar = data.get("proveedor_buscar")

            # Reemplazar espacios por % para ampliar la query
            proveedor_buscar = re.sub(r"\s+", "%", proveedor_buscar)
            print(f"searching {proveedor_buscar}")
            result = connection.execute(query, {
                'proveedor_buscar': f'%{proveedor_buscar}%'
            })
            
            # Usar keys() para mapear columnas y valores manualmente
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]

            return rows  # Retornar la lista de diccionarios

    except Exception as e:
        print(f"Error: {e}")
        return None

def lote_previo_sticker():
    try:
        sql = text("""
                    SELECT 
                        lote
                    FROM sticker_insumo
                    WHERE 
                        arb_insumo_codigo = :arb_insumo_codigo OR
                        arb_insumo_denominacion = :arb_insumo_denominacion
                    ORDER BY id DESC
                    LIMIT 1;
                """
                )

        data = request.get_json()
        resultado = db.db.session.execute(sql,
                                            {
                                                "arb_insumo_codigo": data.get("codigo"),
                                                "arb_insumo_denominacion": data.get("denominacion")
                                            }).mappings().first()
        if resultado is None:
            return None
        return resultado["lote"]
    except Exception as e:
        print(f"Error: {e}")
        return None

def generar_stickers():

    pallets_1 = int(request.form.get("pallets_1")) if request.form.get("pallets_1") else 0
    unidades_1 = int(request.form.get("unidades_1")) if request.form.get("unidades_1") else 0
    pallets_2 = int(request.form.get("pallets_2")) if request.form.get("pallets_2") else 0
    unidades_2 = int(request.form.get("unidades_2")) if request.form.get("unidades_2") else 0
    pallets_3 = int(request.form.get("pallets_3")) if request.form.get("pallets_3") else 0
    unidades_3 = int(request.form.get("unidades_3")) if request.form.get("unidades_3") else 0
    composicion = f"{pallets_1}x{unidades_1}+{pallets_2}x{unidades_2}+{pallets_3}x{unidades_3}"

    try:
        sticker = text("""
                    INSERT INTO 
                        public.sticker_insumo
                        (
                            arb_insumo_codigo, arb_insumo_denominacion, lote, 
                            comprobante_tipo, comprobante_numero, 
                            arb_proveedor_codigo, arb_proveedor_denominacion, arb_proveedor_clase, 
                            cantidad_total, cantidad_a_imprimir, 
                            responsable, fecha_registro, fecha_recepcion, observaciones, vto
                        )
                    VALUES
                        (
                            :arb_insumo_codigo, :arb_insumo_denominacion, :lote, 
                            :comprobante_tipo, :comprobante_numero, 
                            :arb_proveedor_codigo, :arb_proveedor_denominacion, :arb_proveedor_clase, 
                            :cantidad_total, :cantidad_a_imprimir, 
                            :responsable, CURRENT_TIMESTAMP, :fecha_recepcion, :observaciones, :vto
                        )
                        RETURNING id
                """
                )

        # UNA SOLA TRANSACCIÓN
        with db.db.session.begin():
            sticker_id = db.db.session.execute(sticker,
                {
                    "arb_insumo_codigo": request.form.get("arb_insumo_codigo"),
                    "arb_insumo_denominacion": request.form.get("arb_insumo_denominacion"),
                    "lote": request.form.get("lote"),
                    "comprobante_tipo": request.form.get("comprobante_tipo"),
                    "comprobante_numero": request.form.get("comprobante_numero"),
                    "arb_proveedor_codigo": request.form.get("arb_proveedor_codigo"),
                    "arb_proveedor_denominacion": request.form.get("arb_proveedor_denominacion"),
                    "arb_proveedor_clase": request.form.get("arb_proveedor_clase"),
                    "cantidad_total": request.form.get("cantidad_total"),
                    "cantidad_a_imprimir": composicion,
                    "responsable": session["id"],
                    "fecha_recepcion": request.form.get("fecha_recepcion"),
                    "observaciones": request.form.get("observaciones"),
                    "vto": request.form.get("vto") or None,
                }).scalar()

            for i in range(pallets_1):
                numero_unico = ultimo_numero_unico()
                db.db.session.execute(
                        text("""
                            INSERT INTO public.sticker_insumo_detalle
                                (numero_unico, sticker_insumo_id, 
                                cantidad_parcial, fecha_registro)
                            VALUES
                                (:numero_unico, :sticker_insumo_id, 
                                :cantidad_parcial, CURRENT_TIMESTAMP);
                            """),
                        {
                            "numero_unico" : numero_unico,
                            "sticker_insumo_id" : sticker_id,
                            "cantidad_parcial" : unidades_1
                        }        
                    )

            if pallets_2:
                for i in range(pallets_2):
                    numero_unico = ultimo_numero_unico()
                    db.db.session.execute(
                            text("""
                                INSERT INTO public.sticker_insumo_detalle
                                    (numero_unico, sticker_insumo_id, 
                                    cantidad_parcial, fecha_registro)
                                VALUES
                                    (:numero_unico, :sticker_insumo_id, 
                                    :cantidad_parcial, CURRENT_TIMESTAMP);
                                """),
                            {
                                "numero_unico" : numero_unico,
                                "sticker_insumo_id" : sticker_id,
                                "cantidad_parcial" : unidades_2
                            }        
                        )

            if pallets_3:
                for i in range(pallets_3):
                    numero_unico = ultimo_numero_unico()
                    db.db.session.execute(
                            text("""
                                INSERT INTO public.sticker_insumo_detalle
                                    (numero_unico, sticker_insumo_id, 
                                    cantidad_parcial, fecha_registro)
                                VALUES
                                    (:numero_unico, :sticker_insumo_id, 
                                    :cantidad_parcial, CURRENT_TIMESTAMP);
                                """),
                            {
                                "numero_unico" : numero_unico,
                                "sticker_insumo_id" : sticker_id,
                                "cantidad_parcial" : unidades_3
                            }        
                        )

            

        # si llego hasta aca el commit es automatico
        # devolver el id para redirigir a impresion
        return sticker_id
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None

def ultimo_numero_unico():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM sticker_insumo_detalle
                    ORDER BY numero_unico DESC
                    LIMIT 1
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        ultimo_id = result.scalar()
        year = datetime.now().year

        return helpers.next_id(ultimo_id, "PR", year)
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_listado_insumos_sticker(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de sticker_insumo
            subcondicion = []
            subcondicion.append(f"si.arb_insumo_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.arb_insumo_denominacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.comprobante_tipo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.comprobante_numero::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.arb_proveedor_codigo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.arb_proveedor_denominacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.arb_proveedor_clase::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.cantidad_total::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.cantidad_a_imprimir::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.fecha_recepcion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"si.vto::TEXT ILIKE '%{termino}%'")

            # todo: falta el join a sticker_insumo_detalle por numero unico
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT
                si.id,
                si.arb_insumo_denominacion as articulo,
                si.lote,
                si.arb_proveedor_denominacion as proveedor,
                si.comprobante_tipo as comprobante,
                si.comprobante_numero as numero,
                si.fecha_recepcion as recepcion,
                si.vto
            FROM sticker_insumo si 
            JOIN usuario u ON u.id = si.responsable 
            WHERE {condicion_final_ilike}
            ORDER BY si.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT
                                        si.id,
                                        si.arb_insumo_denominacion as articulo,
                                        si.lote,
                                        si.arb_proveedor_denominacion as proveedor,
                                        si.comprobante_tipo as comprobante,
                                        si.comprobante_numero as numero,
                                        si.fecha_recepcion as recepcion
                                    FROM sticker_insumo si 
                                    JOIN usuario u ON u.id = si.responsable 
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

def imprimir_sticker(id):
    try:
        sql = text("""
                    SELECT 
                        si.arb_insumo_denominacion as articulo,
                        si.arb_insumo_codigo as codigo,
                        si.lote,	
                        sid.numero_unico,
                        sid.cantidad_parcial,
                        si.cantidad_total,
                        si.arb_proveedor_denominacion as proveedor,
                        si.comprobante_tipo as comprobante,
                        si.comprobante_numero as numero,
                        si.vto,
                        si.fecha_recepcion as recepcion,
                        u.nombre as responsable
                    FROM sticker_insumo_detalle sid
                    JOIN sticker_insumo si ON si.id = sid.sticker_insumo_id
                    JOIN usuario u ON u.id = si.responsable
                    WHERE si.id = :id
                """
                )
        
        envasado = db.db.session.execute(sql,{"id": id})
        return envasado.mappings().all()
    except Exception as e:
        print(f"Error: {e}")
        return None