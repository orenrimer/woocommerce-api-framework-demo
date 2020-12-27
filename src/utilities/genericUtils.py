import logging as logger
import random
import string


def generate_random_string(prefix=None, suffix=None, length=10):
    random_string = "".join(random.choices(string.ascii_lowercase, k=length))
    if prefix:
        random_string = str(prefix) + "_" + random_string
    elif suffix:
        random_string += str(suffix)
    return random_string

def generate_random_email_and_password(domain=None, prefix=None):
    random_email = generate_random_email(domain=domain, prefix=prefix)
    random_password = generate_random_password()
    return {'email':random_email, 'password':random_password}

def generate_random_email(domain=None, prefix=None):
    if not domain: domain = 'gmail.com'
    if not prefix: prefix = "testuser"

    email_length = 10
    random_string = "".join(random.choices(string.ascii_lowercase, k=email_length))
    random_email = prefix + '_' + random_string + '@' + domain
    logger.debug(f"generating random email: {random_email}")
    return random_email

def generate_random_password():
    password_length = 16
    password_string = "".join(random.choices(string.ascii_letters, k=password_length))
    logger.debug(f"generating random password: {password_string}")
    return password_string




