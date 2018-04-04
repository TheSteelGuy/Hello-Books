#app/__init__.property
#coding:utf-8

"""the init file controls the application
   all essential configaration are done here
"""
#third party imports
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
#local imports
from app.config import app_config
from  .models.user import User
from .models.admin import Admin
from . error import method_not_allowed, server_error, resource_not_found

user_object = User()
admin_user = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config['JWT_SECRET_KEY'] = os.urandom(10) 
    app.config.from_object(app_config[config_name])
    ACCESS_EXPIRES = timedelta(minutes=15)
    REFRESH_EXPIRES = timedelta(days=10)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
    jwt = JWTManager(app)
    from .admin import admin as admin_blueprint
    from .user import user as user_blueprint
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_error_handler(500, server_error)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, resource_not_found)

    return app
