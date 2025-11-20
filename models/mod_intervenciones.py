from sqlalchemy.sql import text
from flask import session
from db import db
from datetime import datetime
import shlex
from flask import request
import traceback
import os, json
import string
import random
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

UPLOAD_FOLDER = "static/img/intervenciones"

def get_lineas_mantenimiento():
    try:
        sql = text("""
                    SELECT 
                    id, denominacion
                    FROM lineas_mantenimiento
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_tipo_de_fallo():
    try:
        sql = text("""
                    SELECT 
                    id, descripcion
                    FROM tipo_de_fallo
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None

# todo
def anular_intervencion():
    # CUIDADO - DANGER - DELETE ZONE
    try:
        anulacion = text("""
                    DELETE FROM intervencion_linea_productiva
                    WHERE id=:id;
                """
                )
        anulacion = db.db.session.execute(anulacion,
                                            {
                                                "id": request.form["intervencion_id"]                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None   

def guardar_intervencion():
    try:
        files = request.files.getlist("imagenes")
        rutas = []

        # Crear base de carpeta si no existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        for i, file in enumerate(files):
            if file and file.filename:
                filename = secure_filename(file.filename)
                
                # Nombre único y aleatorio
                random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                extension = filename.rsplit(".", 1)[-1]
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # %f → microsegundos, cortamos a milisegundos
                new_name = f"{random_part}{session['id']}{timestamp}{i}.{extension}"
                # extension = filename.rsplit(".", 1)[-1]
                # new_name = f"{session['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}.{extension}"
                path = os.path.join(UPLOAD_FOLDER, new_name)
                # file.save(path)
                guardar_imagen(file, path)
                rutas.append(f"/{path}")  # Lo que guardarás en PostgreSQL

        rutas_json = json.dumps(rutas)  # Serializar lista de imágenes

        sql = text("""
            INSERT INTO intervencion_linea_productiva 
                (linea_afectada, tipo_de_fallo, se_detuvo, 
                inicio, fin, quedo_operativa, 
                detalle, imagenes, responsable, 
                fecha_registro, duracion) 
            VALUES 
                (:linea_afectada, :tipo_de_fallo, :se_detuvo, 
                :inicio, :fin, :quedo_operativa, 
                :detalle, :imagenes, :responsable, 
                CURRENT_TIMESTAMP, GREATEST(
                        (:fin)::timestamptz - (:inicio)::timestamptz, INTERVAL '0')
                    )
            RETURNING id;
        """)

        result = db.db.session.execute(sql, {
            "linea_afectada": request.form.get("lineas_mantenimiento_id"),
            "tipo_de_fallo": request.form.get("tipo_de_fallo_id"),
            "se_detuvo": request.form.get("se_detuvo"),
            "inicio": request.form.get("inicio"),
            "fin": request.form.get("fin"),
            "quedo_operativa": request.form.get("quedo_operativa"),
            "detalle": request.form.get("detalle"),
            "imagenes": rutas_json,
            "responsable": session["id"]
        })

        new_id = result.scalar()
        db.db.session.commit()
        return new_id

    except Exception as e:
        db.db.session.rollback()
        print(e)
        return None
    
def guardar_imagen(file, path):
    max_size_kb=500
    img = Image.open(file)

    # Convertir a RGB si viene con canal alfa (transparencia)
    if img.mode in ("RGBA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = background
    else:
        img = img.convert("RGB")

    # Reducir resolución si es gigante
    img.thumbnail((1920, 1080))

    output = BytesIO()
    quality = 85  # calidad inicial

    # Guardar inicialmente
    img.save(output, format="JPEG", optimize=True, quality=quality)

    # Bajar calidad hasta que entre en el límite
    while output.getbuffer().nbytes > max_size_kb * 1024 and quality > 20:
        output = BytesIO()
        quality -= 5
        img.save(output, format="JPEG", optimize=True, quality=quality)

    # Guardar en disco
    with open(path, "wb") as f:
        f.write(output.getvalue())

def get_intervencion(id_intervenciones):
    try:
        sql = text("""
                    SELECT 
                        i.id, i.linea_afectada, i.tipo_de_fallo, 
                        i.se_detuvo, i.inicio, i.fin, 
                        i.quedo_operativa, i.detalle, i.imagenes, 
                        i.responsable, i.fecha_registro, i.duracion, 
                        u.nombre,
                        lm.denominacion as linea,
                        tf.descripcion as fallo
                    FROM intervencion_linea_productiva i
                    INNER JOIN usuario u on u.id = i.responsable
                    INNER JOIN lineas_mantenimiento lm on lm.id = i.linea_afectada
                    INNER JOIN tipo_de_fallo tf on tf.id = i.tipo_de_fallo
                    WHERE i.id = :id
                """
                )
        
        medicion = db.db.session.execute(sql,{
                                                "id": id_intervenciones
                                        })
        return medicion.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_estadisticas():
    try:
        sql = text("""
                    SELECT 
                    m.electricidad_acometida_norte_kw,
                    m.electricidad_acometida_este_kw,
                    m.gas_natural_m3,
                    m.agua_pozo_m3x100,
                    m.agua_caldera1_m3,
                    m.agua_caldera2_m3,
                    m.agua_caldera3_m3,
                    m.efluente_generado_m3,
                    u.nombre as responsable,
                    m.fecha_registro,
                    observaciones
                    FROM mediciones_de_energia m
                    inner join usuario u on u.id = m.responsable
                    ORDER BY m.id ASC
                    LIMIT 12;
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_intervenciones(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            subcondicion.append(f"i.inicio::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i.fin::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i.detalle::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"i.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"lm.denominacion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"tf.descripcion::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")
        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
                i.id, 
                i.inicio,
                i.fin,
                i.duracion,
                i.fecha_registro,
                lm.denominacion as linea,
                tf.descripcion as fallo,
                u.nombre as responsable
            FROM intervencion_linea_productiva i
            JOIN usuario u ON i.responsable = u.id
            INNER JOIN lineas_mantenimiento lm ON lm.id = i.linea_afectada
            INNER JOIN tipo_de_fallo tf ON tf.id = i.tipo_de_fallo
            WHERE {condicion_final_ilike}
            ORDER BY i.id DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                        i.id, 
                                        lm.denominacion as linea,
                                        tf.descripcion as fallo,
                                        u.nombre as responsable
                                    FROM intervencion_linea_productiva i
                                    JOIN usuario u ON i.responsable = u.id
                                    INNER JOIN lineas_mantenimiento lm ON lm.id = i.linea_afectada
                                    INNER JOIN tipo_de_fallo tf ON tf.id = i.tipo_de_fallo
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