from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, permission_classes

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from store.forms import CommentForm, NewBookForm, SearchBookForm, RatingForm, ProfileForm
from store.models import Rating, Basket, Profile

from store.serializer import *


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()  # QuerySet, по сути, — список объектов заданной модели. QuerySet позволяет читать данные из базы данных, фильтровать и изменять их порядок.
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]

    filterset_fields = ['price']
    search_fields = ['name', 'writer']
    ordering_fields = ['price', 'writer', 'name']

    def perfom_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def home(request):
    queryset = Book.objects.all()
    context = {
        'books': queryset,
        'form': SearchBookForm()
    }
    return render(request, 'home.html', context)


def get_profile_form(request):
    context = {
        'profile_form': ProfileForm,
    }
    return render(request, 'profile_add.html', context)


def add_profile_info(request):
    data = ProfileForm(request.POST, request.FILES)
    if data.is_valid():
        photo = data.cleaned_data['photo']
        birthday = data.cleaned_data['birthday']
        profile = Profile.objects.create(user=request.user, photo=photo, birthday=birthday)
        profile.save()
        return redirect('/profile/info/')
    else:
        return render(request, 'error.html')


def show_profile_info(request):
    user_info = Profile.objects.filter(user=request.user)
    if not user_info:
        return render(request, 'empty_profile.html')
    for obj in user_info:
        photo = obj.photo
        birthday = obj.birthday
        context = {
            'username': request.user,
            'photo': photo,
            'birthday': birthday,
        }
        return render(request, 'profile_info.html', context)


def add_to_basket(request, pk):
    book = get_object_or_404(Book, id=pk)
    if Basket.objects.filter(user=request.user, book_id=pk,
                             ).exists():
        book_in_basket = Basket.objects.filter(user=request.user, book_id=pk, )

        book_in_basket.delete()
        status = 'Товар удален из корзины'
        context = {
            'status': status,
        }
        return render(request, 'basket.html', context)
    else:
        book_in_basket = Basket.objects.create(user=request.user, book_id=pk)
        book_in_basket.save()
        status = 'Товар добавлен в корзину'
        context = {
            'status': status,
            'book': book
        }
        return render(request, 'basket.html', context)


def show_all_ratings_and_comments(request, pk):
    all_ratings_for_book = Rating.objects.filter(book_id=pk)
    all_comments_for_book = CommentBook.objects.filter(book_id=pk)
    context = {
        'all_ratings': all_ratings_for_book,
        'all_comments': all_comments_for_book
    }
    return render(request, 'all_ratings.html', context)


def book_detail(request, pk):
    book = Book.objects.filter(id=pk)

    rates = []
    all_ratings_for_book = Rating.objects.filter(book_id=pk)
    if all_ratings_for_book is not None:
        for rate in all_ratings_for_book:
            rates.append(int(rate.value))
        res = sum(rates) / len(rates)

        context = {
            'book': book,
            'book_id': pk,
            'rating_form': RatingForm(),
            'comment_form': CommentForm(),
            'ratings': Rating.objects.filter(book_id=pk),
            'average_rating': res

        }
        return render(request, "book_detail.html", context)


@api_view(['POST'])
def search_book(request):
    if request.method == 'POST':
        search_form = SearchBookForm(request.POST)
        if search_form.is_valid():
            name = search_form.cleaned_data['name']
            queryset = Book.objects.filter(name__contains=name)
            if queryset:
                context = {
                    'filtered_books': queryset,

                }
                return render(request, 'search_results.html', context)
            else:
                return render(request, 'Notfound.html')
        else:
            return render(request, 'error.html')
    return render(request, 'error2.html')


class BookCreateViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_book = NewBookForm(request.POST, request.FILES)
        if new_book.is_valid():
            name = new_book.cleaned_data['name']
            price = new_book.cleaned_data['price']
            writer = new_book.cleaned_data['writer']
            image = new_book.cleaned_data['image']
            audio = new_book.cleaned_data['audio']
            book = Book.objects.create(owner=request.user, name=name, price=price, writer=writer, image=image,
                                       audio=audio)
            book.save()
            return render(request, 'added.html')
        else:
            return render(request, 'error.html')


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def like(request, pk, *args, **kwargs):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=pk)
        obj = book.first()
        if not book.exists():
            return Response({}, status=404)
        if Like.objects.filter(user=request.user, book_id=pk,
                               ).exists():
            like = Like.objects.filter(user=request.user, book_id=pk, )

            like.delete()
            context = {
                'Total': Like.objects.filter(book_id=pk).count()
            }
            return render(request, 'delete.html', context)
        else:
            like = Like.objects.create(user=request.user, book_id=pk,
                                       content_object=obj)
            like.save()

            context = {
                'Total': Like.objects.filter(book_id=pk).count()
            }
            return render(request, 'book.html', context)


@api_view(['POST'])
def rating(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        new_rating = RatingForm(request.POST)
        if Rating.objects.filter(user=request.user, book_id=pk,
                                 ).exists():
            return render(request, 'repeat_error.html')
        else:
            if new_rating.is_valid():
                new_rating = new_rating.save(commit=False)
                new_rating.user = request.user
                new_rating.book = book
                new_rating.save()
                context = {
                    'book': book
                }
                return render(request, 'rating.html', context=context)
            return render(request, 'error2.html')

    return render(request, 'error.html')


@csrf_exempt
@permission_classes([IsAuthenticatedOrReadOnly])
def comment(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        new_comment = CommentForm(request.POST)
        if new_comment.is_valid():
            new_comment = new_comment.save(commit=False)
            if request.user.is_authenticated:
                new_comment.user = request.user
                new_comment.book = book
                new_comment.save()
                return render(request, 'comment.html')
            else:
                return render(request, 'error2.html')

        else:
            return render(request, 'error.html')
