
from flask import Flask
from api.routes import api
from flasgger import Swagger
import jwt
import datetime, os
from functools import wraps

sec_key = str(os.environ.get("SECRET_KEY",'test'))
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = sec_key
    swagger = Swagger(app)
    app.register_blueprint(api, url_prefix="/api/v1")
    return app

