from flask import Flask
from api.routes import api
from flasgger import Swagger
import jwt
import datetime
from functools import wraps

app = None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tech_challenge'
    swagger = Swagger(app)
    app.register_blueprint(api, url_prefix="/api/v1")
    return app

