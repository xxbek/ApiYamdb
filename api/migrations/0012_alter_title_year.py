# Generated by Django 4.1 on 2022-09-14 09:16

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_title_description_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(null=True, validators=[api.utils.date_not_in_future]),
        ),
    ]
