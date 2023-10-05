from django.shortcuts import render

from store import models
from store.models import Book


def userbookView(request):
    data= {"message": Book.objects.all()}
    return render(request,'userbook.html', context=data)