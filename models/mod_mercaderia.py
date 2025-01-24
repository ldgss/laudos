from sqlalchemy.sql import text
from db import db
from datetime import datetime
import shlex

def listar_productos_arballon():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                SELECT cod_mae, den, cod_cls FROM genmae
                WHERE tip_mae = 4 AND (
                    cod_cls = 'Extrac' OR
                    cod_cls = 'Pas500' OR
                    cod_cls = 'Pelado' OR
                    cod_cls = 'Pulpa' OR
                    cod_cls = 'Pure' OR
                    cod_cls = 'Tri500' OR
                    cod_cls = 'Tri8' OR
                    cod_cls = 'Tri910' OR
                    cod_cls = 'Tri950' OR
                    cod_cls = 'Tritur'
                )
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_ultimo_id():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM mercaderia
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
            return f"{year}-T1-000000"
        else:
            # si ya existen pallets, aumentar el numero del id
            prefijo = str(datetime.now().year)
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = f"{prefijo}-T1-{nuevo_numero_str}"

            return nuevo_codigo
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_ultimo_id_extracto():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM extracto
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
            return f"{year}-E1-000000"
        else:
            # si ya existen pallets, aumentar el numero del id
            prefijo = str(datetime.now().year)
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = f"{prefijo}-E1-{nuevo_numero_str}"

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
    
