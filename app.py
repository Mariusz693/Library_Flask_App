from operator import le
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect
# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db
from sqlalchemy.exc import IntegrityError
# from flask_wtf import CSRFProtect, csrf
from validators import validate_phone, validate_email, validate_isbn, validate_date

load_dotenv()

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# csrf = CSRFProtect(app)

from models import Book, Client, Category, Author, Books_Clients


@app.route("/")
def index():
    
    return render_template('index.html')


@app.route("/books/")
def books():
    books_list = Book.query.order_by(Book.title).all()
    
    return render_template(
        'books.html',
        books_list=books_list
        )


@app.route("/authors/")
def authors():
    authors_list = Author.query.order_by(Author.name).all()
    
    return render_template(
        'authors.html',
        authors_list=authors_list
        )


@app.route("/clients/")
def clients():
    clients_list = Client.query.order_by(Client.last_name).all()
    
    return render_template(
        'clients.html',
        clients_list=clients_list
        )


@app.route("/add_author/", methods=['GET', 'POST'])
def add_author():
    message = 'Dodaj wpis nowego autora'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth')
        date_of_death = request.form.get('date_of_death')
        date_check = validate_date(date_of_birth, date_of_death)
        if len(name) > 2 and not date_check:
            new_author = Author(
                name=name, 
                date_of_birth=date_of_birth, 
                date_of_death=date_of_death if date_of_death else None
                )
            try:
                db.session.add(new_author)
                db.session.commit()
                message = f'Dodano wpis nowego autora - {name}'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis autora już istnieje w bazie danych - {name} - uzupełnij ponownie'
        elif len(name) <= 2:
            message = f'Wpis autora zbyt krótki - {name} - uzupełnij ponownie'    
        elif date_check:
            message = date_check
            
    return render_template(
        'add_author.html',
        message=message
        )


@app.route("/edit_author/<int:id_author>/", methods=['GET', 'POST'])
def edit_author(id_author):
    author = Author.query.get_or_404(id_author)
    message = f'Zmień wpis autora - {author}'
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth')
        date_of_death = request.form.get('date_of_death')
        date_check = validate_date(date_of_birth, date_of_death)
        if len(name) > 2 and not date_check:
            author.name = name
            author.date_of_birth = date_of_birth
            author.date_of_death = date_of_death if date_of_death else None
            try:
                db.session.commit()
                message = f'Zmieniono wpis autora - {name}'
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis autora już istnieje w bazie danych - {name} - uzupełnij ponownie'
        elif len(name) <= 2:
            message = f'Wpis autora zbyt krótki - {name} - uzupełnij ponownie'    
        elif date_check:
            message = date_check
            
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
        for book in author.books:
            if book.borrowed_copies > 0:
                message = 'Książki autora są na wypożyczeniu, usuń gdy zostaną zwrócone'
                break
        else:
            try:
                db.session.delete(author)
                db.session.commit()

                return redirect('/authors/')
            
            except IntegrityError:
                db.session.rollback()
                message = f'Błąd w usuwaniu profilu autora'
        
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
        if len(first_name) > 3 and len(last_name) > 3:
            if phone_number == '' or validate_phone(phone_number):
                if email and validate_email(email):
                    new_client = Client(
                        first_name=first_name, 
                        last_name=last_name, 
                        email=email, 
                        phone_number=phone_number
                        )
                    try:
                        db.session.add(new_client)
                        db.session.commit()
                        message = f'Dodano wpis nowego klinta - {new_client}'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis email klienta już istnieje w bazie - {email} - uzupełnij ponownie'
                else:
                    message = 'Brak adresu email lub źle podany - uzupełnij ponownie'
            else:
                message = 'Numer telefonu źle podany - uzupełnij ponownie'
        else:
            message = 'Brak imienia lub nawiska klienta - uzupełnij ponownie'
            
    return render_template(
        'add_client.html',
        message=message
        )


@app.route("/edit_client/<int:id_client>/", methods=['GET', 'POST'])
def edit_client(id_client):
    client = Client.query.get_or_404(id_client)
    message = f'Zmień wpis klienta - {client}'
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        if len(first_name) > 3 and len(last_name) > 3:
            if phone_number == '' or validate_phone(phone_number):
                if email and validate_email(email):
                    client.first_name = first_name
                    client.last_name = last_name
                    client.email = email
                    client.phone_number = phone_number
                    try:
                        db.session.commit()
                        message = f'Zmieniono wpis klinta - {client}'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis email klienta już istnieje w bazie - {email} - uzupełnij ponownie'
                else:
                    message = 'Brak adresu email lub źle podany - uzupełnij ponownie'
            else:
                message = 'Numer telefonu źle podany - uzupełnij ponownie'
        else:
            message = 'Brak imienia lub nawiska klienta - uzupełnij ponownie'
        
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
        for loan in client.books:
            if loan.return_date is None:
                message = 'Klient posiada książki na wypożyczeniu, usuń gdy zwróci wszystkie'
                break
        else:
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
    actuall_loan = Books_Clients.query.filter_by(client=client, return_date=None).order_by(Books_Clients.loan_date.asc()).all()
    
    return render_template(
        'details_client.html',
        client=client,
        actuall_loan=actuall_loan
        )


