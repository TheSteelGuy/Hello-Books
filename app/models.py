"""
app/models.py
coding:utf-8
the model class contains the application models,
and how various entities are relating within the database such as,
relationship between user and books
"""
#third party imports
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,date,timedelta
from flask import current_app
import jwt
import re

#local imports
from . import db

class User(db.Model):
    """ handles users of the app"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    second_name = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(100),unique=True, nullable=False)
    national_id = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(200),)
    books = db.relationship(
        'Book', 
        backref='users',
        lazy='dynamic',
        order_by= 'Book.id',
        cascade='all,delete-orphan'
        )
    is_admin = db.Column(db.Boolean,nullable=False)

    def __init__(self, first_name,second_name, email, national_id, password):
         """constructor method which create the attributes of User() objects"""
         self.first_name = first_name
         self.second_name = second_name
         self.email = email
         self.national_id = national_id
         self.password_hash = generate_password_hash(password)
         self.is_admin =False

    @property
    def password(self):
         """raises attribute error if access to password is tried"""
         return AttributeError('Password is not readable, attribute')
      
    def verify_password(self,password):
         """verify password against the  password hash"""
         return check_password_hash(self.password_hash,password)

    @staticmethod
    def validate_email(email):
         """Ensure valid email"""
         return bool(re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))

    def token_generate(self,user_id):
        "method which generates token for users"
        try:
             paylod = {
                 'exp':datetime.utcnow() + timedelta(minutes=120),
                 'iat':datetime.utcnow(),
                 'sub':user_id

             }
             encoded_token = jwt.encode(
                 paylod,current_app.config['SECRET_KEY'],algorithm='HS256'
             )
             return encoded_token

        except Exception:
            return str(Exception)
    @staticmethod
    def decode_token(token_auth):
        """decodes the token"""
        try:

            paylod = jwt.decode(
                token_auth,current_app.config.get('SECRET_KEY'))
            token_blacklisted = TokenBlacklisting.verify_token(token_auth)
            if token_blacklisted:
                return "Invalid token.Please Login Again"
            return paylod['sub']
        except jwt.ExpiredSignatureError:
            return "Token Expired.Please Login Again"
        except jwt.InvalidTokenError:
            return "Invalid Token.Please Login Again"
    
    def save_user(self):
        """saves a user to the database"""
        db.session.add(self)
        db.commit()
    
    def __repr__(self):
        """string represntaion for the user class"""
        return '<user:{}>'.format(self.first_name)



class Book(db.Model):
    """class book handles book"""
    __tablename__ = 'books'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author = db.Column(db.String(60), nullable=False)
    book_title = db.Column(db.String(60), nullable=False)
    publisher = db.Column(db.String(60), nullable=False)
    edition = db.Column(db.String(100),unique=False, nullable=False)
    category = db.Column(db.String(40),unique=False, nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    borrowers = db.relationship(
        'Borrow', 
        backref='books',
        lazy='dynamic',
        order_by= 'Borrow.book_id',
        cascade='all,delete-orphan'
        )

    def __init__(self,author, book_title, publisher, edition, category, copies):
        """ book constructor method which sets book attributes"""
        self.author = author
        self.book_title = book_title
        self.publisher = publisher
        self.edition = edition
        self.category = category
        self.copies = copies

    @staticmethod
    def book_borrowers(user_id):
        """retrieves all users who have borrowed this book """
        users = Book.query.filter_by(user=user_id).all()
        return users

    @staticmethod
    def check_book_exist_when_adding(author, book_title, edition):
        """checks if a book exist"""
        book = Book.query.filter_by(author=author, book_title=book_title, edition=edition).first()
        if book:
            return True
        return False


    def change_copies(self, author, title, edition, copies):
        book = Book.query.filter_by(author=author, title=title, edition=edition).first()
        if book:
            self.copies = copies
            db.sesion.commit()
    def admin_flag(self):
        admin = User.query.filter_by(self.is_admin).first()
        if admin:
            return True
        return False

    
    def delete_book(self):
        """delete this book"""
        db.session.delete(self)
        db.session.commit()

    def book_serialize(self):
        """checks if a book exist"""
        return {
            'book_id':self.id,
            'author':self.author,
            'publisher':self.publisher,
            'edition':self.edition,
            'category': self.category
        }

    def save_book(self):
        db.session.add(self)
        db.session.commit()

class Borrow(db.Model):
    """handles users who have borrowed"""
    __tablename__ = 'borrowers'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    national_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))


    def __init__(self,book_id, email, national_id):
        """borrower constructor"""
        self.book_id = book_id
        self.email = email
        self.national_id = national_id
    
    def save_borrowed(self):
        db.session.add(self)
        db.commit()

class TokenBlacklisting(db.Model):
    """model handles blacklisting of tokens"""

    __tablename__ = "blacklisted_tokens"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    token = db.Column(db.String(400),nullable=False)
    time_of_blacklisting = db.Column(
        db.String(100),default=datetime.now(),nullable=False
    )

    def __init__(self,token):
        """
        constructor receives token and asigns time for
        blacklisting when an object is created out of this class
        """
        self.token = token
        self.time_of_blacklisting = datetime.now()

    def save_token(self):
        """saves tokens to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify_token(auth_token):
        """
        Checks if the token exist in the database, 
        that is wether it is blacklisted or not.
        """
        blacklisted_token = TokenBlacklisting.query.filter_by(
            token=str(auth_token)).first()
        if blacklisted_token:
            return True
        return False

    def serialize(self):
        """returns the blacklisted token as dictionary"""
        return{
            'token':self.token,
            'time_of_blacklisting':self.time_of_blacklisting
        }