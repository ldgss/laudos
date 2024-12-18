
from flask import Flask
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
from db import db
from datetime import timedelta
from flask import session
from utils import tokens


app = Flask(__name__)
app.secret_key = secrets.token_hex()

if app.debug:
    print("modo de base de datos: desarrollo")
    user = tokens.development_user
    password = tokens.development_pass
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@leo.solvencia.local:5432/laudosdb'
    app.config['SQLALCHEMY_BINDS'] = {
        'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+17+for+SQL+Server'
    }
else:
    print("modo de base de datos: produccion")
    user = tokens.production_user
    password = tokens.production_pass
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@leo.solvencia.local:5432/laudosdb'
    app.config['SQLALCHEMY_BINDS'] = {
        # 'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+18+for+SQL+Server'
        'sqlserver': 'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
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

