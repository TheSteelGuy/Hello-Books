#app/admin/views.py

from flask import make_response, request, jsonify, session
from werkzeug.security import generate_password_hash
import re
#local imports
from app.models import User
from app.models import TokenBlacklisting
from app.authenticate import token_required
from . import auth

@auth.route('/auth/api/v1/register',methods=['POST'])
def register():
    """method to handle register requests"""
    if request.method == 'POST':
        details = request.get_json()
        first_name = details.get('first_name')
        second_name = details.get('second_name')
        email = details.get('email')
        national_id = details.get('national_id')
        password = details.get('password')
        confirm_pwd = details.get('confirm_pwd')
        if len(first_name) < 4 or len(second_name) < 4:    
           return make_response(jsonify(
               {'message':'first and second name must be four letters or more!'}
           )), 409
        if not User.validate_email(email):    
           return make_response(jsonify(
               {'message':"Invalid email"}
           )), 409
        if password != confirm_pwd:    
           return make_response(jsonify(
               {'message':'password mistmatch'}
           )), 400
        if password != confirm_pwd:    
           return make_response(jsonify(
               {'message':'password mistmatch'}
           )), 400
        if password < 4:    
           return make_response(jsonify(
               {'message': 'password too short'}  
           )), 409
        if national_id.isalpha():    
           return make_response(jsonify(
               {'message':'national id must be digits'}
           )), 400
        if first_name.isdigit() or second_name.isdigit:    
           return make_response(jsonify(
               {'message':'Name must be an alphabet'}
           )), 400
        user = User.query.filter_by(email=email).first()
        if user: 
           return make_response(jsonify(
               {'message':'user already registred, login'}
           )), 201
        else:
           user = User(first_name, second_name, email, national_id, password)
           user.save_user()
           auth_token = user.token_generate(user.id)
           return make_response(jsonify(
               {
               'message':'registration successfull',
               'authentication token':auth_token.decode()
               }
           )), 201

            

@auth.route('/auth/api/v1/login',methods=['POST'])
def login():
    """handles login requests"""
    if request.method == 'POST':
        details = request.get_json()
        email = details.get('email')
        password = details.get('password')
        user = User.query.filter_by(email=email).first()
        if user == None:          
            return make_response(jsonify(
                {'message':'user does not exist'}
            )), 200
        elif user and user.verify_password(password):
            auth_token = user.token_generate(user.id)
            return make_response(jsonify(
                {
                    'message':'successfully logged in',
                    'authentication token': auth_token.decode()
                }
            )), 200

@auth.route('/api/auth/logout', methods=['POST'])
def logout():
    if request.method=='POST':
       auth_token = request.headers.get('Authorization')
       if auth_token:
           response = User.decode_token(auth_token)
           if not isinstance(response, str):
              blacklist = TokenBlacklisting(token=auth_token)
              try:
                  blacklist.save_token()
                  return make_response(jsonify(
                       {'message':'successfully logged out'}
                  )), 403
              except Exception:
                   return make_response(jsonify(
                       {'message':Exception}
                   )), 200
           return make_response(jsonify(
               {'message':response}
           )), 404
       return make_response(jsonify(
           {'message':'invalid token,detected, please provide valid token'}
       )), 401
    
@auth.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """allowes user to reset password"""
    if request.method == 'POST':
       email = request.json.get('email')
       new_password = request.json.get('new_password')
       if len(new_password.strip()) < 4:    
          return make_response(jsonify(
               {'message': 'password too short'}
          )), 409
       user = User.query.filter_by(email=email).first()
       if user:
            user.password = user.generate_password_hash(new_password)
            user.save_user()
            return make_response(jsonify(
                {
                    'messaage':'password reset successful',
                    'your new password':new_password
                }
            )), 201
       return make_response(jsonify(
            {'message':'Wrong email'}
        )), 401