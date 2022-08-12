import datetime
from django.core import exceptions


def date_not_in_future(year):
    if year > datetime.datetime.now().year:
        raise exceptions.ValidationError
