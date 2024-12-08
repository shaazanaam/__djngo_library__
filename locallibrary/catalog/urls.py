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
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

]
urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('allborrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    path('author/create',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/update/',views.AuthorUpdate.as_view(),name='author-update'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]