import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db
from sqlalchemy.exc import IntegrityError
# from flask_wtf import CSRFProtect, csrf

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
            
            print(new_author)
            print(new_author.date_of_birth)
            print(new_author.date_of_death)
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


if __name__ == '__main__':
    app.run(port=8000, debug=True)