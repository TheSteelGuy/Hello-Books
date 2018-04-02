#test_app.py
#coding:utf-8

#third party imports
from flask_testing import TestCase
import unittest
import json
#local import
from app import user,admin_user,create_app

class TestBase(TestCase):
    """ common class"""
    def create_app(self):
         config_name = 'testing'
         self.app = create_app(config_name)
         self.client = self.app.test_client()
         return self.app
    
    def setUp(self):
        """ gets run before any test"""
        self.book = {
            'author':'testauthor',
            'title':'testtitle',
            'publisher':'testpublisher',
            'edition':'tested',
            'category':'testcateg'}
        self.user_ = {
            'username':'testuserone',
            'email':'testemail1@gmail.com',
            'password':'test1',
            'confirm_pwd':'test1'
        }

    def tearDown(self):
        user.users_list = list()
        admin_user.books_list = list()
        admin_user.books_category_list = []
        admin_user.borrowed_books = []
        admin_user.user_borrowed_books = []


    
class TestHomeViews(TestBase):
    """test all views"""
    def test_register(self):
        """test user registration endpoint"""
        response = self.client.post(
            '/auth/api/v1/register',
            data = json.dumps(self.user_),
            content_type = 'application/json'
        )

        self.assertIn("registration succesfull",response.data)
    
    
    def test_login(self):
        """ tests if a user can log in"""
        self.client.post(
            '/auth/api/v1/register',
            data = json.dumps(self.user_),
            content_type = 'application/json'
        )
        user1 = {
            'email':'testemail1@gmail.com',
            'password':'test1'
        }
        response = self.client.post(
            '/auth/api/v1/login',
            data = json.dumps(user1),
            content_type = 'application/json'
        )
        self.assertIn('succsefully logged in',response.data)
    
    def test_get_books(self):
        """test if a user can retrieve books"""
        admin_user.add_book('col','test1','testpublisher1','tested','testcateg')
        res = self.client.get(
            '/api/v1/books'
        )
        self.assertEqual(200, res.status_code)

    def test_add_book(self):
        """tests if admin can add book with no logging in"""
        response = self.client.post(
            '/api/v1/users/books',
            data = json.dumps(self.book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,403)
    
    def test_borrow(self):
        """tests if a user can borrow book without authentication"""
        admin_user.add_book('col','test1','testpublisher1','tested','testcateg')
        book_id = admin_user.books_list[0]['book_id']
        book = {
            'author':'col',
            'title':'test1',
            'publisher':'testpublisher1',
            'edition':'tested',
            'category':'testcateg'}
        response = self.client.post(
            '/api/v1/users/books/<book_id>',
            data = json.dumps(book),
            content_type='application/json')

        self.assertEqual(response.status_code,403)

    def test_return_book(self):
        """tests returing of book with no login"""
        admin_user.add_book('col','test1','testpublisher1','tested','testcateg')
        book_id = admin_user.books_list[0]['book_id']
        user.borrow_book('col','test1','testpublisher1','tested','testcateg',book_id)
        response = self.client.post(
            '/api/v1/users/books/<book_id>',
            data = json.dumps(book_id),
            content_type='application/json')
        self.assertEqual(response.status_code,403)
        
if __name__ == '__main__':
    unittest.main()


