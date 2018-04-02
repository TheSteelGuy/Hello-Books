#app/admin/views.py

from flask import make_response, request, jsonify
import re
#local imports
from app.models import User, Book
from app.authenticate import token_required
from . import admin

"""
@admin.route('/api/v1/books', methods=['POST'])
@token_required
def add_book():
    endpoint allows user to add a new book information
    if request.method == 'POST':
        author = request.json.get('author')
        title = request.json.get('title')
        publisher = request.json.get('publisher')
        edition = request.json.get('edition')
        category = request.json.get('category')
        copies = request.json.get('copies')
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
        if not copies.isdigit():
           return make_response(jsonify(
               {'message':'copies must be provided in digits only'} 
           )), 409
        book = Book(author, title, publisher, edition, category, copies)

        if book.check_book_exist_when_adding(author,title, edition):
            return make_response(jsonify(
                {'message':'book already in the catalog, but you can increase or decrease copies'}
            )), 409


@admin.route('/api/v1/books/<book_id>', methods=['PUT'])
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
def delete_book(book_id):
    allows the admin to delete/remove book details
    if not session.get('username'):
        return make_response(jsonify(
            {'message':'you are not logged in'}
        )), 403
    else:
        if request.method == 'DELETE':
            response = admin_user.delete_book_details(str(book_id))
            if response == "book deleted":
                return make_response(jsonify(
                    {'message':response}
                )), 200
        
@admin.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    if not session.get('username'):
        return make_response(jsonify(
            {'message':'you are not logged in'}
        )), 403
    else:
       if request.method == 'GET':
           session.pop('email')
           return make_response(jsonify(
               {'message':'successfully logged out'}
           )), 200

@admin.route('/api/auth/', methods=['POST'])
def reset_default_password():
    
    allowes admin to reset the default credentials
    from username :admin and password:admin12
    
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
            )) """
                
