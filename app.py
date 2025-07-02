
from flask import Flask
from flask_swagger import swagger
import logging
from logging.handlers import RotatingFileHandler
import secrets
from routes import login
from routes import envasado
from routes import etiquetado
from routes import encajonado
from routes import reacondicionado
from routes import insumos
from routes import ubicaciones
from routes import extracto
from routes import index
from routes import errors
from routes import bloqueo
from routes import reporte
from routes import anulacion
from routes import correcion
from routes import materia
from routes import despacho
from routes import kpi
from routes import usuario
from routes.usuario import active_users
from routes import bascula
from routes import retiro
from db import db
from datetime import timedelta
from datetime import datetime
from flask import session
from utils import tokens


app = Flask(__name__)
app.secret_key = secrets.token_hex()

# logging

log_format = (
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
)
logging.basicConfig(
    level=logging.DEBUG,  # Nivel más detallado
    format=log_format,
)

file_handler = RotatingFileHandler("app.log", maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

app.logger.debug("app started...")

# modes

if app.debug:
    print("modo de base de datos: desarrollo")
    user = tokens.development_user
    password = tokens.development_pass
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@{tokens.development_db}'
    app.config['SQLALCHEMY_BINDS'] = {
        'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+17+for+SQL+Server'
    }
else:
    print("modo de base de datos: produccion")
    user = tokens.production_user
    password = tokens.production_pass
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@{tokens.production_db}'
    app.config['SQLALCHEMY_BINDS'] = {
        # 'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+18+for+SQL+Server'
        'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
db.db.init_app(app)
app.register_blueprint(login.login_bp)
app.register_blueprint(index.index_bp)
app.register_blueprint(errors.errors_bp)
app.register_blueprint(envasado.envasado_bp)
app.register_blueprint(etiquetado.etiquetado_bp)
app.register_blueprint(encajonado.encajonado_bp)
app.register_blueprint(extracto.extracto_bp)
app.register_blueprint(reacondicionado.reacondicionado_bp)
app.register_blueprint(ubicaciones.ubicaciones_bp)
app.register_blueprint(insumos.insumos_bp)
app.register_blueprint(bloqueo.bloqueo_bp)
app.register_blueprint(reporte.reporte_bp)
app.register_blueprint(anulacion.anulacion_bp)
app.register_blueprint(correcion.correccion_bp)
app.register_blueprint(materia.materia_bp)
app.register_blueprint(despacho.despacho_bp)
app.register_blueprint(kpi.kpi_bp)
app.register_blueprint(usuario.usuario_bp)
app.register_blueprint(bascula.bascula_bp)
app.register_blueprint(retiro.retiro_bp)

# swagger

@app.route("/spec")
def spec():
    """
    Endpoint para obtener la documentación Swagger.
    ---
    responses:
      200:
        description: Devuelve la documentación de Swagger.
    """
    return swagger(app)

# ping para chequear conexion

@app.route('/ping')
def ping():
    return "pong", 200

@app.before_request
def actualizar_ultima_actividad():
    if session.get("nombre"):
        ahora = datetime.now()
        # 8 minutos de inactividad
        timeout = 8 * 60
        usuario_encontrado = False

        # Actualizar la última actividad si el usuario ya está en la lista
        for usuario in active_users:
            if usuario["usuario"] == session["nombre"]:
                usuario["ultima_actividad"] = ahora
                usuario_encontrado = True
                break

        # Si el usuario no estaba en la lista, agregarlo
        if not usuario_encontrado:
            active_users.append(
                {
                    "usuario": session["nombre"],
                    "ultima_actividad": ahora
                }
            )

        # Limpiar usuarios inactivos sin modificar la lista mientras se itera
        active_users[:] = [usuario for usuario in active_users if (ahora - usuario["ultima_actividad"]).seconds <= timeout]
