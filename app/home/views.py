#app/home/views.py

from flask import make_response,request,jsonify, session
#local imports
from app import user as users,admin_user
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
        response = users.register(username,email,password,confirm_pwd)
        if response == 'username exists choose another name!':    
           return make_response(jsonify(
               {'message':'username exists choose another name!'}
           )), 400
        if response == "Email is already in use":    
           return make_response(jsonify(
               {'message':"Email is already in use"}
           )), 400
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
           return make_response(jsonify(
               {'message':response}
           )), 201

  
@home.route('/auth/api/v1/login',methods=['GET','POST'])
def login():
    """handles login requests"""
    if request.method == 'GET':
        return make_response(jsonify(
            {'message':'welcome to the login endpoint'}
        )), 200
    if request.method == 'POST':
        details = request.get_json()
        email = details.get('email')
        password = details.get('password')
        response = users.login(email,password)
        if response == "succsefully logged in":
            return make_response(jsonify(
                {'message':response}
            )), 200
        for user in users.users_list:
            if user['email'] == email:
               session['email'] = email
        if response == "Inavlid username password":
            return make_response(jsonify(
                {'message':response}
            )), 400
        if response == "you have no account, register":
            return make_response(jsonify(
                {'message':response}
            )), 400
            
@home.route('/api/v1/books')
def get_books():
    if request.method == 'GET':
        res = admin_user.books_list
        return make_response(jsonify(
            {'books':res}
        )), 200

@home.route('/api/v1/books/<book_id>',methods=['POST'])
def borrow_book(book_id):
    if request.method == 'POST':
        author = request.json.get('author')
        title = request.json.get('title')
        publisher = request.json.get('publisher')
        edition = request.json.get('edition')
        for user in users.users_list:
            if session['email'] != user['email']:
               return make_response(jsonify(
                   {'message':'you are not logged in'}
               )), 403
            response = users.borrow_book(author, title, publisher, edition, str(book_id))
            return make_response(jsonify(
                {'book borrowed':response}
            )), 200
          
