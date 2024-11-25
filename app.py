
from flask import Flask
import secrets
from routes import login
from routes import envasado
from routes import etiquetado
from routes import encajonado
from routes import insumos
from routes import ubicaciones
from routes import extracto
from routes import index
from routes import errors
from routes import bloqueos
from routes import hojalata
from db import db

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1234@localhost:5432/laudos'
app.config['SQLALCHEMY_BINDS'] = {'sqlserver':'mssql+pyodbc://arballon_RO:SolArb2024@Sql-server.solvencia.local/arballon?driver=ODBC+Driver+17+for+SQL+Server'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.db.init_app(app)
app.register_blueprint(login.login_bp)
app.register_blueprint(envasado.envasado_bp)
app.register_blueprint(etiquetado.etiquetado_bp)
app.register_blueprint(encajonado.encajonado_bp)
app.register_blueprint(ubicaciones.ubicaciones_bp)
app.register_blueprint(insumos.insumos_bp)
app.register_blueprint(index.index_bp)
app.register_blueprint(errors.errors_bp)
app.register_blueprint(extracto.extracto_bp)
app.register_blueprint(bloqueos.bloqueos_bp)
app.register_blueprint(hojalata.hojalata_bp)
