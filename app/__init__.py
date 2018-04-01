#app/__init__.property
#coding:utf-8

"""the init file controls the application
   all essential configaration are done here
"""
#third party imports
from flask import Flask
#local imports
from app.config import app_config
from  .models.user import User
from .models.admin import Admin
from . error import method_not_allowed, server_error, resource_not_found

user = User()
admin_user = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config.from_object(app_config[config_name])
    from .admin import admin as admin_blueprint
    from .home import home as home_blueprint
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_error_handler(500, server_error)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, resource_not_found)

    return app