@app.route("/categories/", methods=['GET', 'POST'])
def categories():
    categories = Category.query.order_by(Category.name).all()
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
                categories = Category.query.order_by(Category.name).all()

            except IntegrityError:
                db.session.rollback()
                message = 'Błąd w usuwaniu kategorii'
        elif len(name) > 2:
            new_category = Category(name=name)
            try:
                db.session.add(new_category)
                db.session.commit()
                message = f'Dodano nową kategorię - "{new_category}"'
                categories = Category.query.order_by(Category.name).all()
    
            except IntegrityError:
                db.session.rollback()
                message = f'Wpis kategorii już istnieje w bazie danych - "{name}"'
        elif name:
            message = f'Wpis kategorii zbyt krótki - "{name}" - uzupełnij ponownie'
    
    return render_template(
        'categories.html',
        categories=categories,
        message=message
        )


@app.route("/add_book/", methods=['GET', 'POST'])
def add_book():
    message = 'Dodaj wpis nowej książki'
    authors_list = Author.query.order_by(Author.name).all()
    categories_list = Category.query.order_by(Category.name).all()
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
                    date_check = validate_date(date_of_birth, date_of_death)
                    if Author.query.filter_by(name=name).first() or len(name) < 3 or date_check:
                        if name == '':
                            message = 'Wybierz autora z listy lub wpisz nową pozycję - uzupełnij ponownie'
                        elif len(name) < 3:
                            message = f'Wpis nowego autora zbyt krótki - {name} - uzupełnij ponownie'
                        elif Author.query.filter_by(name=name).first():
                            message = f'Wpis autora już istnieje - {name}, wybierz z listy autorów - uzupełnij ponownie'
                        elif date_check:
                            message = date_check
                        
                        return render_template(
                            'add_book.html',
                            message=message,
                            authors_list=authors_list,
                            categories_list=categories_list
                            )

                    author_book = Author(
                        name=name, 
                        date_of_birth=date_of_birth, 
                        date_of_death=date_of_death if date_of_death else None
                        )
                else:
                    author_book = Author.query.filter_by(id=author).first()
                
                if new_category:
                    if Category.query.filter_by(name=new_category).first() or len(new_category) < 3:
                        if len(new_category) < 3:
                            message = f'Wpis kategorii zbyt krótki - "{new_category}" - uzupełnij ponownie'
                        else:
                            message = f'Wpis kategorii już istnieje - "{new_category}", wybierz z listy kategorii - uzupełnij ponownie'
                        
                        return render_template(
                            'add_book.html',
                            message=message,
                            authors_list=authors_list,
                            categories_list=categories_list
                            )

                    new_category = Category(name=new_category)
                
                try:
                    if author == '':
                        db.session.add(author_book)
                        db.session.commit()
                    if new_category:
                        db.session.add(new_category)
                        db.session.commit()
                        categories.append(str(new_category.id))
                    new_book = Book(
                        isbn=isbn, 
                        title=title,
                        description=description,
                        copies=int(copies),
                        author=author_book
                        )
                    categories_set = Category.query.filter(Category.id.in_(categories))
                    new_book.categories.extend(categories_set)
                    db.session.add(new_book)
                    db.session.commit()
                    message = f'Dodano wpis nowej książki "{new_book}"'
                except IntegrityError:
                    db.session.rollback()
                    message = f'Wpis książki o numerze ISBN {isbn} już istnieje w bazie danych - uzupełnij ponownie'

                authors_list = Author.query.order_by(Author.name).all()
                categories_list = Category.query.order_by(Category.name).all()

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


