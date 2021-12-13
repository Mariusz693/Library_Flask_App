from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

books_categories = db.Table(
    'books_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
    db.Column('category_id', db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
)


class Books_Clients(db.Model):
    __tablename__ = 'books_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    client_id = db.Column(db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    book = db.relationship('Book', back_populates='clients')
    client = db.relationship('Client', back_populates='books')
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return '<id {} - book_client>'.format(self.id)


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
    categories = db.relationship('Category', secondary=books_categories, back_populates='books')
    clients = db.relationship('Books_Clients', back_populates='book', cascade='all, delete')

    def __repr__(self):
        return '<id {} - book>'.format(self.id)

    def __str__(self):
        return self.title


class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', back_populates='author', cascade='all, delete')

    def __repr__(self):
        return '<id {} - author>'.format(self.id)

    def __str__(self):
        return self.name


class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(9), nullable=True)
    books = db.relationship('Books_Clients', back_populates='client', cascade='all, delete')

    def __repr__(self):
        return '<id {} - client>'.format(self.id)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    books = db.relationship('Book', secondary=books_categories, back_populates='categories')

    def __repr__(self):
        return '<id {} - category>'.format(self.id)

    def __str__(self):
        return self.name
