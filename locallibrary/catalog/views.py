from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
# Create your views here.
def index(request):
    """ View function for the home page of the site."""

    #Generate counts of some of the main objects
    num_books =Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()


    # Available books (status = 'a')

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres_fiction = Genre.objects.filter(name__icontains='fiction').count()
    num_books_with_fiction = Book.objects.filter(genre__name__icontains='fiction').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_fiction': num_genres_fiction,
        'num_books_with_fiction': num_books_with_fiction,
    }
# Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)