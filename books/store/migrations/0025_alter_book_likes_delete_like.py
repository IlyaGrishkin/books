# Generated by Django 4.1.5 on 2023-06-23 12:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0024_remove_book_total_likes_like_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
