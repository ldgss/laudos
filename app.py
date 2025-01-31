
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
from routes import bloqueos
from routes import hojalata
from routes import reporte
from routes import anulacion
from routes import correcion
from routes import materia
from routes import despacho
from db import db
from datetime import timedelta
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
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@leo.solvencia.local:5432/laudosdb?client_encoding=utf8'
    app.config['SQLALCHEMY_BINDS'] = {
        'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+17+for+SQL+Server'
    }
else:
    print("modo de base de datos: produccion")
    user = tokens.production_user
    password = tokens.production_pass
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@leo.solvencia.local:5432/laudosdb?client_encoding=utf8'
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
app.register_blueprint(bloqueos.bloqueos_bp)
app.register_blueprint(hojalata.hojalata_bp)
app.register_blueprint(reporte.reporte_bp)
app.register_blueprint(anulacion.anulacion_bp)
app.register_blueprint(correcion.correccion_bp)
app.register_blueprint(materia.materia_bp)
app.register_blueprint(despacho.despacho_bp)

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
