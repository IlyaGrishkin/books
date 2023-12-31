# Generated by Django 4.1.5 on 2023-06-18 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0016_book_likes_delete_booklike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='likes',
        ),
        migrations.CreateModel(
            name='LikeBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
