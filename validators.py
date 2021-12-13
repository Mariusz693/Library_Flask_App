from datetime import datetime


def validate_phone(phone_number):

    if len(phone_number) != 9:
        
        return False

    for number in phone_number:
        if not number.isdigit():
    
            return False
    
    return True


def validate_isbn(isbn):

    if len(isbn) != 13:
        
        return False

    for number in isbn:
        if not number.isdigit():
    
            return False
    
    return True


def validate_email(email):
    split_email = email.split('@')
    
    if len(split_email) == 2:
        split_email_domain = split_email[1].split('.')
    
        if len(split_email_domain) < 2:
            
            return False
    
    else:
    
        return False

    return True


def validate_date(date_of_birth, date_of_death):
    
    if date_of_birth == '':

        return 'Brak daty urodzenia autora - uzupełnij ponownie'
    
    if datetime.strptime(date_of_birth, '%Y-%m-%d').date() > datetime.today().date():

        return 'Data urodzenia autora nie może być datą przyszłą - uzupełnij ponownie'
    
    if date_of_death and datetime.strptime(date_of_death, '%Y-%m-%d').date() > datetime.today().date():

        return 'Data śmierci autora nie może być datą przyszłą - uzupełnij ponownie'
    
    if date_of_death and datetime.strptime(date_of_birth, '%Y-%m-%d').date() > datetime.strptime(date_of_death, '%Y-%m-%d').date():

        return 'Data urodzenia autora nie może być większa od daty śmierci - uzupełnij ponownie'
    
    return False