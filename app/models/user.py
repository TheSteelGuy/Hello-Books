#app/user.py
#coding:"utf-8"

from base import Base
import re

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
        if len(username) == 0 or not username.isalpha():
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
             continue
         return "you have no account, register"

    
    def borrow_book(self, author, title, publisher, edition, email, book_id):
        """handles borrowing of books by registered users"""
        for book in self.books_list:
            if book['book_id'] != str(book_id):
               return 'book does not exist'
            continue
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
            if book_details['book_id'] == str(book_id):
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
    