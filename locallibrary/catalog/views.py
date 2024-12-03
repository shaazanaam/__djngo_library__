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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits +=1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_fiction': num_genres_fiction,
        'num_books_with_fiction': num_books_with_fiction,
        'num_visits': num_visits,
    }

# Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic
#The generic view will query the database to get all records for the specified model (Book) and render them using a template.
#located at /locallibrary/catalog/templates/catalog/book_list.html(we will create this file in the next step).
#Within the template, the object_list  or the book_list variable will contain the list of books to display.
#Or more generically <model_name>_list.
# The generic views look for tempaltes in /application_name/model_name_list.html
#(in this case, /locallibrary/catalog/book_list.html). inside the applciaiton's (/application_name/templates/) directory.
#(/catalog/templates/catalog/book_list.html)
class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'book_list' # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name='catalog/book_list'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        #Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    
class BookDetailView(generic.DetailView):
    model = Book
    # template_name = 'catalog/book_detail.html'  # Specify your own template name/location


