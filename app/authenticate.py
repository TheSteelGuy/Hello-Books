#app/authenticate.py
#coding:utf-8

#third party imports
from flask import jsonify,make_response,request
from functools import wraps
#local imports
from app.models import User
"""
controls access to various methods of the views which are decorated
by the function.
"""

def token_required(func):
    '''decorator method for authentication with tokens'''
    @wraps(func)
    def decorator(*args, **kwargs):
        auth_token = request.headers.get('Authorization') 
        if auth_token:
            kwargs['user_id'] = User.decode_token(auth_token)
            if not isinstance(kwargs['user_id'],int):
                message = kwargs['user_id']
                response = {'message':message}
                return make_response(jsonify(response)), 401 
        else:
            response = {'message':'invalid token, please login.'}
            return make_response(jsonify(response)), 401
        return func(*args, **kwargs)
    return decorator 
            

