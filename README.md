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


Bright Events application lets you create and manage events.

[click here to access bright events github pages][2]

#### Getting Started
To start using the Bright Event:
git clone:
`https://github.com/betsybeth/Bright_event.git`  
into your computer
* change your directory into `cd Bright_event`
#### Usage
with Bright Event you can:
* create an account
* login into the account
* create an event
* update an event
* view an event
* delete an event
* add RSVP into the event
* update RSVP card
* delete an RSVP card
* logout
#### Setting
* First install the virtual environment globally `sudo pip instal virtualenv`
* create the virtual enviroment `virtualenv --python=python3 myenv`
* activate virtual environment `source myenv/bin/activate`
* type `export FLASK_CONFIG=development`
#### How to run flask
* Run  `python run.py`

#### Testing:
* Install nosetests `pip install nose`
* Run the tests `nosetests -`
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
|` POST /api/v1/logout`                           |  logs in a user                      |

### Credits
* [Collins][1]


 




