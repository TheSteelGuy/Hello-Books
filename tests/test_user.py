#test_app.py
#coding:utf-8

#third party imports
from flask_testing import TestCase
import unittest
import json
#local import
from app import user_object as user,admin_user,create_app

class TestBase(unittest.TestCase):
    """ common class"""
    def create_app(self):
         config_name = 'testing'
         self.app = create_app(config_name)
         self.client = self.app.test_client()
         return self.app
    
    def setUp(self):
        """ gets run before any test"""
        self.user1 = user.register('testuser','testemail@gmail.com','testpass1','testpass1')
        self.admin = admin_user.add_book('testauthor','testtitle','testpublisher','tested','testcateg',10)


    def tearDown(self):
        admin_user.users_list = list()
        admin_user.books_list = list()
        admin_user.books_category_list = []
        admin_user.borrowed_books = []
        admin_user.user_borrowed_books = []


    
class TestUser(TestBase):
    """test user class"""
    def test_register(self):
        """test if user can register"""
        user2 =user.register('testusertwo','testemailtwo@gmail.com','testpass1','testpass1')
        self.assertEqual(user2,'registration succesfull')

    def test_email_use_once(self):
        """test email uniquesness"""
        user2 = user.register('testuser1','testemail@gmail.com','testpass1','testpass1')
        self.assertEqual(user2,'Email is already in use')

    def test_unique_username(self):
        """test username uniqueness"""
        user2 = user.register('testuser','testemail1@gmail.com','testpass1','testpass1')
        self.assertEqual(user2,'username exists choose another name!')

    def test_valid_email(self):
        """test email valid email"""
        user1 = user.register('testuserone','testusergmail.com','testpass1','testpass1')
        self.assertTrue(user1=="Invalid email")

    def test_password_and_confirm(self):
        """test if password and confirm are similar"""
        user1 = user.register('testuserone','testuser@gmail.com','testpass','testpass1')
        self.assertEqual(user1,'password does not match')

    def test_password_length(self):
        """password length less than 3"""
        user1 = user.register('testuserone','testuser@gmail.com','t2','t2')
        self.assertEqual(user1,'password length should be more than 3 characters')

    def test_login(self):
        """tests login"""
        user1 = user.login('testemail@gmail.com','testpass1')
        self.assertEqual(user1,'succsefully logged in')
    
    def test_get_books(self):
        """test user access to all books"""
        books = admin_user.get_all_books()
        self.assertEqual(len(books),8)
        
    def test_user_borrow(self):
        """test if a user can borrow a book"""
        borrow = user.borrow_book('testauthor','testtitle','testpublisher','tested')
        self.assertEqual(len(borrow), 5)
        
    def test_getbookby_id(self):
        'gets abook by an id'
        book_id = admin_user.books_list[0]['book_id']  
        book = admin_user.book_by_id(book_id)
        self.assertIn('category',book) 

class TestAdmin(TestBase):
    """tests admin methods"""
    def test_login(self):
        """tests login"""
        Admin = admin_user.login('admin','admin12')
        self.assertEqual(Admin,'succsefully logged in')

    def test_add_book(self):
        """test adding book"""
        self.assertEqual(self.admin,'book created')
        self.assertIn('author',admin_user.books_list[0])
    
    def test_modify_book(self):
        """test moddify book"""
        book_id = admin_user.books_list[0]['book_id']
        admin_user.modify_book_details('new_name','new_title','new_publisher','new_edition','new_categ', book_id)
        self.assertTrue('new_name'== admin_user.books_list[0]['author'])

    def test_delete_book(self):
        """tests admin delete book details"""
        admin_user.add_book('testauthor2','testtitle2','testpublisher2','tested2','testcateg2',10)
        book_id = admin_user.books_list[0]['book_id']
        delete = admin_user.delete_book_details(book_id)
        self.assertEqual(delete,True)
        self.assertFalse(len(admin_user.books_list)==2)

    def test_delete_with_wrong_details(self):
        """tests delete with wrong  book id details"""
        book_id = "nvjkbvksbhckvbhc"
        delete = admin_user.delete_book_details(book_id)
        self.assertEqual(delete,'book does not exist')

    def test_reset_admin_defaults(self):
        new_det = admin_user.reset_default_password('admin','new_username','admin12','new_pwd','collins0chieng.com')
        self.assertEqual(new_det,'admin details updated')

    def test_get_user(self):
        user = admin_user.get_all_users()  
        self.assertEqual(len(user),0)      
if __name__ == '__main__':
    unittest.main()


