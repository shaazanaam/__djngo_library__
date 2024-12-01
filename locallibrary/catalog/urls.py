# Description: URL Configuration for the catalog application
#the text defines the imported urlpatterns

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # this path function defines a pattern to match against the URL('/books') , a view function 
    # that will be called if the URL matches(views.BookListView.as_view()), and a name 
    # that you can use to uniquely identify the URL (books).
    path('books/', views.BookListView.as_view(), name='books'),
]

