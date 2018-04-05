#app/home/views.py

from flask import make_response,request,jsonify
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
import re
#local imports
from app import user_object as users,admin_user
from . import user


@user.route('/')
def homepage():
    """get requests for homepage"""
    return make_response(jsonify(
        {
        'message':'welcome to the hello-books app you can register in order to get the most out of the app'
        }
    )), 200


@user.route('/auth/api/v1/register',methods=['POST'])
def register():
    """method to handle register requests"""
    if request.method == 'POST':
       details = request.get_json()
       username = details.get('username')
       email = details.get('email')
       password = details.get('password')
       confirm_pwd = details.get('confirm_pwd')
       response = users.register(username,email,password,confirm_pwd)
       if response == 'username exists choose another name!':    
          return make_response(jsonify(
              {'message':'username exists choose another name!'}
          )), 409
       if response == "Email is already in use":    
          return make_response(jsonify(
              {'message':"Email is already in use"}
          )), 409
       if response == "Invalid email":    
          return make_response(jsonify(
              {'message':response}
          )), 400
       if response == "password length should be more than 3 characters":    
          return make_response(jsonify(
              {'message':response}
          )), 400
       if response == "username cannot be empty, or non alphabet":    
          return make_response(jsonify(
              {'message':response}
          )), 400
       if response == "password does not match":    
          return make_response(jsonify(
              {'message':response}
          )), 400
       if response == "registration succesfull": 
          access_token = create_access_token(identity=email)  
          return make_response(jsonify(
              {
                  'message':response,
                  'token': access_token
              }
          )), 201
    
@user.route('/auth/api/v1/login',methods=['POST'])
def login():
    """handles login requests"""
    if request.method == 'POST':
        details = request.get_json()
        email = details.get('email')
        password = details.get('password')
        response = users.login(email,password)
        if response == "succsefully logged in":
            access_token = create_access_token(identity=email)            
            return make_response(jsonify(
                {
                    'message':response,
                    'token':access_token
                }
            )), 200
        if response == "Inavlid username password":
            return make_response(jsonify(
                {'message':response}
            )), 401
        if response == "you have no account, register":
            return make_response(jsonify(
                {'message':response}
            )), 404
            
@user.route('/api/v1/books')
def get_books():
    if request.method == 'GET':
        res = admin_user.books_list
        if len(res) == 0:
           return make_response(jsonify(
               {'message':'no books to show'}
           )), 200
            
        return make_response(jsonify(
            {'books':res}
        )), 200

@user.route('/api/v1/users/books/<book_id>',methods=['POST'])
@jwt_required
def borrow_book(book_id):
    """ borrow book"""
    if request.method == 'POST':
        author = request.json.get('author')
        title = request.json.get('title')
        publisher = request.json.get('publisher')
        edition = request.json.get('edition')
        if len(title) == 0 or len(publisher) == 0 or len(edition) == 0:
           return make_response(jsonify(
               {'message':'no empty inputs allowed'}
           )), 409
        if author.isdigit() or title.isdigit() or publisher.isdigit():
           return make_response(jsonify(
               {'message':'book details must be alphabet'}
           )), 409   
        if not re.findall(r'(^[A-Za-z]+\s[A-Za-z]+$)', author):
           return make_response(jsonify(
               {'message':'author must be in form of Evalyn James'}
           )), 409  
           
        response = users.borrow_book(author, title, publisher, edition)
        return make_response(jsonify(
            {'book borrowed':response}
        )), 200

'''@user.route('/api/v1/users/<book_id>', methods=['POST'])
def return_book(book_id):
    """Allow a user to return a book borrowed"""
    if request.method == 'POST':
        response = users.return_book(str(book_id))
        if response == "book returned":
            return make_response(jsonify(
                {'message':response}
            )), 200
        else:
            return make_response(jsonify(
                {'message':response}
            )), 404'''

            
@user.route('/api/v1/books/<book_id>')
def retrieve_book_by_id(book_id):
    """retrieves a book based on passed id"""
    if request.method == 'GET':
        response = admin_user.book_by_id(book_id)
        return make_response(jsonify(
            {'message':response}
        )), 200

'''@user.route('/api/v1/user/history')
def show_my_borrowing(self):
    """ shows a user borrowing history"""
    if not session.get('email'):
        return make_response(jsonify(
            {'message':'you are not logged in'}
        )), 403
    else:
        email = session['email']
        response = users.user_borrowing_history(email)
        if len(response) == 0:
            return make_response(jsonify(
                {'message':'no history to show'}
            )), 200
        else:
            return make_response(jsonify(
                {'borrowed books':response}
            )), 200 '''

@user.route('/api/auth/logout')
@jwt_required
def logout():
        return make_response(jsonify(
            {'message':'successfully logged out'}
        )), 200
    
@user.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """allowes user to reset password"""
    if request.method == 'POST':
       email = request.json.get('email')
       new_password = request.json.get('new_password')
       if not email or new_password:
           return make_response(jsonify(
               {'message':'you need to pass all data in json format'}
           )), 400
       else:
           response = users.reset_password(email,new_password)
           if response == 'password reset was succesfull':
              return make_response(jsonify(
                  {'messaage':response}
              )), 200
        

