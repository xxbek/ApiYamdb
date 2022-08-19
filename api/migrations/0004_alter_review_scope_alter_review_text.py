# Generated by Django 4.1 on 2022-08-19 05:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_category_id_alter_comments_id_alter_genre_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='scope',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=6000),
        ),
    ]