@app.route("/edit_book/<int:id_book>/", methods=['GET', 'POST'])
def edit_book(id_book):
    book = Book.query.get_or_404(id_book)
    message = f'Zmień wpis książki "{book}"'
    authors_list = Author.query.order_by(Author.name).all()
    categories_list = Category.query.order_by(Category.name).all()
    book.categories_set = []
    for item in book.categories:
        book.categories_set.append(item.id)

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        description = request.form.get('description')
        author = request.form.get('author')
        categories = request.form.getlist('categories')
        new_category = request.form.get('new_category')
        copies = int(request.form.get('copies'))

        if len(title) > 2:
            if validate_isbn(isbn):
                if copies >= book.borrowed_copies:
                    if author == '':
                        name = request.form.get('author_name')
                        date_of_birth = request.form.get('author_date_of_birth')
                        date_of_death = request.form.get('author_date_of_death')
                        date_check = validate_date(date_of_birth, date_of_death)
                        if Author.query.filter_by(name=name).first() or len(name) < 3 or date_check:
                            if name == '':
                                message = 'Wybierz autora z listy lub wpisz nową pozycję - uzupełnij ponownie'
                            elif len(name) < 3:
                                message = f'Wpis nowego autora zbyt krótki - {name} - uzupełnij ponownie'
                            elif Author.query.filter_by(name=name).first():
                                message = f'Wpis autora już istnieje - {name}, wybierz z listy autorów - uzupełnij ponownie'
                            elif date_check:
                                message = date_check
                            
                            return render_template(
                                'add_book.html',
                                message=message,
                                authors_list=authors_list,
                                categories_list=categories_list
                                )

                        author_book = Author(
                            name=name, 
                            date_of_birth=date_of_birth, 
                            date_of_death=date_of_death if date_of_death else None
                            )       
                    else:
                        author_book = Author.query.filter_by(id=author).first()
                    if new_category:
                        if Category.query.filter_by(name=new_category).first() or len(new_category) < 3:
                            if len(new_category) < 3:
                                message = f'Wpis kategorii zbyt krótki - "{new_category}" - uzupełnij ponownie'
                            else:
                                message = f'Wpis kategorii już istnieje - "{new_category}", wybierz z listy kategorii - uzupełnij ponownie'
                            
                            return render_template(
                                'add_book.html',
                                message=message,
                                authors_list=authors_list,
                                categories_list=categories_list
                                )

                        new_category = Category(name=new_category)

                    try:
                        if author == '':
                            db.session.add(author_book)
                            db.session.commit()
                        if new_category:
                            db.session.add(new_category)
                            db.session.commit()
                            categories.append(str(new_category.id))
                        book.title = title
                        book.isbn = isbn
                        book.description = description
                        book.copies = copies
                        book.author = author_book
                        book.categories.clear()
                        categories_set = Category.query.filter(Category.id.in_(categories))
                        book.categories.extend(categories_set)
                        db.session.commit()
                        message = f'Zmieniono wpis książki "{book}"'
                    except IntegrityError:
                        db.session.rollback()
                        message = f'Wpis książki o numerze ISBN {isbn} już istnieje w bazie danych - uzupełnij ponownie'

                    authors_list = Author.query.order_by(Author.name).all()
                    categories_list = Category.query.order_by(Category.name).all()
                    book.categories_set = []
                    for item in book.categories:
                        book.categories_set.append(item.id)
                else:
                    message = 'Ilość egzemplarzy musi być wieksza niż wypożyczonych - uzupełnij ponownie'        
            else:
                message = 'Numer ISBN jest nie poprawny - uzupełnij ponownie'
        else:
            message = 'Wpis tytułu nowej książki zbyt krótki - uzupełnij ponownie'
    
    return render_template(
        'edit_book.html',
        book=book,
        message=message,
        authors_list=authors_list,
        categories_list=categories_list
        )


@app.route("/delete_book/<int:id_book>/", methods=['GET', 'POST'])
def delete_book(id_book):
    book = Book.query.get_or_404(id_book)
    message = 'Potwierdź usunięcie książki'
    if request.method == 'POST':
        if book.borrowed_copies == 0:
            try:
                db.session.delete(book)
                db.session.commit()

                return redirect('/books/')
            
            except IntegrityError:
                db.session.rollback()
                message = 'Błąd w usuwaniu książki'
        else:
            message = 'Egzemplarze na wypożyczeniu, usuń gdy będą wszystkie zwrócone'
        
    return render_template(
        'delete_book.html',
        message=message,
        book=book
        )


@app.route("/details_book/<int:id_book>/")
def details_book(id_book):
    book = Book.query.get_or_404(id_book)
    
    return render_template(
        'details_book.html',
        book=book
        )


