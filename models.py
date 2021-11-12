from flask_sqlalchemy import SQLAlchemy

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
    descripion = db.Column(db.Text)
    is_loaned = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
    categories = db.relationship('Category', secondary=books_categories, lazy='subquery', backref=db.backref('books', lazy=True))
    clients = db.relationship('Client', secondary=books_clients, lazy='subquery', backref=db.backref('books', lazy=True))
    
    def __init__(self, isbn, title, description, is_loaned, author_id):
        self.isbn = isbn
        self.title = title
        self.descripion = description
        self.is_loaned = is_loaned
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.title


class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', backref='book', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.name


class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __str__(self):
        return self.name