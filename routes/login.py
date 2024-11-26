from flask import render_template
from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from models import mod_login
from utils import helpers
from models import mod_mercaderia



login_bp = Blueprint('login', __name__)

@login_bp.get("/login")
def login_get():
    if helpers.session_on():
        return redirect(url_for("index.index"))
    else:
        title = "Ingresar"
        section = "Ingresar"
        return render_template("login/index.html", title=title, section=section)

@login_bp.post("/login")
def login_post():
    usuario = request.form["usuario"]
    password = request.form["password"]
    user = mod_login.log_user(usuario, password)
    if user:
        session.update(user)
        productos_arballon = mod_mercaderia.listar_productos_arballon()
        productos_dict = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in productos_arballon
        ]
        session["productos_arballon"] = productos_dict
        return redirect(url_for("index.index"))
    else:
        flash("usuario o contraseña incorrecta")
        return redirect(url_for("login.login_get"))

@login_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.login_get"))