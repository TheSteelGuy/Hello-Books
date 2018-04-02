#app/home/views.py

from flask import make_response,request,jsonify, session
import re
#local imports
from app.models import Book, User
from app.authenticate import token_required
from . import home


@home.route('/')
def index():
    if request.method == 'GET':
       """get requests for homepage"""
       return make_response(jsonify(
           {
           'message':'welcome to the hello-books app you can register in order to get the most out of the app'
           }
       )), 200

            
@home.route('/api/v1/books')
def get_books():
    if request.method == 'GET':
        try:
            limit = int(request.args.get('limit', default=15,type=int))    
            page = int(request.args.get('page', default=1,type=int))    
        except TypeError:
            return make_response(jsonify(
                {'message':'please ensure page and limit of boos to be displayed are integers eg 5'}
            )), 400
        books = Book.query.all().paginate(int(page),int(limit), False)
        next_page = ''
        prev_page = ''
        pages = books.pages
        if books.has_prev:
            prev_page = '/books/?limit={}&page={}'.format(limit, books.prev_num)
        if books.has_next:
           next_page = '/books/?limit={}&page={}'.format(limit, books.next_num)
        book_list = [book.book_serialize() for book in books.items]
        if len(book_list)  == 0:
            return make_response(jsonify(
                {'message':'no books available'}
            )), 200
        return  make_response(jsonify(
            book_list=book_list,
            prev_page=prev_page,
            next_page=next_page,
            pages=pages
        )), 200
  
@home.route('/api/v1/users/books/<book_id>',methods=['POST'])
@token_required
def borrow_book(book_id):
    if request.method == 'POST':
       book = Book.query.filter_by(id=book_id).first()
       if book:
          return make_response(jsonify(
               {
                   'message':'success',
                   
                }
          )), 200


@home.route('/api/v1/users/<book_id>', methods=['POST'])
def return_book(book_id):
    """Allow a user to return a book borrowed"""


@home.route('/api/v1/books/<book_id>')
def retrieve_book_by_id(book_id):
    """retrieves a book based on passed id"""
    if request.method == 'GET':
        book = Book.filter_by(id=book_id).first()
        if book is None:
            return make_response(jsonify(
                {'message':'book requested is not available'}
            )), 404
        return make_response(jsonify(
            {
                'id':book.id,
                'author':book.author,
                'title':book.title,
                'publisher':book.publisher,
                'edition':book.edition
            }
        )), 200
