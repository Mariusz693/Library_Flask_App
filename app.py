from operator import le
import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db
from sqlalchemy.exc import IntegrityError
# from flask_wtf import CSRFProtect, csrf
from validators import validate_phone, validate_email, validate_isbn

load_dotenv()

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# csrf = CSRFProtect(app)

from models import Book, Client, Category, Author


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/books/")
def books():
    books_list = Book.query.all()
    return render_template('books.html', books_list=books_list)


@app.route("/authors/")
def authors():
    authors_list = Author.query.all()
    return render_template('authors.html', authors_list=authors_list)


@app.route("/clients/")
def clients():
    clients_list = Client.query.all()
    return render_template('clients.html', clients_list=clients_list)


@app.route("/add_author/", methods=['GET', 'POST'])
def add_author():
    message = 'Dodaj wpis nowego autora'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth')
        date_of_death = request.form.get('date_of_death')
        if len(name) > 2:
            new_author = Author(name)
            if date_of_birth:
                new_author.date_of_birth = date_of_birth
            if date_of_death:
                new_author.date_of_death = date_of_death
            try:
                db.session.add(new_author)
                db.session.commit()
                message = f'Dodano wpis nowego autora "{name}"'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis "{name}" już istnieje w bazie danych'
        else:
            message = 'Wpis autora zbyt krótki - nie dodano'    
            
    return render_template(
        'add_author.html',
        message=message
        )


@app.route("/edit_author/<int:id_author>/", methods=['GET', 'POST'])
def edit_author(id_author):
    author = Author.query.get_or_404(id_author)
    message = f'Zmień wpis autora - {author.name}'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth')
        date_of_death = request.form.get('date_of_death')
        if len(name) > 3:
            author.name = name
            author.date_of_birth = date_of_birth if date_of_birth else None
            author.date_of_death = date_of_death if date_of_death else None
            try:
                db.session.commit()
                message = f'Zmieniono wpis autora "{name}"'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis "{name}" już istnieje w bazie danych'
        else:
            message = 'Wpis autora zbyt krótki - nie zmieniono'    
            
    return render_template(
        'edit_author.html',
        message=message,
        author=author
        )


@app.route("/delete_author/<int:id_author>/", methods=['GET', 'POST'])
def delete_author(id_author):
    author = Author.query.get_or_404(id_author)
    message = 'Potwierdź usunięcie profilu autora'
    if request.method == 'POST':
        try:
            db.session.delete(author)
            db.session.commit()

            return redirect('/authors/')
        
        except IntegrityError:
            db.session.rollback()
            message = f'Błąd w usuwaniu profilu'
        
    return render_template(
        'delete_author.html',
        message=message,
        author=author
        )


@app.route("/details_author/<int:id_author>/")
def details_author(id_author):
    author = Author.query.get_or_404(id_author)

    return render_template(
        'details_author.html',
        author=author
        )


@app.route("/add_client/", methods=['GET', 'POST'])
def add_client():
    message = 'Dodaj wpis nowego clienta'
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        if first_name and last_name:
            if phone_number == '' or validate_phone(phone_number):
                if email and validate_email(email):
                    new_client = Client(first_name, last_name, email)
                    if phone_number:
                        new_client.phone_number = phone_number
                    try:
                        db.session.add(new_client)
                        db.session.commit()
                        message = f'Dodano wpis nowego klinta "{new_client}"'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis email "{email}" już istnieje w bazie'
                else:
                    message = 'Brak adresu email lub źle podany'
            else:
                message = 'Numer telefonu źle podany'
        else:
            message = 'Brak imienia lub nawiska klienta'    
            
    return render_template(
        'add_client.html',
        message=message
        )


@app.route("/edit_client/<int:id_client>/", methods=['GET', 'POST'])
def edit_client(id_client):
    client = Client.query.get_or_404(id_client)
    message = f'Zmień wpis clienta - {client}'
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        if first_name and last_name:
            if phone_number == '' or validate_phone(phone_number):
                if email and validate_email(email):
                    client.first_name = first_name
                    client.last_name = last_name
                    client.email = email
                    if phone_number:
                        client.phone_number = phone_number
                    try:
                        db.session.commit()
                        message = f'Zmieniono wpis klinta "{client}"'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis email "{email}" już istnieje w bazie'
                else:
                    message = 'Brak adresu email lub źle podany'
            else:
                message = 'Numer telefonu źle podany'
        else:
            message = 'Brak imienia lub nawiska klienta'    
        
    return render_template(
        'edit_client.html',
        message=message,
        client=client
        )


