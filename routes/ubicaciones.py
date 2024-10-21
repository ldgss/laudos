from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

ubicaciones_bp = Blueprint("ubicaciones", __name__)

@ubicaciones_bp.route("/ubicaciones")
def ubicaciones():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        title = "Ubicaciones"
        section = "Ubicaciones"
        return render_template("ubicaciones/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))