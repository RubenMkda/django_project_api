# Generated by Django 4.2.3 on 2023-07-13 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_projects'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='user_id',
            new_name='user',
        ),
    ]
