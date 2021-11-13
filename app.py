import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db

load_dotenv()

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Book, Client, Category, Author


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/books/")
def books():
    return render_template('index.html')


@app.route("/authors/")
def authors():
    return render_template('index.html')


@app.route("/clients/")
def clients():
    return render_template('index.html')


@app.route("/add_author/", methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        new_author = Author(name)
        db.session.add(new_author)
        db.session.commit()
        
        return "Dodano autora"

    return render_template('author_add.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)