from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


books_categories = db.Table(
    'books_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
)


books_clients = db.Table(
    'books_clients',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
    db.Column('loan_date', db.Date, nullable=False),
    db.Column('return_date', db.Date, default=None)
)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    copies = db.Column(db.Integer, nullable=False, default=1, server_default=text('1')) 
    borrowed_copies = db.Column(db.Integer, nullable=False, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
    categories = db.relationship('Category', secondary=books_categories, lazy='subquery', backref=db.backref('books', lazy=True))
    clients = db.relationship('Client', secondary=books_clients, lazy='subquery', backref=db.backref('books', lazy=True))
    
    def __init__(self, isbn, title, description, copies, author_id):
        self.isbn = isbn
        self.title = title
        self.descripion = description
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
    books = db.relationship('Book', backref='book', lazy=True)

    def __init__(self, name, date_of_birth, date_of_death):
        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death

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
    
    def __init__(self, first_name, last_name, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return '<id {}>'.format(self.id)

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
