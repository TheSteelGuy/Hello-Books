#app/home/__init__.py
#coding:utf-8

from flask import Blueprint

home = Blueprint('home',__name__)

from . import views


