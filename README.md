[![Coverage Status](https://coveralls.io/repos/github/TheSteelGuy/Hello-Books/badge.svg?branch=master)](https://coveralls.io/github/TheSteelGuy/Hello-Books?branch=master)
[![Build Status](https://travis-ci.org/TheSteelGuy/Hello-Books.svg?branch=develop2)](https://travis-ci.org/TheSteelGuy/Hello-Books)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/963b33c3b1594047b966da05c5bb4d31)](https://www.codacy.com/app/TheSteelGuy/Hello-Books?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TheSteelGuy/Hello-Books&amp;utm_campaign=Badge_Grade)


# Hello-Books app

### Introduction
The application allows admin(s) to manage the library resources(books) efficiently.
Registered/authenticated users can borrow,return and view the books they owe the library.
Anybody can see the list of available books.


#### Getting Started


#### Usage
With the app Hello-Books:
#### Admin can:
* Add a book 
* Update book information/details
* View users who owns the library book(s)
* View all books in the library
* Remove a book from the list of available books 

#### Registered user can:
* Create an account
* Login into the account
* Logout
* Borrow books
* View books owed to the library
* Return a book


#### Setting
* First install the virtual environment globally `sudo pip instal virtualenv`
* create the virtual enviroment `virtualenv --python=python2.7 myenv`
* change directory to myenv
* activate virtual environment `source myenv/bin/activate`
* run pip install requirements.txt
* clone the repo
* change directory to the repo
* type`export FLASK_CONFIG=development` 

#### How to run flask
* Run  `python run.py`

#### Testing:
* Install nosetests `pip install nose`

* Run the tests `nosetests `
#### Flask API endpoints

| Endpoints                                       |       Functionality                  |
| ------------------------------------------------|:------------------------------------:|
| `POST /api/v1/auth/register`                    |  Creates a user account              |
| `POST /api/v1/auth/reset-password`              |  Password reset                      |
| `POST /api/v1/auth/login`                       |  login a user                        |   
| `GET  /api/v1/books/<bookId>                    |  Get a book                          |
| `GET  /api/v1/books`                            |  Retrieves all books                 |
| `PUT /api/v1/books/<bookId>`                    |  modify a book’s information         |
| `DELETE /api/v1/books/<bookId>`                 |  Remove a book                       |
| `POST  /api/v1/users/books/<bookId>`            |  Borrow book                         |
|` POST /api/v1/logout`                           |  logs out a user                      |
