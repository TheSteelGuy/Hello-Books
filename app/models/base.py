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
  