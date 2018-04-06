#app/user.py
#coding:"utf-8"

from .base import Base
from datetime import date
import uuid

class Administration(Base):
    """
    The admin class Contains methods that manage the site
    """
    def __init__(self):
        """admin class constructor"""
        Base.__init__(self)
        self.admin_list = [{'username':'admin','password':'admin12'}]

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
    

    def add_book(self, author, title, publisher, edition, category, copies):
        """ creates a book which does not exist"""
        book_dict = dict()   
        for book in self.books_list:
             if book['title'] == title and book['author'] == author:
                return "book with similar details exists"
             continue
        else:
           book_dict['author'] = author 
           book_dict['title'] = title
           book_dict['publisher'] = publisher
           book_dict['edition'] = edition
           book_dict['category'] = category
           book_dict['copies'] = copies
           book_dict['book_id'] = str(uuid.uuid4())
           book_dict['date_added'] = date.today().isoformat()
           self.books_list.append(book_dict)
           self.copies += 1
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
            continue
        return "book not existing, you can add it"
  
    def delete_book_details(self, book_id):
        """removes the book details given a title and author"""
        for book in self.books_list:
            if book['book_id'] == str(book_id):   
                self.books_list.remove(book)
                self.copies -= 1 
                return True
            continue
        return "book does not exist"

    def book_by_id(self,book_id):
        """ gets a abook when passed an id of that book"""
        for book in self.books_list:
            if book['book_id'] == str(book_id):
                return book
            continue
        return "book id provided does not match any book" 
        
    
