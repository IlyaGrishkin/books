# Generated by Django 4.1.5 on 2023-07-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='audio',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