def guardar_envasado(form, vto, lote):
    try:
        sql = text("""
                    INSERT INTO
                    mercaderia
                    (producto, observacion, cantidad, lote, fecha_elaboracion, 
                    responsable, numero_unico, vto, fecha_registro,
                    den)
                    VALUES
                    (:producto, :observacion, :cantidad, :lote, :fecha_elaboracion, 
                    :responsable, :numero_unico, :vto, CURRENT_TIMESTAMP,
                    :den)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observacion": form['observaciones'],
                                                "cantidad": form['cantidad'],
                                                "lote": lote,
                                                "fecha_elaboracion": f"{form['fecha']} {form['hora']}",
                                                "responsable": form['user_id'],
                                                "numero_unico": form['numero_unico'],
                                                "vto": vto['id'],
                                                "den": form['denominacion']
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def guardar_etiquetado(form, vto, lote):
    try:
        sql = text("""
                    INSERT INTO
                    mercaderia
                    (producto, observacion, cantidad, lote, fecha_etiquetado, 
                    responsable, numero_unico, vto, fecha_registro,
                    den)
                    VALUES
                    (:producto, :observacion, :cantidad, :lote, :fecha_etiquetado, 
                    :responsable, :numero_unico, :vto, CURRENT_TIMESTAMP,
                    :den)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observacion": form['observaciones'],
                                                "cantidad": form['cantidad'],
                                                "lote": lote,
                                                "fecha_etiquetado": f"{form['fecha']} {form['hora']}",
                                                "responsable": form['user_id'],
                                                "numero_unico": form['numero_unico'],
                                                "vto": vto['id'],
                                                "den": form['denominacion']
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def guardar_encajonado(form, vto, lote):
    try:
        sql = text("""
                    INSERT INTO
                    mercaderia
                    (producto, observacion, cantidad, lote, fecha_encajonado, 
                    responsable, numero_unico, vto, fecha_registro,
                    den)
                    VALUES
                    (:producto, :observacion, :cantidad, :lote, :fecha_encajonado, 
                    :responsable, :numero_unico, :vto, CURRENT_TIMESTAMP,
                    :den)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observacion": form['observaciones'],
                                                "cantidad": form['cantidad'],
                                                "lote": lote,
                                                "fecha_encajonado": f"{form['fecha']} {form['hora']}",
                                                "responsable": form['user_id'],
                                                "numero_unico": form['numero_unico'],
                                                "vto": vto['id'],
                                                "den": form['denominacion']
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def guardar_extracto(form, vto, lote):
    try:
        sql = text("""
                    INSERT INTO
                    extracto
                    (numero_unico, producto, fecha_elaboracion, lote, brix, numero_recipiente,
                    observaciones, vto_meses, responsable, fecha_registro, den)
                    VALUES
                    (:numero_unico, :producto, :fecha_elaboracion, :lote, :brix, :numero_recipiente,
                    :observaciones, :vto_meses, :responsable, CURRENT_TIMESTAMP, :den)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observaciones": form['observaciones'],
                                                "brix": form['brix'],
                                                "numero_recipiente": form['numero_recipiente'],
                                                "lote": lote,
                                                "fecha_elaboracion": f"{form['fecha']} {form['hora']}",
                                                "responsable": form['user_id'],
                                                "numero_unico": form['numero_unico'],
                                                "vto_meses": vto['id'],
                                                "den": form['denominacion']
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_envasado(numero_unico):
    try:
        sql = text("""
                    SELECT m.*, v.*, u.*
                    FROM mercaderia m
                    JOIN vencimiento v ON m.vto = v.id
                    JOIN usuario u ON m.responsable = u.id
                    WHERE numero_unico = :numero_unico 
                    AND fecha_etiquetado IS NULL
                    AND fecha_encajonado IS NULL
                    ORDER BY m.fecha_registro DESC
                """
                )
        
        envasado = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return envasado.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_etiquetado(numero_unico):
    try:
        sql = text("""
                    SELECT m.*, v.*, u.*
                    FROM mercaderia m
                    JOIN vencimiento v ON m.vto = v.id
                    JOIN usuario u ON m.responsable = u.id
                    WHERE numero_unico = :numero_unico
                    AND fecha_elaboracion IS NULL
                    AND fecha_encajonado IS NULL
                    ORDER BY m.fecha_registro DESC
                """
                )
        
        envasado = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return envasado.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_encajonado(numero_unico):
    try:
        sql = text("""
                    SELECT m.*, v.*, u.*
                    FROM mercaderia m
                    JOIN vencimiento v ON m.vto = v.id
                    JOIN usuario u ON m.responsable = u.id
                    WHERE numero_unico = :numero_unico
                    AND fecha_elaboracion IS NULL
                    AND fecha_etiquetado IS NULL
                    ORDER BY m.fecha_registro DESC
                """
                )
        
        envasado = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return envasado.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_extracto(numero_unico):
    try:
        sql = text("""
                    SELECT e.*, v.*, u.*
                    FROM extracto e
                    JOIN vencimiento v ON e.vto_meses = v.id
                    JOIN usuario u ON e.responsable = u.id
                    WHERE numero_unico = :numero_unico
                    ORDER BY e.fecha_registro DESC
                """
                )
        
        envasado = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return envasado.mappings().first()
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
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT m.*, u.*, v.*
            FROM mercaderia m
            JOIN usuario u ON m.responsable = u.id
            JOIN vencimiento v ON m.vto = v.id
            WHERE {condicion_final_ilike}
            AND fecha_etiquetado IS NULL
            AND fecha_encajonado IS NULL
            ORDER BY m.fecha_registro DESC
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
                                    WHERE {condicion_final_ilike}
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

def get_listado_etiquetado(terminos_de_busqueda, resultados_por_pagina, offset):
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
            subcondicion.append(f"m.fecha_etiquetado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT m.*, u.*, v.*
            FROM mercaderia m
            JOIN usuario u ON m.responsable = u.id
            JOIN vencimiento v ON m.vto = v.id
            WHERE {condicion_final_ilike}
            AND fecha_elaboracion IS NULL
            AND fecha_encajonado IS NULL
            ORDER BY m.fecha_registro DESC
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
                                    WHERE {condicion_final_ilike}
                                    AND fecha_elaboracion IS NULL
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
    
def get_listado_encajonado(terminos_de_busqueda, resultados_por_pagina, offset):
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
            subcondicion.append(f"m.fecha_encajonado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.vto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT m.*, u.*, v.*
            FROM mercaderia m
            JOIN usuario u ON m.responsable = u.id
            JOIN vencimiento v ON m.vto = v.id
            WHERE {condicion_final_ilike}
            AND fecha_elaboracion IS NULL
            AND fecha_etiquetado IS NULL
            ORDER BY m.fecha_registro DESC
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
                                    WHERE {condicion_final_ilike}
                                    AND fecha_elaboracion IS NULL
                                    AND fecha_etiquetado IS NULL
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
    
def get_listado_extracto(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de extracto
            subcondicion = []
            subcondicion.append(f"e.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.observaciones::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.brix::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_recipiente::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            
            # chequear cada termino en nombre usuario
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            # chequear cada termino en meses vencimiento
            subcondicion.append(f"v.meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"v.producto::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT e.*, u.*, v.*
            FROM extracto e
            JOIN usuario u ON e.responsable = u.id
            JOIN vencimiento v ON e.vto_meses = v.id
            WHERE {condicion_final_ilike}
            ORDER BY e.fecha_registro DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT e.*, u.*, v.*
                                    FROM extracto e
                                    JOIN usuario u ON e.responsable = u.id
                                    JOIN vencimiento v ON e.vto_meses = v.id
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