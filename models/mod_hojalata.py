from sqlalchemy.sql import text
from db import db
from datetime import datetime

def listar_productos_arballon_hojalata():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""SELECT cod_mae, den, cod_cls 
                FROM genmae
                WHERE tip_mae = 4 AND (cod_cls = 'Extrac' OR
                                             cod_cls = 'Pas500' OR
                                             cod_cls = 'Pelado' OR
                                             cod_cls = 'Pulpa' OR
                                             cod_cls = 'Pure' OR
                                             cod_cls = 'Tri500' OR
                                             cod_cls = 'Tri8' OR
                                             cod_cls = 'Tri910' OR
                                             cod_cls = 'Tri950' OR
                                             cod_cls = 'Tritur') 
                                             AND (cod_mae > '901010'
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
                    FROM hojalata
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
            return f"{year}-H-000000"
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

def get_vencimiento_meses(vto_id):
    try:
        sql = text("""
                    SELECT *
                    FROM vencimiento
                    WHERE id = :id
                """
                )
        
        vencimiento = db.db.session.execute(sql,{"id": vto_id})
        return vencimiento.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def insert_mercaderia(form, vto):
    try:
        sql = text("""
                    INSERT INTO
                    hojalata
                   (producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad,   
                    numero_unico, responsable, vto_meses, fecha_registro)
                    VALUES
                    (:producto, :observacion, :fecha_elaboracion, :lote, :lote_cuerpo, :lote_tapa, :cantidad,
                    :numero_unico, :responsable,  :vto_meses, CURRENT_TIMESTAMP)
                """
                )
        
        hojalata = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observacion": form['observaciones'],
                                                "fecha_elaboracion": f"{form['fecha']} {form['hora']}",
                                                "lote": form['lote'],
                                                "lote_cuerpo": form['lote'],
                                                "lote_tapa": form['lote'],
                                                "cantidad": form['cantidad'],
                                                "numero_unico": form['numero_unico'],
                                                "responsable": form['user_id'],                                                
                                                "vto_meses": vto['id'],
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_hojalata(numero_unico):
    try:
        sql = text("""
                    SELECT h.*, v.*, u.*
                    FROM hojalata h
                    JOIN vencimiento v ON h.vto_meses = v.id
                    JOIN usuario u ON h.responsable = u.id
                    WHERE numero_unico = :numero_unico
                """
                )
        
        hojalata = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return hojalata.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo
        terminos_de_busqueda = terminos_de_busqueda.split()
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de hojalata
            subcondicion = []
            subcondicion.append(f"h.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.numero_unico::TEXT ILIKE '%{termino}%'")
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
