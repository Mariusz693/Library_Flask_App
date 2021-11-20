import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db
from sqlalchemy.exc import IntegrityError
# from flask_wtf import CSRFProtect, csrf
from validators import validate_phone, validate_email

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
    return render_template('index.html')


@app.route("/authors/")
def authors():
    authors_list = Author.query.all()
    return render_template('authors.html', authors_list=authors_list)


@app.route("/clients/")
def clients():
    return render_template('index.html')


@app.route("/add_author/", methods=['GET', 'POST'])
def add_author():
    message = 'Dodaj wpis nowego autora'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth') if request.form.get('date_of_birth') else None
        date_of_death = request.form.get('date_of_death') if request.form.get('date_of_death') else None
        if len(name) > 3:
            new_author = Author(name, date_of_birth, date_of_death)
            try:
                db.session.add(new_author)
                db.session.commit()
                message = f'Dodano wpis nowego autora - {name}'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis - {name} - już istnieje w bazie danych'
        else:
            message = 'Wpis autora zbyt krótki - nie dodano'    
            
    return render_template(
        'add_author.html',
        message=message
        )


@app.route("/edit_author/<int:id_author>/", methods=['GET', 'POST'])
def edit_author(id_author):
    author = Author.query.get_or_404(id_author)
    message = f'Zmień wpis autora {author.name}'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth') if request.form.get('date_of_birth') else None
        date_of_death = request.form.get('date_of_death') if request.form.get('date_of_death') else None
        if len(name) > 3:
            author.name = name
            author.date_of_birth = date_of_birth
            author.date_of_death = date_of_death
            try:
                db.session.commit()
                message = f'Zmieniono wpis autora - {name}'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis - {name} - już istnieje w bazie danych'
        else:
            message = 'Wpis autora zbyt krótki - nie zmieniono'    
            
    return render_template(
        'edit_author.html',
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


@app.route("/delete_author/<int:id_author>/", methods=['GET', 'POST'])
def delete_author(id_author):
    author = Author.query.get_or_404(id_author)
    message = 'Potwierdź usunięcie profilu'
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
                    new_client = Client(first_name, last_name, email, phone_number)
                    try:
                        db.session.add(new_client)
                        db.session.commit()
                        message = f'Dodano wpis nowego klinta - {new_client}'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Podany email {email} już istnieje w bazie'
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


if __name__ == '__main__':
    app.run(port=8000, debug=True)