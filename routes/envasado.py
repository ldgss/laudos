from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session
from datetime import datetime
from dateutil.relativedelta import relativedelta


envasado_bp = Blueprint("envasado", __name__)

@envasado_bp.get("/envasado")
def envasado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.get("/envasado/agregar")
def envasado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # enviar al form el listado de productos/marcas
        # asi como tmb el ultimo id incrementado en uno
        productos_arballon = mod_mercaderia.listar_productos_arballon()
        proximo_id = mod_mercaderia.get_ultimo_id()
        productos_dict = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in productos_arballon
        ]
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/agregar.html", title=title, section=section, proximo_id=proximo_id,productos_arballon=productos_dict)
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.post("/envasado/agregar")
def envasado_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # el insert devuelve True si todo salio bien
        barcode = mod_mercaderia.insert_mercaderia(request.form, vto)
        title = "Envasado"
        section = "Envasado"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("envasado.envasado_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("envasado.envasado_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.get("/envasado/imprimir/<numero_unico>")
def envasado_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        envasado = mod_mercaderia.get_envasado(numero_unico)
        vto_meses = mod_mercaderia.get_vencimiento_meses(envasado["vto"])
        fecha_vencimiento = envasado['fecha_elaboracion'] + relativedelta(months=vto_meses["meses"])
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/imprimir.html", 
                               title=title, section=section, 
                               envasado=envasado,
                               fecha_vencimiento=fecha_vencimiento)
    else:
        return redirect(url_for("login.login_get"))