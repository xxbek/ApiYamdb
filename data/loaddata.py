import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from api.models import Genre, Category, Title, Review, NewUser

with open('users.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = NewUser(id=row['id'], username=row['username'],
                    email=row['email'], role=row['role'], bio=row['bio'],
                    first_name=row['first_name'], last_name=row['last_name'])
        p.save()
