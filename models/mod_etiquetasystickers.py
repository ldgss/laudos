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
        print(f"files: {request.files}")
        print(f"form: {request.form}")
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

        # si no habia id, insert
        if(not request.form["id_modal"]):
            sql = text("""
                INSERT INTO public.etiquetas_y_stickers
                    (codigo, codigo_clase, denominacion, imagen, responsable, fecha_registro)
                VALUES
                    (:codigo, :codigo_clase, :denominacion, :imagenes, :responsable, CURRENT_TIMESTAMP)
                RETURNING id;
            """)

            result = db.db.session.execute(sql, {
                "codigo": request.form.get("codigo_modal"),
                "codigo_clase": request.form.get("clase_modal"),
                "denominacion": request.form.get("denominacion_modal"),
                "imagenes": rutas_json,
                "responsable": session["id"]
            })
            new_id = result.scalar()
            db.db.session.commit()
            return new_id
        else:
        # si ya habia id, actualizar
            evento = f'Usuario {session["id"]} actualiza la etiqueta {request.form["denominacion_modal"]} a {rutas_json}'

            sql = text("""
                UPDATE
                       etiquetas_y_stickers
                SET 
                    imagen=:imagenes
                WHERE id=:id
            """)

            result = db.db.session.execute(sql, {
                "id": request.form["id_modal"],
                "imagenes": rutas_json,
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
                        id, codigo, codigo_clase, denominacion, imagen, responsable, fecha_registro
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
        
