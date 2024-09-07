
from flask import Flask
import secrets
from models import mod_login
from utils import helpers
from routes import login
from routes import mercaderia
from routes import extracto
from routes import index
from routes import errors
from db import db

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1234@localhost:5432/laudosdb'
db.db.init_app(app)
app.register_blueprint(login.login_bp)
app.register_blueprint(mercaderia.mercaderia_bp)
app.register_blueprint(index.index_bp)
app.register_blueprint(errors.errors_bp)
app.register_blueprint(extracto.extracto_bp)

