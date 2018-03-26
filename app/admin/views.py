#app/admin/views.py

from flask import make_response, request, jsonify, session
#local imports
from app import user, admin_user
from . import admin

@admin.route('/auth/api/v1/admin/login', methods=['GET','POST'])
def login():
    """logs the admin in"""
    if request.method == 'GET':
        return make_response(jsonify(
            {'message':'only admins are allowed here'}
        )), 200
    if request.method == 'POST':
       username = request.json.get('username')
       password = request.json.get('password')
       response = admin_user.login(username, password)
       if response == "succsefully logged in":
           session['username'] = username
           return make_response(jsonify(
               {
                   'message':'welcome admin',
                   'session': session['username']
               }
           ))
       else:
           return make_response(jsonify(
               {'message':response}
           ))

@admin.route('/api/v1/books', methods=['POST'])
def add_book():
    """endpoint allows user to add a new book information"""
    if not session.get('username'):
        return make_response(jsonify(
            {'message':'you are not logged in'}
        )), 401
    else:
       if request.method == 'POST':
           author = request.json.get('author')
           title = request.json.get('title')
           publisher = request.json.get('publisher')
           edition = request.json.get('edition')
           category = request.json.get('category')
           response = admin_user.add_book(author, title, publisher, edition, category)
           if response == "book with similar details exists":
               return make_response(jsonify(
                   {'message':response}
               )), 400
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
def modify_book(book_id):
    '''modifys book information'''
    if not session.get('username'):
        return make_response(jsonify(
            {'message':'you are not an admin, keep off.'}
        )), 403
    else:
        if request.method == 'PUT':
           author = request.json.get('new_author')
           title = request.json.get('new_title')
           publisher = request.json.get('new_publisher')
           edition = request.json.get('new_edition')
           category = request.json.get('new_category')
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
    """allows the admin to delete/remove book details"""
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
                

