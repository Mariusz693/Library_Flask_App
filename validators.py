

def validate_phone(phone_number):
        
    for number in phone_number:
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