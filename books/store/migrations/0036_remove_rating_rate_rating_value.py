# Generated by Django 4.1.5 on 2023-08-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rate',
        ),
        migrations.AddField(
            model_name='rating',
            name='value',
            field=models.CharField(blank=True, choices=[('1', 'Ужасно'), ('2', 'Плохо'), ('3', 'Средне'), ('4', 'Хорошо'), ('5', 'Отлично')], max_length=1),
        ),
    ]