from django import forms

from store.models import CommentBook, Image, Book, Rating, Profile


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentBook
        fields = ('comment',)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        labels = {
            'value': 'Оценить',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'birthday', ]


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'price', 'writer', 'image', 'audio', ]


class SearchBookForm(forms.Form):
    name = forms.CharField(max_length=200)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'book_id', ]