@app.route("/delete_client/<int:id_client>/", methods=['GET', 'POST'])
def delete_client(id_client):
    client = Client.query.get_or_404(id_client)
    message = 'Potwierdź usunięcie profilu clienta'
    if request.method == 'POST':
        try:
            db.session.delete(client)
            db.session.commit()

            return redirect('/clients/')
        
        except IntegrityError:
            db.session.rollback()
            message = 'Błąd w usuwaniu profilu'
        
    return render_template(
        'delete_client.html',
        message=message,
        client=client
        )
        

@app.route("/details_client/<int:id_client>/")
def details_client(id_client):
    client = Client.query.get_or_404(id_client)
    print(client.books)

    return render_template(
        'details_client.html',
        client=client
        )


@app.route("/categories/", methods=['GET', 'POST'])
def categories():
    categories = Category.query.all()
    message = 'Kategorie książek'
    if request.method == 'POST':
        delete_category = request.form.get('delete_category')
        name = request.form.get('name')
        if delete_category:
            category = Category.query.get_or_404(delete_category)
            category_name = category.name
            try:
                db.session.delete(category)
                db.session.commit()
                message = f'Usunięto kategorię - "{category_name}"'
                categories = Category.query.all()

            except IntegrityError:
                db.session.rollback()
                message = f'Ups... coś poszło nie tak, nie usunięto kategorię "{category_name}"'

        elif len(name) > 2:
            new_category = Category(name)
            try:
                db.session.add(new_category)
                db.session.commit()
                message = f'Dodano wpis nowej kategorii "{new_category}"'
                categories = Category.query.all()
    
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis "{name}" już istnieje w bazie danych'

    return render_template(
        'categories.html',
        categories=categories,
        message=message
        )


@app.route("/add_book/", methods=['GET', 'POST'])
def add_book():
    message = 'Dodaj wpis nowej książki'
    authors_list = Author.query.all()
    categories_list = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        description = request.form.get('description')
        author = request.form.get('author')
        categories = request.form.getlist('categories')
        new_category = request.form.get('new_category')
        copies = request.form.get('copies')
        if len(title) > 2:
            if validate_isbn(isbn):
                if author == '':
                    name = request.form.get('author_name')
                    date_of_birth = request.form.get('author_date_of_birth')
                    date_of_death = request.form.get('author_date_of_death')
                    if len(name) > 2:
                        new_author = Author(name)
                        if date_of_birth:
                            new_author.date_of_birth = date_of_birth
                        if date_of_death:
                            new_author.date_of_death = date_of_death
                        try:
                            db.session.add(new_author)
                            db.session.commit()
                            author = new_author.id
                        except IntegrityError:
                            db.session.rollback()
                            message = f'Wpis autora "{name}" już istnieje w bazie danych, wybierz z listy autorów - uzupełnij ponownie'
                            return render_template(
                                'add_book.html',
                                message=message,
                                authors_list=authors_list,
                                categories_list=categories_list
                                )
                    else:
                        if name == '':
                            message = 'Wybierz autora z listy lub wpisz nową pozycję - uzupełnij ponownie'
                        else:
                            message = 'Wpis nowego autora zbyt krótki - uzupełnij ponownie'    
                        return render_template(
                            'add_book.html',
                            message=message,
                            authors_list=authors_list,
                            categories_list=categories_list
                            )
                if len(new_category) > 2:
                    new_category = Category(new_category)
                    try:
                        db.session.add(new_category)
                        db.session.commit()
                        categories.append(str(new_category.id))
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis "{new_category}" już istnieje w bazie danych, wybierz z listy kategorii - uzupełnij ponownie'
                        return render_template(
                            'add_book.html',
                            message=message,
                            authors_list=authors_list,
                            categories_list=categories_list
                            )
                elif new_category:
                    message = 'Wpis nowej kategorii zbyt krótki - uzupełnij ponownie'    
                    return render_template(
                        'add_book.html',
                        message=message,
                        authors_list=authors_list,
                        categories_list=categories_list
                        )
                # author = Author.query.get(author)
                new_book = Book(isbn, title, description, copies, author)
                categories_set = Category.query.filter(Category.id.in_(categories))
                new_book.categories.extend(categories_set)
                try:
                    db.session.add(new_book)
                    db.session.commit()
                    message = f'Dodano wpis nowej książki "{new_book}"'
                except IntegrityError:
                    db.session.rollback()
                    message = f'Wpis książki o numerze ISBN {isbn} już istnieje w bazie danych - uzupełnij ponownie'
            else:
                message = 'Numer ISBN jest nie poprawny - uzupełnij ponownie'
        else:
            message = 'Wpis tytułu nowej książki zbyt krótki - uzupełnij ponownie'
            
    return render_template(
        'add_book.html',
        message=message,
        authors_list=authors_list,
        categories_list=categories_list
        )


if __name__ == '__main__':
    app.run(port=8000, debug=True)