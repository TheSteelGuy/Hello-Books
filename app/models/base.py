#app/user.py
#coding:"utf-8"

class Base(object):
    """parent class for common methods"""
    def __init__(self):
        """constructor which prepares structures to store data about the app"""
        self.users_list = list()
        self.books_list = list()
        self.books_category_list = []
        self.borrowed_books = []
        self.copies = 0
 
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
  