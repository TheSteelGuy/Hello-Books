#app/config.py
#coding:utf-8

import os 

class Baseconfig:
    """base config"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')


class Productionconfig(Baseconfig):
    """production based config"""
    TESTING = False


class Developmentconfig(Baseconfig):
    """config for development"""
    DEBUG = True
    SECRET_KEY = os.urandom(20)

class Testconfig(Baseconfig):
    """For testing the application"""
    DEBUG = True
    SECRET_KEY = os.urandom(20)

app_config = {
    'development':Developmentconfig,
    'testing' : Testconfig,
    'production':Productionconfig

}


 
