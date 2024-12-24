from sqlalchemy.sql import text
from db import db
from datetime import datetime
from flask import request
from itertools import cycle
from flask import session

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
    
def get_ubicacion_nombre():
    try:
        sql = text("""
                    SELECT *
                    FROM ubicacion_nombre
                   ;
                """
                )
        
        result = db.db.session.execute(sql)
        
        return result.mappings().all()
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
    
def guardar_ubicaciones():
    try:
        reacondicionado = text("""
                    INSERT INTO
                    ubicacion
                    (ubicacion_fila, mercaderia, hojalata, extracto, 
                    responsable, fecha_registro, insumo_envase, ubicacion_profundidad, ubicacion_altura, reacondicionado)
                    VALUES
                    (:ubicacion_fila, :mercaderia, :hojalata, :extracto, 
                    :responsable, CURRENT_TIMESTAMP, :insumo_envase, :ubicacion_profundidad, :ubicacion_altura, :reacondicionado)
                """
                )
        print(request.form)
        reacondicionado = db.db.session.execute(reacondicionado,
                                            {
                                                "ubicacion_fila": request.form["id_ubicacion"],
                                                "mercaderia": request.form["numero_unico"] if 'T1' in request.form["numero_unico"] else None,
                                                "reacondicionado": request.form["numero_unico"] if 'T2' in request.form["numero_unico"] else None,
                                                "hojalata": request.form["numero_unico"] if 'H1' in request.form["numero_unico"] else None,
                                                "extracto": request.form["numero_unico"] if 'E1' in request.form["numero_unico"] else None,
                                                "responsable": session["id"],
                                                "insumo_envase": request.form["numero_unico"] if 'I1' in request.form["numero_unico"] else None,
                                                "ubicacion_profundidad": request.form["profundidad"],
                                                "ubicacion_altura": request.form["altura"],
                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None
    
def get_ubicaciones(numero_unico):
    try:
        sql = text("""
                    SELECT u.*, un.posicion, un.sector, us.nombre AS responsable_de_movimiento
                    FROM ubicacion u
                    JOIN ubicacion_nombre un ON u.ubicacion_fila = un.id
                    JOIN usuario us ON u.responsable = us.id
                    WHERE 
					    u.mercaderia = :numero_unico OR
						u.hojalata = :numero_unico OR
						u.extracto = :numero_unico OR
						u.insumo_envase = :numero_unico OR
						u.reacondicionado = :numero_unico
						ORDER BY u.fecha_registro DESC	
                """
                )
        
        result = db.db.session.execute(sql,{"numero_unico": numero_unico})
        result = result.mappings().all() or {}
        return result 
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_ubicaciones(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = terminos_de_busqueda.split()
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            # chequear cada termino en cada columna de ubicacion
            subcondicion.append(f"u.responsable::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.ubicacion_fila::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.mercaderia::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"m.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.hojalata::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.extracto::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"e.den::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.insumo_envase::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.ubicacion_profundidad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.ubicacion_altura::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.reacondicionado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u_n.id::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u_n.posicion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u_n.sector::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"usuario.nombre::TEXT ILIKE '%{termino}%'")
            

            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")

        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        
        query_sql = f"""
            
WITH ubicacion_con_row AS (
    SELECT 
    	u.responsable,
        u.ubicacion_fila,
        u.mercaderia,
        m.den as mden,
        u.hojalata,
        h.den as hden,
        u.extracto,
        e.den as eden,
        u.fecha_registro,
        u.insumo_envase,
        u.ubicacion_profundidad,
        u.ubicacion_altura,
        u.reacondicionado,
        u_n.id as ubicacion_fila_2,
        u_n.posicion,
        u_n.sector,
        usuario.id as usuario_id,
        usuario.nombre,
        ROW_NUMBER() OVER (
            PARTITION BY 
                u.mercaderia, u.reacondicionado
            ORDER BY u.fecha_registro DESC
        ) AS rn
    FROM ubicacion u
    LEFT JOIN ubicacion_nombre u_n ON u.ubicacion_fila = u_n.id
    LEFT JOIN usuario ON u.responsable = usuario.id
    left join mercaderia m on m.numero_unico = u.mercaderia
    left join hojalata h on h.numero_unico = u.hojalata
    left join extracto e on e.numero_unico = u.extracto
    WHERE 
        {condicion_final_ilike}
)
SELECT 
		u.responsable,
        u.ubicacion_fila,
        u.mercaderia,
        m.den as mden,
        u.hojalata,
        h.den as hden,
        u.extracto,
        e.den as eden,
        u.fecha_registro,
        u.insumo_envase,
        u.ubicacion_profundidad,
        u.ubicacion_altura,
        u.reacondicionado,
        u_n.id as ubicacion_fila_2,
        u_n.posicion,
        u_n.sector,
        usuario.id as usuario_id,
        usuario.nombre
FROM ubicacion_con_row AS u
LEFT JOIN ubicacion_nombre u_n ON u.ubicacion_fila = u_n.id
LEFT JOIN usuario ON u.responsable = usuario.id
left join mercaderia m on m.numero_unico = u.mercaderia
left join hojalata h on h.numero_unico = u.hojalata
left join extracto e on e.numero_unico = u.extracto
WHERE u.rn = 1
ORDER BY u.fecha_registro DESC
LIMIT :limit OFFSET :offset;




        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        query_count_sql = f"""
            
WITH ubicacion_con_row AS (
    SELECT 
    	u.responsable,
        u.ubicacion_fila,
        u.mercaderia,
        m.den,
        u.hojalata,
        h.den,
        u.extracto,
        e.den,
        u.fecha_registro,
        u.insumo_envase,
        u.ubicacion_profundidad,
        u.ubicacion_altura,
        u.reacondicionado,
        u_n.id as ubicacion_fila_2,
        u_n.posicion,
        u_n.sector,
        usuario.id as usuario_id,
        usuario.nombre,
        ROW_NUMBER() OVER (
            PARTITION BY 
                u.mercaderia, u.reacondicionado
            ORDER BY u.fecha_registro DESC
        ) AS rn
    FROM ubicacion u
    LEFT JOIN ubicacion_nombre u_n ON u.ubicacion_fila = u_n.id
    LEFT JOIN usuario ON u.responsable = usuario.id
    left join mercaderia m on m.numero_unico = u.mercaderia
    left join hojalata h on h.numero_unico = u.hojalata
    left join extracto e on e.numero_unico = u.extracto
    WHERE 
        {condicion_final_ilike}
)
SELECT 
		u.responsable,
        u.ubicacion_fila,
        u.mercaderia,
        m.den,
        u.hojalata,
        h.den,
        u.extracto,
        e.den,
        u.fecha_registro,
        u.insumo_envase,
        u.ubicacion_profundidad,
        u.ubicacion_altura,
        u.reacondicionado,
        u_n.id as ubicacion_fila_2,
        u_n.posicion,
        u_n.sector,
        usuario.id as usuario_id,
        usuario.nombre
FROM ubicacion_con_row AS u
LEFT JOIN ubicacion_nombre u_n ON u.ubicacion_fila = u_n.id
LEFT JOIN usuario ON u.responsable = usuario.id
left join mercaderia m on m.numero_unico = u.mercaderia
left join hojalata h on h.numero_unico = u.hojalata
left join extracto e on e.numero_unico = u.extracto
WHERE u.rn = 1;



        """

        total_resultado = db.db.session.execute(text(query_count_sql))

        total_paginas = total_resultado.rowcount // resultados_por_pagina
        if total_resultado.rowcount % resultados_por_pagina != 0:
            total_paginas += 1
        return [resultados.fetchall(), total_paginas]

    except Exception as e:
        print(f"Error: {e}")
        return None