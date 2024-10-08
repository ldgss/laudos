from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
import json

envasado_bp = Blueprint("envasado", __name__)

@envasado_bp.route("/envasado")
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
        productos_arballon = mod_mercaderia.get_mercaderia()
        
        productos_dict = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in productos_arballon
        ]
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/agregar.html", title=title, section=section, productos_arballon=productos_dict)
    else:
        return redirect(url_for("login.login_get"))