# Generated by Django 4.1 on 2022-09-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_newuser_conformation_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
