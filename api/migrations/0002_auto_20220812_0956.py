# Generated by Django 3.0.5 on 2022-08-12 09:56

import api.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Review'),
        ),
        migrations.AddField(
            model_name='newuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Об авторе'),
        ),
        migrations.AddField(
            model_name='newuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Крд подтверждения'),
        ),
        migrations.AddField(
            model_name='newuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', max_length=50, verbose_name='Представление'),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(blank=True, max_length=6000),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[api.utils.date_not_in_future]),
        ),
    ]
