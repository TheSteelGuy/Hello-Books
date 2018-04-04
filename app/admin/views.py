#app/admin/views.py

from flask import make_response, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
import re
#local imports
from app import user, admin_user
from . import admin


@admin.route('/auth/api/v1/admin/login', methods=['POST'])
def login():
    """logs the admin in"""
    if request.method == 'POST':
       username = request.json.get('username')
       password = request.json.get('password')
       response = admin_user.login(username, password)
       if response == "succsefully logged in":
           access_token = create_access_token(identity=password)
           return make_response(jsonify(
               {
                   'message':'welcome admin',
                   'token': access_token
               }
           )), 200
       else:
           return make_response(jsonify(
               {'message':response}
           )), 403


@admin.route('/api/v1/books', methods=['POST'])
@jwt_required
def add_book():
    """endpoint allows user to add a new book information"""
    if request.method == 'POST':
        author = request.json.get('author')
        title = request.json.get('title')
        publisher = request.json.get('publisher')
        edition = request.json.get('edition')
        category = request.json.get('category')
        response = admin_user.add_book(author, title, publisher, edition, category)
        if len(author) == 0 or len(title) == 0 or len(publisher) == 0 or len(edition) == 0 or len(category) == 0:
           return make_response(jsonify(
               {'message':'no empty inputs allowed'}
           )), 409
        if author.isdigit() or title.isdigit() or publisher.isdigit() or category.isdigit():
           return make_response(jsonify(
               {'message':'book details must be alphabet'}
           )), 409   
        if not re.findall(r'(^[A-Za-z]+\s[A-Za-z]+$)', author):
           return make_response(jsonify(
               {'message':'author must be in form of Evalyn James'}
           )), 409  
        
        if response == "book with similar details exists":
            return make_response(jsonify(
                {'message':response}
            )), 409
        if response == "book created":
           return make_response(jsonify(
               {
                   'author':author,
                   'title':title,
                   'publisher':publisher,
                   'edition':edition,
                   'category':category
               }
           )), 201


@admin.route('/api/v1/books/<book_id>', methods=['PUT'])
@jwt_required
def modify_book(book_id):
    '''modifys book information'''
    if request.method == 'PUT':
       author = request.json.get('new_author')
       title = request.json.get('new_title')
       publisher = request.json.get('new_publisher')
       edition = request.json.get('new_edition')
       category = request.json.get('new_category')
       if len(title) == 0 or len(publisher) == 0 or len(edition) == 0 or len(category) == 0:
          return make_response(jsonify(
              {'message':'no empty inputs allowed'}
          )), 409
       if author.isdigit() or title.isdigit() or publisher.isdigit() or category.isdigit():
          return make_response(jsonify(
              {'message':'book details must be alphabet'}
          )), 409   
       if not re.findall(r'(^[A-Za-z]+\s[A-Za-z]+$)', author):
          return make_response(jsonify(
              {'message':'author must be in form of Evalyn James'}
          )), 409 
       response = admin_user.modify_book_details(author, title, publisher, edition, category, str(book_id))
       if response == "book details updated":
           return make_response(jsonify(
               {'message':response}
           )), 201
       return make_response(jsonify(
           {'message':response}
       )), 400


@admin.route('/api/v1/books/<book_id>', methods=['DELETE'])
@jwt_required
def delete_book(book_id):
    """allows the admin to delete/remove book details"""
    if request.method == 'DELETE':
        response = admin_user.delete_book_details(str(book_id))
        if response == "book deleted":
            return make_response(jsonify(
                {'message':response}
            )), 204

        
@admin.route('/api/v1/auth/logout')
@jwt_required
def logout():
    if request.method == 'GET':
        return make_response(jsonify(
            {'message':'successfully logged out'}
        )), 200


@admin.route('/api/auth/reset',methods=['POST'])
def reset_default_password():
    """
    allowes admin to reset the default credentials
    from username :admin and password:admin12
    """
    if request.method == 'POST':
       username = request.json.get('username')
       new_username = request.json.get('new_username')
       password = request.json.get('password')
       new_pwd = request.json.get('new_password')
       email = request.json.get('admin_email')
       if len(new_username) < 4 or len(new_pwd) < 4:
            return make_response(jsonify(
                {'message':'new username or password cannot be empty'}
            )), 409
       if not re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):  
           return make_response(jsonify(
               {'messaage':'Invalid email'}
           )), 200                
       response = admin_user.reset_default_password(username,new_username,password,new_pwd,email)
       if response == 'admin details updated': 
           return make_response(jsonify(
               {'messaage':response}
           )), 200
       else:
            return make_response(jsonify(
                {'message':'unable to reset your credentials, check the default values and try again'}
            ))
                

