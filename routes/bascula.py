from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_bascula
from flask import jsonify
from flask import flash
from flask import request
import socket
from win32printing import Printer

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
        imprimir_texto(datos)
        return jsonify({"status": "ok", "message": "Impresión enviada"})
    else:
        return redirect(url_for("login.login_get"))
    
def imprimir_texto(datos):
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