from sqlalchemy.sql import text
from db import db
from datetime import datetime
import shlex
from flask import request
import traceback
from flask import session


def get_ultimo_pallet_interno():
    try:
        sql = text("""
                    SELECT numero_pallet_interno
                    FROM hojalata
                    ORDER BY numero_pallet_interno DESC
                    LIMIT 1
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        ultimo_numero_pallet_interno = result.scalar()
        return int(ultimo_numero_pallet_interno) + 1 if ultimo_numero_pallet_interno is not None else 0
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_ultimo_id():
    try:
        sql = text("""
                    SELECT numero_unico
                    FROM hojalata
                    ORDER BY numero_unico DESC
                    LIMIT 1
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        ultimo_id = result.scalar()
        
        if not ultimo_id:
            # si es el primer pallet
            year = datetime.now().year
            return f"{year}-H1-000000"
        else:
            # si ya existen pallets, aumentar el numero del id
            prefijo = str(datetime.now().year)
            sufijo = int(ultimo_id[-6:])
            nuevo_numero = sufijo + 1
            nuevo_numero_str = f"{nuevo_numero:06d}"
            nuevo_codigo = f"{prefijo}-H1-{nuevo_numero_str}"

            return nuevo_codigo
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def guardar_hojalata(form, vto, lote):
    try:
        sql = text("""
                    INSERT INTO public.hojalata
                        (producto, observacion, fecha_elaboracion, 
                        lote, lote_cuerpo, lote_tapa, cantidad, 
                        numero_unico, responsable, vto_meses, 
                        fecha_registro, den, numero_pallet_interno)
                    VALUES
                        (:producto, :observacion, :fecha_elaboracion, 
                        :lote, :lote_cuerpo, :lote_tapa, :cantidad, 
                        :numero_unico, :responsable, :vto_meses, 
                        CURRENT_TIMESTAMP, :den, :numero_pallet_interno)
                """
                )
        
        envasado = db.db.session.execute(sql,
                                            {
                                                "producto": form['cod_mae'],
                                                "observacion": form['observaciones'],
                                                "fecha_elaboracion": f"{form['fecha']}",
                                                "lote": lote,
                                                "lote_cuerpo": None,
                                                "lote_tapa": None,
                                                "cantidad": form['cantidad'],
                                                "numero_unico": form['numero_unico'],
                                                "responsable": session["id"],
                                                "vto_meses": vto['id'],
                                                "den": form['denominacion'],
                                                "numero_pallet_interno": form['numero_pallet_interno']
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        error_traceback = traceback.format_exc()
        print(f"e: {e}")
        print(f"tb: {error_traceback}")
        return None

def get_hojalata(numero_unico):
    try:
        sql = text("""
                    SELECT 
                        h.numero_unico,
                        h.den,
                        h.numero_pallet_interno,
                        h.fecha_elaboracion,
                        v.meses as meses,
                        h.lote,
                        h.lote_cuerpo,
                        h.lote_tapa,
                        h.cantidad,
                        u.nombre as responsable_nombre
                    FROM hojalata h
                    JOIN vencimiento v ON h.vto_meses = v.id
                    JOIN usuario u ON h.responsable = u.id
                    WHERE numero_unico = :numero_unico 
                    ORDER BY h.fecha_registro DESC
                """
                )
        
        envasado = db.db.session.execute(sql,{"numero_unico": numero_unico})
        return envasado.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_hojalata(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            # chequear cada termino en cada columna de mercaderia
            subcondicion = []
            subcondicion.append(f"h.producto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.observacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.fecha_elaboracion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote_cuerpo::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.lote_tapa::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.cantidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.numero_unico::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.vto_meses::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.numero_pallet_interno::TEXT ILIKE '%{termino}%'")
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
            ORDER BY h.fecha_registro DESC
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