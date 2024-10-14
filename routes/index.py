from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from utils import helpers
from flask import Blueprint

index_bp = Blueprint("index", __name__)

@index_bp.get("/")
def index():
    if helpers.session_on():
        title = "Laudos Solvencia S.A"
        body = f"Bienvenido/a {session['nombre']}"
        return render_template("index.html", title=title, body=body)
    else:
        return redirect(url_for("login.login_get"))