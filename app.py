#################################################################################
# FLASK IMPORTS
#################################################################################

from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import session
from flask import flash
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

#################################################################################
# MODEL IMPORTS
#################################################################################

from models import mod_login

#################################################################################
# FLASK CONFIG
#################################################################################

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1234@localhost:5432/laudos'

#################################################################################
# DB CONFIG
#################################################################################

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

#################################################################################
# FLASK ROUTES
#################################################################################

@app.route("/")
def index():
    if session_on():
        title = "Laudos Solvencia S.A"
        body = f"Bienvenidos {session}"
        return render_template("index.html", title=title, body=body)
    else:
        return redirect(url_for("login_get"))


@app.get("/login")
def login_get():
    if session_on():
        return redirect(url_for("index"))
    else:
        title = "Ingresar"
        body = "Ingresar"
        return render_template("login/index.html", title=title, body=body)
    
@app.post("/login")
def login_post():
    usuario = request.form["usuario"]
    password = request.form["password"]
    result = mod_login.log_user(db,usuario, password)
    if result:
        session["id"] = result[0]
        session["usuario"] = result[1]
        session["password"] = result[2]
        session["fecha_creacion"] = result[3]
        session["fecha_modificacion"] = result[4]
        session["esta_activo"] = result[5]

        return redirect(url_for("index"))
    else:
        flash("usuario o contraseña incorrecta")
        return redirect(url_for("login_get"))
    

@app.route("/mercaderia")
def mercaderia():
    if session_on():
        title = "Mercaderia"
        body = "Mercaderia"
        return render_template("mercaderia/index.html", title=title, body=body)
    else:
        return redirect(url_for("login_get"))

#################################################################################
# ERROR PAGES
#################################################################################

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error/pagina_no_encontrada.html"), 404

#################################################################################
# UTIL DEF
#################################################################################

def session_on():
    if 'usuario' in session:
        return True
    return False
