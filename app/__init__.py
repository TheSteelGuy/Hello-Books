"""
app/__init__.py
coding:utf-8

the init file controls the application
all essential configaration are done here
"""
#third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI
from flask_cors import CORS
#local imports
from app.config import app_config
from . error import method_not_allowed, server_error, resource_not_found


db = SQLAlchemy()

def create_app(config_name):
    ''' functions which creates the app'''
    app = FlaskAPI(__name__)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)

    #import and register blueprints
    from app.admin import admin as admin_blueprint
    from app.home import home as home_blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_error_handler(500, server_error)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, resource_not_found)

    return app
