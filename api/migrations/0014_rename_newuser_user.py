# Generated by Django 4.1 on 2022-09-14 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('api', '0013_rename_scope_review_score'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewUser',
            new_name='User',
        ),
    ]
