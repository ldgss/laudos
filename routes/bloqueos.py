from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_hojalata
from models import mod_mercaderia
from models import mod_bloqueos
from flask import flash
from flask import request
from flask import session
from flask import jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta


bloqueos_bp = Blueprint("bloqueos", __name__)
resultados_por_pagina = 20
@bloqueos_bp.get("/bloqueos_produccion")
def bloqueos():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        title = "Bloqueo"
        section = "Bloqueo"
        return render_template("bloqueados/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    

# @bloqueos_bp.get("/bloqueos/agregar")
# def bloqueos_agregar():
#      if helpers.session_on() and helpers.authorized_to("bloqueo"):
#         # hojalata = mod_hojalata.get_hojalata(numero_unico)
        
#         title = "bloqueados"
#         section = "bloqueados"
#         return render_template("bloqueados/agregar.html", 
#                                title=title, section=section, 
#                                productos_arballon = session["productos_arballon"])
#      else:
#         return redirect(url_for("login.login_get"))

@bloqueos_bp.post("/bloqueos/agregar/agregarbloq")
def bloqueos_agregar_post():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # obtenemos el id solo del vencimiento necesario
        print(request.form)
        # el insert devuelve True si todo salio bien
        barcode = mod_bloqueos.insert_bloqueados_envasado(request.form)
        print(barcode)
        title = "Bloqueados"
        section = "Bloqueados"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("bloqueos.bloqueados_imprimir", id_unico=request.form["id_unico"]))
        
         
            
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("bloqueos.bloqueos"))
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.get("/bloqueos/imprimir/<id_unico>")
def bloqueados_imprimir(id_unico):
    print(id_unico)
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        bloqueados = mod_bloqueos.get_bloqueados(id_unico)
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/imprimir.html", 
                               title=title, section=section, 
                               bloqueados=bloqueados)
    else:
        return redirect(url_for("login.login_get"))

@bloqueos_bp.get("/bloqueos/agregar/<numero_unico>")
def bloqueos_agregar_id(numero_unico):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        hojalata = mod_mercaderia.get_envasado(numero_unico)
        motivo_bloqueo = mod_bloqueos.get_listado_motivo()
        
        title = "bloqueados"
        section = "bloqueados"
        return render_template("bloqueados/agregar.html", 
                               motivo_bloqueo = motivo_bloqueo,
                               title=title, section=section, 
                               hojalata=hojalata)
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.get("/bloqueos/agregarmultiple")
def bloqueos_agregar_multiple():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        proximo_id = mod_hojalata.get_ultimo_id()
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/agregarmultiple.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon_hojalata=session["productos_arballon_hojalata"])
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.post("/bloqueos/buscar")
def bloqueos_buscar():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        return redirect(url_for("bloqueos.bloqueados_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    

    

@bloqueos_bp.get("/bloqueos/listado/<terminos_de_busqueda>")
def bloqueados_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
      
        resultado = mod_bloqueos.get_listado_envasado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/listado.html",
<<<<<<< HEAD
                               offset=offset, 
=======
                               max=max,
                               min=min, 
>>>>>>> df675bf8361a19b09a1f48095171872cb434912b
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.post("/bloqueos/buscarbloqueados")
def bloqueos_buscarbloqueados():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        return redirect(url_for("bloqueos.bloqueados_listado_bloqueados", terminos_de_busqueda=request.form["buscarbloqueados"]))
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.get("/bloqueos/listadobloqueados/<terminos_de_busqueda>")
def bloqueados_listado_bloqueados(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
      
        resultado = mod_bloqueos.get_listado_bloqueados(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/listadobloqueados.html", 
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    

@bloqueos_bp.post("/bloqueos_produccion/agregar/liberacion")
def bloqueos_agregar_liberacion_post():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # Obtener los datos enviados desde el cliente.
        data = request.get_json()

        numero_unico = data.get('numero_unico')
        denominacion = data.get('denominacion')
        motivo = data.get('motivo')
        fecha_bloqueo = data.get('fecha_bloqueo')
        fecha_actual = data.get('fecha_actual')
        observaciones = data.get('observaciones')
        # Validar los datos (opcional)
        print(f"Datos recibidos: {data}")

        

        # el insert devuelve True si todo salio bien
        barcode = mod_bloqueos.insert_liberacion(data)
        print(barcode)
        title = "Bloqueados"
        section = "Bloqueados"
        if barcode is True:
            return jsonify(success=True)
    
        else:
            return jsonify(success=False, error="Error al guardar los datos")
    else:
        return redirect(url_for("login.login_get"))