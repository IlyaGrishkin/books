# Generated by Django 4.1.5 on 2023-05-10 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_commentbook_name_commentbook_user_alter_book_readers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='likes',
        ),
    ]