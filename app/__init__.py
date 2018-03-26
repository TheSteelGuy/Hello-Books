#app/__init__.property
#coding:utf-8

"""the init file controls the application
   all essential configaration are done here
"""
#third party imports
from flask import Flask
#local imports
from app.config import app_config
from  classes import User
from classes import Admin

user = User()
admin_user = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config.from_object(app_config[config_name])
    from admin import admin as admin_blueprint
    from home import home as home_blueprint
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)

    return app