@app.route("/add_loan/", methods=['GET', 'POST'])
def add_loan():
    message = 'Dodaj wypożyczenie książki'
    books_all = Book.query.order_by(Book.title).all()
    books_list = [book for book in books_all if book.copies > book.borrowed_copies]
    clients_list = Client.query.order_by(Client.last_name).all()
    
    if request.method == 'POST':
        book = request.form.get('book')
        client = request.form.get('client')
        loan_date = request.form.get('loan_date')
        if book:
            if client:
                if loan_date:
                    book = Book.query.get_or_404(book)
                    client = Client.query.get_or_404(client)
                    new_loan = Books_Clients(book=book, client=client, loan_date=loan_date)
                    try:
                        db.session.add(new_loan)
                        book.borrowed_copies += 1
                        db.session.commit()
                        message = f'Dodano wpis wypożyczenia książki "{book}" - {client}'
                    except IntegrityError:
                        db.session.rollback()
                        message = 'Błąd w dodawaniu wypożyczenia'
                else:
                    message = 'Brak daty wypożyczenia - uzupełnij ponownie'
            else:
                message = 'Brak wybranego klienta - uzupełnij ponownie'
        else:
            message = 'Brak wybranej książki - uzupełnij ponownie'

    return render_template(
        'add_loan.html',
        message=message,
        books_list=books_list,
        clients_list=clients_list
        )


@app.route("/delete_loan/<int:id_loan>/", methods=['GET', 'POST'])
def delete_loan(id_loan):
    message = 'Zapisz zwrot książki'
    loan = Books_Clients.query.get(id_loan)
    next = request.args.get('next')

    if request.method == 'POST':
        return_date = request.form.get('return_date')
        if return_date:
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
            if return_date > loan.loan_date:            
                try:
                    loan.return_date = return_date
                    loan.book.borrowed_copies -= 1
                    db.session.commit()

                    return redirect(next)

                except IntegrityError:
                    db.session.rollback()
                    message = 'Błąd w dodawaniu zwrotu'
            else:
                message = 'Data zwrotu nie może być przed wypożyczeniem - uzupełnij ponownie'
        else:
            message = 'Brak daty zwrotu - uzupełnij ponownie'

    return render_template(
        'delete_loan.html',
        message=message,
        loan=loan
        )


@app.route("/book_loan/<int:id_book>/", methods=['GET', 'POST'])
def book_loan(id_book):
    book = Book.query.get_or_404(id_book)
    loaned = request.args.get('loaned')
    message = f'Historia wypożyczeń książki - "{book}"'
    loan_list = Books_Clients.query.filter_by(book=book).order_by(Books_Clients.loan_date.asc()).all()
    if loaned == 'True':
        loan_list = [item for item in loan_list if item.return_date == None]
        message = f'Aktualne wypożyczenia książki - "{book}"'
    
    if request.method == 'POST':
        delete_loan = request.form.getlist('delete_loan')
        delete_loan = Books_Clients.query.filter(Books_Clients.id.in_(delete_loan))
        for loan in delete_loan:
            if loan.return_date == None:
                message = 'Wybrano wypożyczenia bez zwrotu książki - wybierz ponownie'
                break
        else:
            try:
                for loan in delete_loan:
                    db.session.delete(loan)
                db.session.commit()
                message = f'Usunięto, historia wypożyczeń książki - "{book}"'
                loan_list = Books_Clients.query.filter_by(book=book).order_by(Books_Clients.loan_date.asc()).all()
            except IntegrityError:
                db.session.rollback()
                message = 'Błąd w usuwaniu historii'
    
    return render_template(
        'book_loan.html',
        book=book,
        loan_list=loan_list,
        message=message
        )


@app.route("/client_loan/<int:id_client>/", methods=['GET', 'POST'])
def client_loan(id_client):
    client = Client.query.get_or_404(id_client)
    loaned = request.args.get('loaned')
    loan_list = Books_Clients.query.filter_by(client=client).order_by(Books_Clients.loan_date.asc()).all()
    message = f'Historia wypożyczeń klienta - {client}'
    loan_list = Books_Clients.query.filter_by(client=client).order_by(Books_Clients.loan_date.asc()).all()
    if loaned == 'True':
        loan_list = [item for item in loan_list if item.return_date == None]
        message = f'Aktualne wypożyczenia klienta - {client}'
    
    if request.method == 'POST':
        delete_loan = request.form.getlist('delete_loan')
        delete_loan = Books_Clients.query.filter(Books_Clients.id.in_(delete_loan))
        for loan in delete_loan:
            if loan.return_date == None:
                message = 'Wybrano wypożyczenia bez zwrotu książki - wybierz ponownie'
                break
        else:
            try:
                for loan in delete_loan:
                    db.session.delete(loan)
                db.session.commit()
                message = f'Usunięto, historia wypożyczeń klienta - {client}'
                loan_list = Books_Clients.query.filter_by(client=client).order_by(Books_Clients.loan_date.asc()).all()
            except IntegrityError:
                db.session.rollback()
                message = 'Błąd w usuwaniu historii'
    
    return render_template(
        'client_loan.html',
        client=client,
        loan_list=loan_list,
        message=message
        )


if __name__ == '__main__':
    app.run(port=8000, debug=True)