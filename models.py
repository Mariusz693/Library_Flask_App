from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Table, Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()


books_categories = db.Table(
    'books_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
)


# books_clients = db.Table(
#     'books_clients',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
#     db.Column('client_id', db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
#     db.Column('loan_date', db.Date, nullable=False),
#     db.Column('return_date', db.Date, nullable=True)
# )


class Books_Clients(db.Model):
    __tablename__ = 'books_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    client_id = db.Column(db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    book = db.relationship('Book', back_populates='clients')
    client = db.relationship('Client', back_populates='books')
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    def __init__(self, book_id, client_id, loan_date):
        self.book_id = book_id
        self.client_id = client_id
        self.loan_date = loan_date
    
    def __repr__(self):
        return '<id {}, {}>'.format(self.id, self.loan_date)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    copies = db.Column(db.Integer, nullable=False) 
    borrowed_copies = db.Column(db.Integer, nullable=False, default=u'0', server_default=u'0')
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
    author = db.relationship('Author', back_populates='books')
    categories = db.relationship('Category', secondary=books_categories, lazy='subquery', backref=db.backref('books', lazy=True))
    # clients = db.relationship('Client', secondary='books_clients', lazy='subquery', backref=db.backref('books', lazy=True))
    clients = db.relationship('Books_Clients', back_populates='book')

    def __init__(self, isbn, title, description, copies, author_id):
        self.isbn = isbn
        self.title = title
        self.description = description
        self.copies = copies
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.title


class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', back_populates='author')

    # books = db.relationship('Book', lazy='joined', backref=db.backref('author', lazy='joined'))


    # def __init__(self, name):
    #     self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.name


class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(9), nullable=True)
    books = db.relationship('Books_Clients', back_populates='client')

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<id {} client>'.format(self.id)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.name



# books_categories = db.Table(
#     'books_categories',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
#     db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
# )


# # books_clients = db.Table(
# #     'books_clients',
# #     db.Column('id', db.Integer, primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
# #     db.Column('client_id', db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
# #     db.Column('loan_date', db.Date, nullable=False),
# #     db.Column('return_date', db.Date, nullable=True)
# # )


# class Books_Clients(db.Model):
#     __tablename__ = 'books_clients'
    
#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
#     client_id = db.Column(db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
#     book = db.relationship('Book', back_populates='clients')
#     client = db.relationship('Client', back_populates='books')
#     loan_date = db.Column(db.Date, nullable=False)
#     return_date = db.Column(db.Date, nullable=True)

#     def __init__(self, book_id, client_id, loan_date):
#         self.book_id = book_id
#         self.client_id = client_id
#         self.loan_date = loan_date
    
#     def __repr__(self):
#         return '<id {}, {}>'.format(self.id, self.loan_date)


# class Book(db.Model):
#     __tablename__ = 'books'

#     id = db.Column(db.Integer, primary_key=True)
#     isbn = db.Column(db.String(13), unique=True, nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     copies = db.Column(db.Integer, nullable=False) 
#     borrowed_copies = db.Column(db.Integer, nullable=False, default=u'0', server_default=u'0')
#     author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
#     author = db.relationship('Author', back_populates='books')
#     categories = db.relationship('Category', secondary=books_categories, lazy='subquery', backref=db.backref('books', lazy=True))
#     # clients = db.relationship('Client', secondary='books_clients', lazy='subquery', backref=db.backref('books', lazy=True))
#     clients = db.relationship('Books_Clients', back_populates='book')

#     def __init__(self, isbn, title, description, copies, author_id):
#         self.isbn = isbn
#         self.title = title
#         self.description = description
#         self.copies = copies
#         self.author_id = author_id

#     def __repr__(self):
#         return '<id {}>'.format(self.id)

#     def __str__(self):
#         return self.title


# class Author(db.Model):

#     __tablename__ = 'authors'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True, nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=True)
#     date_of_death = db.Column(db.Date, nullable=True)
#     books = db.relationship('Book', back_populates='author')

#     # books = db.relationship('Book', lazy='joined', backref=db.backref('author', lazy='joined'))


#     # def __init__(self, name):
#     #     self.name = name

#     def __repr__(self):
#         return '<id {}>'.format(self.id)

#     def __str__(self):
#         return self.name


# class Client(db.Model):

#     __tablename__ = 'clients'

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     phone_number = db.Column(db.String(9), nullable=True)
#     books = db.relationship('Books_Clients', back_populates='client')

#     def __init__(self, first_name, last_name, email):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email

#     def __repr__(self):
#         return '<id {} client>'.format(self.id)

#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)


# class Category(db.Model):

#     __tablename__ = 'categories'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True, nullable=False)
    
#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return '<id {}>'.format(self.id)

#     def __str__(self):
#         return self.name