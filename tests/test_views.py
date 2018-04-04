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
        self.admin = admin_user.add_book('testauthor','testtitle','testpublisher','tested','testcateg')
        self.reg_details = {
            'username':'userone',
            'email':'testemail1@gmail.com',
            'password':'test1',
            'confirm_pwd':'test1'
        }
        self.admin ={
            'username':'admin',
            'password':'admin12'
        }

        self.user_ = {
            'email':'testemail1@gmail.com',
            'password':'test1'
        }

        self.book ={
            'author':'author',
            'title':'sometitle',
            'publisher':'pbpublisher',
            'edition':'testedition',
            'category':'testcateg'
        }


    def tearDown(self):
        user.users_list = list()
        admin_user.books_list = list()
        admin_user.borrowed_books = []

    
class TestUserViews(TestBase):
    """test all views"""  
    def test_login(self):
        """ tests if a user can log in"""
        self.client.post(
            '/auth/api/v1/register',
            data = json.dumps(self.reg_details),
            content_type = 'application/json'
        )

        response = self.client.post(
            '/auth/api/v1/login',
            data = json.dumps(self.user_),
            content_type = 'application/json'
        )
        self.assertEqual(200,response.status_code)
    
    def test_get_books(self):
        """test if a user can retrieve books"""
        admin_user.add_book('col','test1','testpublisher1','tested','testcateg')
        res = self.client.get(
            '/api/v1/books'
        )
        self.assertEqual(200, res.status_code)



class TestAdminViews(TestBase):
    """tests admin views"""


    def test_add_book_no_token(self):
        """tests admin adding book"""
        response = self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book),
            content_type='application/json'
        )
        self.assertEqual(401, response.status_code)

    def test_add_book(self):
        """tests admin adding book"""
        response = self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book),
            content_type='application/json',
        )
        self.assertEqual(401, response.status_code)

    def test_modify_book(self):
        """test modifucation of book with no login"""
        admin_user.books_list[0]['book_id']
        book ={
            'author':'autho1r',
            'title':'sometitle1',
            'publisher':'pbpublishe1r',
            'edition':'testedition',
            'category':'testcateg'
        }
        response = self.client.put(
            '/api/v1/books/<book_id>',
            data = json.dumps(book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,401)
        
if __name__ == '__main__':
    unittest.main()


