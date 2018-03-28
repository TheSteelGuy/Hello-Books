#app/user.py
#coding:"utf-8"

""" modules import"""
from datetime import date
import re
import uuid

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
            continue
        return "no books by that category in the library"

    def filter_borrowed_books_by_user(self, email):
        """filters users borrowing per profile"""
        for borrow_details in self.borrowed_books:
            if borrow_details['email'] == email:
               self.user_borrowed_books.append(borrow_details)
               return "filtered"
            continue 
        return "you have not borrowed any book"  
 
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

    
    def borrow_book(self, author, title, publisher, edition, email, book_id):
        """handles borrowing of books by registered users"""
        for book in self.books_list:
            if book['book_id'] != str(book_id):
               return 'book does not exist'
        else: 
                book = {
                    'author' : author,
                    'title' : title,
                    'publisher' : publisher,
                    'edition' : edition,
                    'email'   : email
                }
                self.borrowed_books.append(book)
                return book
        

    def return_book(self, email, book_id):
        """handles returning borrowed book"""
        books_borrowed = self.filter_borrowed_books_by_user(email)
        for book_details in books_borrowed:
            if book_details['booK_id'] == str(book_id):
                self.user_borrowed_books.remove(book_details)
                return "book returned"
            continue
        return "book does not exist"
    def reset_password(self, email,new_password):
        """resets user password, if forgoten, 
           user has to provide valid email
        """
        for user in self.users_list:
            if user['email'] == email:
                user['password'] = new_password
                return 'password reset was succesfull'
            continue
        return "email provided does not match any user"
        
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
    
    def reset_default_password(self,username,new_username,password,new_pwd,email):
        """reset the admin credetials from default values"""
        for admin_dict in self.admin_list:
            if admin_dict['username'] != username:
                return "wrong username"
            if admin_dict['password'] != password:
                return 'wrong password'
            else:
                new_details ={
                    'username':new_username,
                    'password':new_pwd,
                    'email':email
                }
                del self.admin_list[0]
                self.admin_list.append(new_details)
                return 'admin details updated'

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
           book_dict['book_id'] = str(uuid.uuid4())
           book_dict['date_added'] = date.today().isoformat()
           self.books_list.append(book_dict)
           self.total_books += 1
           return "book created" 

    def modify_book_details(self, new_author, new_title, new_publisher, new_edition, new_category, book_id):
        """updates book details"""
        for book_dict in self.books_list:
            if book_dict['book_id'] == str(book_id): 
                   new_details=  {
                     'author' :new_author,
                     'title':new_title, 
                     'publisher' :new_publisher,
                     'edition' : new_edition,
                     'category' : new_category
                   }
                   book_dict.update(new_details)
                   return "book details updated"
            return "book not existing, you can add it"
  
    def delete_book_details(self, book_id):
        """removes the book details given a title and author"""
        for book in self.books_list:
            if book['book_id'] == book_id:   
                   self.books_list.remove(book)
                   self.total_books -= 1 
                   return "book deleted"
            continue
        return "book does not exist"

    def book_by_id(self,book_id):
        """ gets a abook when passed an id of that book"""
        for book in self.books_list:
            if book['book_id'] == str(book_id):
                return book
            continue
        return "email provided does not match any user"


