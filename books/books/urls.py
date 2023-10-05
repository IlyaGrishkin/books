"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin

from django.urls import path, include, re_path

from rest_framework.routers import SimpleRouter, DefaultRouter

from django.urls import path
from store.views import *

# router = SimpleRouter()
# router.register(r'', BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/auth/', include('rest_framework.urls')),
    path('like/<int:pk>/', like, name='like'),
    path('comments/<int:pk>/', comment),
    path('rating/<int:pk>/', rating),
    path('book/<int:pk>/', book_detail, name='book'),
    # path('api/', include(router.urls)),
    path('api/adding/book/', BookCreateViewSet.as_view()),
    path('search/', search_book, name='search_book'),
    path('all/ratings/<int:pk>/', show_all_ratings_and_comments, ),
    path('basket/<int:pk>/', add_to_basket),
    path('profile/form/', get_profile_form),
    path('profile/add/', add_profile_info),
    path('profile/info/', show_profile_info)
]

# urlpatterns += router.urls
