

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from books import settings
from store import models
from store.models import CommentBook, Book, Like

BOOK_ACTION_OPTIONS=settings.BOOK_ACTION_OPTIONS


class BooksSerializer(ModelSerializer):


    class Meta:
        model= Book
        fields=('id', 'name','readers')

class BookLikeSerializer(serializers.ModelSerializer):
      class Meta:
          model=Like
          fields=('total_likes', 'book_id')

