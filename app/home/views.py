#app/home/views.py

from flask import make_response,request,jsonify
#local imports
from app import user
from . import home

@home.route('/')
def homepage():
    """get requests for homepage"""
    return make_response(jsonify(
        {
        'message':'welcome to the hello-books app you can register in order to get the most out of the app'
        }
    )), 200

@home.route('/auth/api/v1/register',methods=['GET','POST'])
def register():
    """method to handle register requests"""
    if request.method == 'GET':
        return make_response(jsonify(
            {
                'message':'welcome to the register endpoint, use autenticated post requests to register'
            }
        )), 200
    if request.method == 'POST':
        details = request.get_json()
        username = details.get('username')
        email = details.get('email')
        password = details.get('password')
        confirm_pwd = details.get('confirm_pwd')
        try:
            response = user.register(username,email,password,confirm_pwd)
            return make_response(jsonify(
                {'message':response}
            )) 
        except Exception as e:
            return make_response(jsonify(
                {'message':e}
            )), 401
    return make_response(jsonify(
        {'message':'method not allowed,sorry'}
    )), 405

@home.route('/auth/api/v1/login',methods=['GET','POST'])
def login():
    """handles login requests"""
    if request.method == 'GET':
        return make_response(jsonify(
            {'message':'welcome to the login endpoint'}
        )), 200
