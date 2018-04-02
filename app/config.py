#app/config.py
#coding:utf-8

import os 

class Baseconfig:
    """base config"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DBASE_URI')


class Productionconfig(Baseconfig):
    """production based config"""
    TESTING = False


class Developmentconfig(Baseconfig):
    """config for development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:collo0@localhost/hello_books'
    SECRET_KEY = os.urandom(24)

class Testconfig(Baseconfig):
    """For testing the application"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:collo0@localhost/hello_tests"
    SECRET_KEY = os.urandom(10)

app_config = {
    'development':Developmentconfig,
    'testing' : Testconfig,
    'production':Productionconfig

}


 