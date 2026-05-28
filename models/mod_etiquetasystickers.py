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

UPLOAD_FOLDER = "static/img/etiquetasystickers"

def listar_etiquetas_y_stickers_arballon():
    # cambiar a sqlserver para llamar a arballon
    try:
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            result = connection.execute(text("""
                SELECT ac.codigo, ac.denominacion, ac.codigo_clase 
                FROM arballon.dbo.articulos_completo ac 
                where 
                	(lower(ac.denominacion) like '%etiqueta%' or lower(ac.denominacion) like '%sticker%')
                	AND (lower(ac.codigo_clase) not like '%repone%')
                	AND (lower(ac.codigo_clase) not like '%librer%')
                	AND (lower(ac.codigo_clase) not like '%repmaq%')
                	AND (lower(ac.codigo_clase) not like '%bulone%')
                	AND (lower(ac.codigo_clase) not like '%cadcin%')
                	AND (lower(ac.codigo_clase) not like '%adhesi%')
                	AND (lower(ac.codigo_clase) not like '%manten%')
                	AND (lower(ac.codigo_clase) not like '%heracc%')
                	AND (lower(ac.codigo_clase) not like '%1inspr%')
                	AND (lower(ac.codigo_clase) not like '%varios%')
                	AND (lower(ac.codigo_clase) not like '%servar%')
                    AND (lower(ac.codigo) not like '%19005004%')
                	AND (lower(ac.codigo) not like '%19005006%')
                order by ac.denominacion;
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None

def guardar_etiquetasystickers():
    try:
        files = request.files.getlist("imagenes")
        rutas = []

        rutas = crear_ruta(files, rutas)

        imagen_modal = request.form.get("imagen_modal")
        # return point
        if imagen_modal:
            if rutas:
                print(f"cambiando imagen de: {imagen_modal} a {rutas}")
                imagen_anterior = json.dumps([imagen_modal])
                imagen_nueva = json.dumps(rutas)    
            else:
                print(f"manteniendo imagen de: {imagen_modal} a {rutas}")
                imagen_anterior = json.dumps([imagen_modal])
                imagen_nueva = imagen_anterior
        else:
            # viene desde carga nueva
            print(f"primer imagen: {rutas}")
            imagen_nueva = json.dumps(rutas)

        # si no habia id, insert
        if(not request.form["id_modal"]):
            sql = text("""
                INSERT INTO public.etiquetas_y_stickers
                    (codigo, codigo_clase, denominacion, imagen, responsable, fecha_registro, observacion, vigente)
                VALUES
                    (:codigo, :codigo_clase, :denominacion, :imagenes, :responsable, CURRENT_TIMESTAMP, :observacion, :vigente)
                RETURNING id;
            """)

            result = db.db.session.execute(sql, {
                "codigo": request.form.get("codigo_modal"),
                "codigo_clase": request.form.get("clase_modal"),
                "denominacion": request.form.get("denominacion_modal"),
                "imagenes": imagen_nueva,
                "responsable": session["id"],
                "observacion": request.form.get("observacion"),
                "vigente": request.form.get("vigente") or False
            })
            new_id = result.scalar()
            db.db.session.commit()
            return new_id
        else:
        # si ya habia id, actualizar
            evento = f'Se actualiza la etiqueta {request.form["denominacion_modal"]} de {imagen_anterior} a {imagen_nueva}, observacion: {request.form.get("observacion")}, vigente: {"si" if request.form.get("vigente") else "no"}'

            sql = text("""
                UPDATE
                       etiquetas_y_stickers
                SET 
                    imagen=:imagenes,
                    observacion=:observacion,
                    vigente=:vigente
                WHERE id=:id
            """)

            result = db.db.session.execute(sql, {
                "id": request.form["id_modal"],
                "imagenes": imagen_nueva,
                "observacion": request.form.get("observacion"),
                "vigente": request.form.get("vigente") or False
            })
            
            # registrar el update

            sql = text("""
                INSERT INTO etiquetas_y_stickers_u
                    (evento, responsable, fecha_registro)
                VALUES
                    (:evento, :responsable, CURRENT_TIMESTAMP);
                """)

            result = db.db.session.execute(sql, {
                "evento": evento,
                "responsable": session["id"]
            })
            db.db.session.commit()
            return True
    except Exception as e:
        db.db.session.rollback()
        print(e)
        return None

def crear_ruta(files, rutas):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    for i, file in enumerate(files):
        if file and file.filename:
            filename = secure_filename(file.filename)
            random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            extension = filename.rsplit(".", 1)[-1]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # %f → microsegundos, cortamos a milisegundos
            new_name = f"{random_part}{session['id']}{timestamp}{i}.{extension}"
            path = os.path.join(UPLOAD_FOLDER, new_name)
            guardar_imagen(file, path)
            rutas.append(f"/{path}")
    return rutas

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

def get_etiquetasystickers():
    try:
        data = request.get_json()
        codigo = data.get("codigo")
        denominacion = data.get("denominacion")
        sql = text("""
                    SELECT 
                        id, codigo, codigo_clase, denominacion, imagen, responsable, fecha_registro, observacion, vigente
                    FROM etiquetas_y_stickers
                    WHERE 
                        codigo ilike :codigo OR denominacion ilike :denominacion;
                """
                )
        
        resultado = db.db.session.execute(sql,{
                                                "codigo": codigo,
                                                "denominacion": denominacion
                                        })
        return [dict(row) for row in resultado.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def get_listado_etiquetasystickers(resultados_por_pagina, offset):
    try:
        query_sql = f"""
            SELECT 
                eys.id, 
                eys.codigo, 
                eys.codigo_clase, 
                eys.denominacion, 
                eys.observacion,
                eys.imagen::jsonb ->> 0 AS imagen,
                u.nombre as responsable, 
                eys.fecha_registro,
                eys.vigente
            FROM etiquetas_y_stickers eys
            JOIN usuario u ON u.id = eys.responsable
            ORDER BY eys.id DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                        id, codigo, codigo_clase, denominacion, imagen, responsable, fecha_registro
                                    FROM etiquetas_y_stickers eys
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