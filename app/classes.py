#app/user.py
#coding:"utf-8"

""" modules import"""
from datetime import date
import re

class Base(object):
    """parent class for common methods"""
    def __init__(self):
        """constructor which prepares structures to store data about the app"""
        self.users_list = list()
        self.books_list = list()
        self.books_category_list = []
        self.borrowed_books = []
        self.user_borrowed_books = []
    
    def filter_books_by_category(self, category):
        """filters books by category eg programming, sciences etc"""
        for book_details in self.books_list:
            if book_details['category'] == category:
                self.books_category_list.append(book_details)
                return self.books_category_list
            
            return "no books in"+" " + str(category) +" " " are available"
        return "no books by that category in the library"
    def filter_borrowed_books_by_user(self, email):
        """filters users borrowing per profile"""
        for book_details in self.borrowed_books:
            if book_details['email'] == email:
                self.user_borrowed_books.append(book_details)
                return self.user_borrowed_books
            return "email does not exist"
        return "there are no books in the library"

    def get_all_books(self):
        """ gets all books within the library"""
        for book in self.books_list:
            if len(self.books_list) != 0:
                return book
            return "books unavailable"


    def user_borrowing_history(self, email):
        """method displays user borrowin history"""
        user_borrowing_history = [
             borrowing_details for borrowing_details in self.borrowed_books if borrowing_details['email'] == email
            ]
        return user_borrowing_history

######################################### USER CLASS ###############################################################
class User(Base):
    """user class contains methods allowed for user object"""
    def __init__(self):
        """person constructor"""
        Base.__init__(self)
        self.is_admin = False

    def register(self, username, email, password, confirm_pwd):
        """ Registration"""
        registration_dict = dict()
        for user in self.users_list:
            if username == user['username']:
                return 'username exists choose another name!'
            if user['email'] == email:
                 return "Email is already in use"
        if not re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
          return "Invalid email"
    
        if len(password) < 3:
          return "password length should be more than 3 characters"
        if username.strip() == "" or not username.isalpha():
          return  "username cannot be empty, or non alphabet"
        if password != confirm_pwd:
         return "password does not match"
        else:
           registration_dict['username'] = username
           registration_dict['email']  = email
           registration_dict['password'] = password
           registration_dict['is_admin'] = self.is_admin
           self.users_list.append(registration_dict)
           return "registration succesfull"
               
    def login(self, email, password):
         """login method"""
         for user in self.users_list:
             if email == user['email']:
                if password == user['password']:
                   return "succsefully logged in"
             
                return "Inavlid username password"
         return "you have no account, register"

    
    def borrow_book(self, author, title, publisher, edition, email):
        """handles borrowing of books by registered users"""
        for user in self.users_list:
            if user['email'] == email:
                book = {
                    'author' : author,
                    'title' : title,
                    'publisher' : publisher,
                    'edition' : edition
                }
                self.borrowed_books.append(book)
                return 'book borrowed'
            return 'wrong email address'
        return 'book does not exist'

    def return_book(self, author, title, email):
        """handles returning borrowed book"""
        books_borrowed = self.filter_borrowed_books_by_user(email)
        for book_details in books_borrowed:
            if book_details['author'] == author:
                if book_details['title'] == title:
                    if book_details['edition']:
                        self.user_borrowed_books.remove(book_details)
                        return "book returned"
                    return "inconsistent edition with the book title and author"
                return "title does not match any author for any book"
            return "book does not exist"
        return "book does not exist in the category given"

############################################ ADMIN CLASS ############################################################## 

class Admin(Base):
    """
    The admin class Contains methods that manage the site
    """
    def __init__(self):
        """admin class constructor"""
        Base.__init__(self)
        self.admin_list = [{'username':'admin','password':'admin12'}]
        self.total_books = 0

    def login(self, username, password):
        """admin login method"""
        for admin_dict in self.admin_list:
            if username == admin_dict['username']:
                if password == admin_dict['password']:
                    return "succsefully logged in"
                return "Inavlid username or password for admin"
            return "you are not an admin"
    
    def change_default_password(self):
        """reset the admin credetials from default values"""
        pass

    def get_all_users(self):
        """users who have registered"""
        return self.users_list
    

    def add_book(self, author, title, publisher, edition, category):
        """ creates a book which does not exist"""
        book_dict = dict()   
        for book in self.books_list:
             if book['title'] == title and book['author'] == author:
                return "book with similar details exists"
        else:
           book_dict['author'] = author 
           book_dict['title'] = title
           book_dict['publisher'] = publisher
           book_dict['edition'] = edition
           book_dict['category'] = category
           book_dict['date_added'] = date.today().isoformat()
           self.books_list.append(book_dict)
           self.total_books += 1
           return "book created"   
    def modify_book_details(self, new_author, new_title, new_publisher, new_edition, new_category, author, title):
        """updates book details"""
        for book_dict in self.books_list:
            if book_dict['author'] == author:
                if book_dict['title'] == title:   
                   new_details=  {
                     'author' :new_author,
                     'title':new_title, 
                     'publisher' :new_publisher,
                     'edition' : new_edition,
                     'category' : new_category
                   }
                   book_dict.update(new_details)
                   return "book details updated"
                return "check spelling errors in book title"
            return "check spelling errors in  author details"
        return "book not existing, you can add it"
  
    def delete_book_details(self, author, title):
        """removes the book details given a title and author"""
        for book in self.books_list:
            if book['author'] == author:   
                if book['title'] == title:
                   self.books_list.remove(book)
                   self.total_books -= 1 
                   return "deleted"
                return "check the author details for spelling errors"
            return "book does not exist"


