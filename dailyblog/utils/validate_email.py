#-*- coding:utf-8 -*-

"""

the email valition compile:
        [a-zA-Z0-9_-]+@\\.[a-zA-Z0-9_-]+$
I think it is very easy to understand

"""


from django.core.validators import validate_email
from django.core.exceptions import ValidationError





def ValidateEmail(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True





