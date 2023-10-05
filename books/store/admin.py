from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, CommentBook

'''class CommentAdmin(ModelAdmin):
    list_display = ('book')
    search_fields = ('comment')
admin.site.register (CommentBook, CommentAdmin)
'''
@admin.register(Book)
class BookAdm(ModelAdmin):
    pass






