from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    writer = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='my_books')  # foreingkey у чего то одного может быть много чего другого
    readers = models.ManyToManyField(User, related_name='books')
    description = models.CharField(max_length=800, null=True)
    image = models.ImageField(blank=True)
    audio = models.FileField(blank=True)

    def __str__(self):
        return f'{self.name}, Цена: {self.price}, Владелец:{self.owner}'

    def get_absolute_url(self):
        return reverse('book', args=[self.pk])


class CommentBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    comment = models.TextField(max_length=2000)
    name = models.CharField(max_length=30, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Id{self.id}:{self.book}:{self.comment}:{self.user}'


class Rating(models.Model):
    CHOICES = [
        ('1', 'Ужасно'),
        ('2', 'Плохо'),
        ('3', 'Средне'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=1, choices=CHOICES, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Рейтинг: {self.value} * {self.user}'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # ToDo: balance = models.BigIntegerField()
    photo = models.ImageField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_id = models.PositiveIntegerField()
    total_likes = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'book_id')

    def __str__(self):
        return f'User:  {self.user}  Book:{self.book_id}{self.content_object}'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    in_basket = models.BooleanField(default=False)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    book_id = models.PositiveIntegerField()
