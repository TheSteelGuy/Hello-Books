#test_app.py
#coding:utf-8

#third party imports
from flask_testing import TestCase
import unittest
#local import
from app import create_app

class TestBase(TestCase):
    """ common class"""
    def create_app(self):
         config_name = 'testing'
         self.app = create_app(config_name)
         self.client = self.app.test_client()
         return self.app
    
    def setUp(self):
        """ gets run before any test"""
        pass

    def tearDown(self):
        pass
    
class TestUser(TestBase):
    """test user class"""
    def test_register(self):
        """test if user can register"""


    def test_email_use_once(self):
        """test email uniquesness"""

    def test_unique_username(self):
        """test username uniqueness"""


    def test_valid_email(self):
        """test email valid email"""
 

    def test_password_and_confirm(self):
        """test if password and confirm are similar"""


    def test_password_length(self):
        """password length less than 3"""
    
    def test_login(self):
        """tests login"""

    def test_get_books(self):
        """test user access to all books"""

    def test_user_borrow(self):
        """test if a user can borrow a book"""

       
    def test_filter_by_email(self):
        """test books filterin with email"""

    def test_getbookby_id(self):
        'gets abook by an id'


    def test_reset_password(self):
        """tests user can rest their password"""


class TestBook(TestBase):
    """tests admin methods"""
    def test_login(self):
        """tests login"""


    def test_add_book(self):
        """test adding book"""

    
    def test_modify_book(self):
        """test moddify book"""
   

    def test_delete_book(self):
        """tests admin delete book details"""

    def test_delete_with_wrong_details(self):
        """tests delete with wrong  book id details"""

    def test_filter_by_category(self):
        """test category"""

class TestBorrow(TestBase):
    pass

        
if __name__ == '__main__':
    unittest.main()


