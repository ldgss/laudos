from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_bascula
from flask import jsonify
from flask import flash
from flask import request
from utils import clasificador
import time
import json
import cv2
import ast
import base64
import numpy as np
import socket
from win32printing import Printer
import win32print # de pywin32

# la impresora debe estar instalada en el cliente
# o en el servidor ????????????????????????????
# IMPRESORA = r"\\mrslave\Brother - laboratorio"
IMPRESORA = r"\\mrslave\Datamax-O'Neil E-4205A Mark III"

bascula_bp = Blueprint("bascula", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@bascula_bp.get("/bascula")
def bascula():
    if helpers.session_on() and helpers.authorized_to("materia"):
        title = "Bascula"
        section = "Bascula"
        return render_template("bascula/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@bascula_bp.post("/bascula/buscar")
def bascula_buscar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        return redirect(url_for("bascula.bascula_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))

@bascula_bp.get("/bascula/agregar")
def bascula_agregar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        title = "Bascula"
        section = "Bascula"
        return render_template("bascula/agregar.html", 
                               title=title, section=section
                               )
    else:
        return redirect(url_for("login.login_get"))

@bascula_bp.get("/bascula/tara")
def bascula_detalle():
    if helpers.session_on() and helpers.authorized_to("materia"):
        result = leer_bascula()
        if result:
            return jsonify(result)
        else:
            return jsonify({})
    else:
        return redirect(url_for("login.login_get"))

def leer_bascula(ip='192.168.23.77', port=1001, bytes=14):
    try:
        # la bascula usa un socket udp
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)
            # mandamos algo para despertar la bascula
            sock.sendto(b'\n', (ip, port))
            lectura, _ = sock.recvfrom(bytes)
            peso_bascula = lectura.decode('ascii').strip()
            return peso_bascula
    except (socket.timeout, socket.error) as e:
        return f"Error: {e}"
    
@bascula_bp.post("/bascula/agregar")
def bascula_agregar_post():
    if helpers.session_on() and helpers.authorized_to("materia") and not helpers.authorized_to_action("limitado"):
        resultado = mod_bascula.guardar_bascula()
        if resultado:
            return redirect(url_for("bascula.bascula_imprimir", id=resultado))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("bascula.bascula_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@bascula_bp.get("/bascula/imprimir/<id>")
def bascula_imprimir(id):
    if helpers.session_on() and helpers.authorized_to("materia"):
        bascula = mod_bascula.get_bascula(id)
        title = "Bascula"
        section = "Bascula"
        return render_template("bascula/imprimir.html", 
                               title=title, section=section, 
                               bascula=bascula)
    else:
        return redirect(url_for("login.login_get"))
    
@bascula_bp.post("/bascula/imprimir/sticker")
def bascula_imprimir_sticker():
    if helpers.session_on() and helpers.authorized_to("materia"):
        datos = request.json
        # imprimir_texto_win32_printing(datos)
        imprimir_texto_win32_print(datos)
        return jsonify({"status": "ok", "message": "Impresión enviada"})
    else:
        return redirect(url_for("login.login_get"))
    
def imprimir_texto_win32_printing(datos):
    texto_font = {
        "height": 8,
    }
    peso_font = {
        "height": 12,
    }
    with Printer(printer_name=IMPRESORA, auto_page=True, margin= (20, 10, 10, 10)) as printer:
        printer.text(f"FECHA: {datos["fecha"]}", font_config=texto_font)
        printer.text(f"DIA: {datos["dia"]}", font_config=texto_font)
        printer.text(f"HORA: {datos["hora"]}", font_config=texto_font)
        printer.text(f"MODO: {datos["modo"]}", font_config=texto_font)
        printer.text(f"CHOFER: {datos["chofer"]}", font_config=texto_font)
        printer.text(f"DOMINIO: {datos["dominio"]}", font_config=texto_font)
        printer.text(f"IPM: {datos["ipm"]}", font_config=texto_font)
        printer.text(f"PESO: {datos["peso"]} KG", font_config=peso_font)

def imprimir_texto_win32_print(datos):
    epl = f"""
N
q800
Q250,24
A50,20,0,3,1,1,N,"FECHA: {datos['fecha']}"
A50,60,0,3,1,1,N,"CHOFER: {datos['chofer']}"
A50,100,0,3,1,1,N,"DOMINIO: {datos['dominio']}"
A50,140,0,4,1,1,N,"PESO: {datos['peso']} KG"
P1
"""

    raw = epl.encode("ascii")

    h = win32print.OpenPrinter(IMPRESORA)
    try:
        job = win32print.StartDocPrinter(h, 1, ("Sticker", None, "RAW"))
        win32print.StartPagePrinter(h)
        win32print.WritePrinter(h, raw)
        win32print.EndPagePrinter(h)
        win32print.EndDocPrinter(h)
    finally:
        win32print.ClosePrinter(h)

@bascula_bp.get("/bascula/listado/<terminos_de_busqueda>")
def bascula_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("materia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_bascula.get_listado_bascula(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Bascula"
        section = "Bascula"
        return render_template("bascula/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))

# clasificacion por imagenes

@bascula_bp.get("/bascula/clasificacion")
def bascula_clasificacion():
    if helpers.session_on() and helpers.authorized_to("materia"):
        title = "Bascula"
        section = "Clasificacion por imagenes"
        return render_template("bascula/clasificacion.html", 
                               title=title, section=section
                               )
    else:
        return redirect(url_for("login.login_get"))

@bascula_bp.post("/bascula/clasificar_muestra")
def bascula_clasificar_muestra():
    if helpers.session_on() and helpers.authorized_to("materia") and not helpers.authorized_to_action("limitado"):
        
        req_data = request.get_json()
        if not req_data:
            return jsonify({"error": "No se recibieron datos JSON válidos."}), 400

        image_data_url = req_data.get("image_data")
        roi_str = req_data.get("coordenadas")
        ipm = req_data.get("ipm")
        
        if not image_data_url or not roi_str:
            return jsonify({"error": "Faltan datos de la cámara o de la zona de recorte."}), 400
        
        try:
            # Decodificar Base64 a matriz OpenCV EN MEMORIA (sin guardar archivo aún)
            header, encoded = image_data_url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            roi = ast.literal_eval(roi_str)
        except Exception as e:
            return jsonify({"error": f"Error procesando la imagen o las coordenadas: {str(e)}"}), 400

        radio = 8
        
        # truco temporal: si predict_tomato_maturity estrictamente requiere una RUTA de archivo, 
        # puedes usar un archivo temporal en memoria o escribirlo un segundo y borrarlo. 
        # O idealmente actualizar predict_tomato_maturity para que acepte la matriz `img` directo.
        # Asumiendo que aún necesita ruta temporal para el análisis en caliente:
        temp_path = f"static/img/clasificaciones/temp_{ipm}.jpg"
        cv2.imwrite(temp_path, img)
        
        analisis = clasificador.predict_tomato_maturity(temp_path, roi=roi, radio=radio)
        
        # Limpiamos inmediatamente el archivo temporal del análisis en caliente para no acumular basura
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if analisis:
            return jsonify({"analisis": analisis})
        else:
            return jsonify({"error": "Error al intentar analizar la imagen con el clasificador."}), 500
    else:
        return jsonify({"error": "No autorizado o sesión expirada."}), 403


@bascula_bp.post("/bascula/clasificacion_guardar")
def bascula_clasificacion_guardar():
    if helpers.session_on() and helpers.authorized_to("materia") and not helpers.authorized_to_action("limitado"):
        
        ipm = request.form.get("ipm")
        muestras_json_str = request.form.get("muestras_json")
        
        if not muestras_json_str:
            flash("No hay muestras para guardar.")
            return redirect(url_for("bascula.bascula"))

        clasificacion_detalle = []
        try:
            muestras = json.loads(muestras_json_str)
            
            # AQUÍ ES DONDE SÍ GUARDAMOS EN DISCO LAS IMÁGENES DEFINITIVAS DE CADA MUESTRA ACEPTADA
            for index, muestra in enumerate(muestras):
                image_data_url = muestra.get("image_data")
                header, encoded = image_data_url.split(",", 1)
                image_bytes = base64.b64decode(encoded)
                
                np_arr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                # Nombre de archivo único y definitivo para la BD
                timestamp = int(time.time() * 1000)
                image_path = f"static/img/clasificaciones/{ipm}_{index}_{timestamp}.jpg"
                cv2.imwrite(image_path, img)
                clasificacion_detalle.append(
                    {
                        "imagen" : image_path,
                        "coordenadas_mascara" : muestra.get("coordenadas"),
                        "analisis" : muestra.get("analisis")
                    }
                )
                
                # Reemplazamos el Base64 en el diccionario por la ruta física que se guardará en la BD
                muestra["imagen"] = image_path
            
            # Actualizamos el valor que consumirá tu módulo de guardado con las rutas físicas ya listas
            request.form = request.form.copy() # Hacemos mutable el form si fuera necesario
            # (O asegúrate de pasar 'muestras' ya procesadas a tu función de guardado)

        except Exception as e:
            flash(f"Error procesando las imágenes del lote: {str(e)}")
            return redirect(url_for("bascula.bascula"))

        resultado = mod_bascula.guardar_bascula_clasificacion(clasificacion_detalle) # Asegúrate de que este módulo lea el JSON con las rutas corregidas
        if resultado:
            return redirect(url_for("bascula.bascula_imprimir_clasificacion", 
                                    ipm=resultado)
                            )
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("bascula.bascula"))
    else:
        return redirect(url_for("login.login_get"))

@bascula_bp.get("/bascula/imprimir_clasificacion/<ipm>")
def bascula_imprimir_clasificacion(ipm):
    if helpers.session_on() and helpers.authorized_to("materia"):
        clasificacion = mod_bascula.get_bascula_clasificacion(ipm)
        if clasificacion:

            print("="*50)
            print(f"clasificacion: {clasificacion}")
            print("="*50)

            title = "Bascula - Clasificacion"
            section = "Imprimir clasificacion"
            return render_template("bascula/imprimir_clasificacion.html", 
                                    title=title, section=section, 
                                    clasificacion=clasificacion)
        else:
            flash("No se encontro la clasificacion buscada.")
            return redirect(url_for("bascula.bascula"))
    else:
        return redirect(url_for("login.login_get"))