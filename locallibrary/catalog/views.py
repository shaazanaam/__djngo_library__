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
#The generic view will query the database to get all records for the specified model (Book) and render them 
# using a template.
#located at /locallibrary/catalog/templates/catalog/book_list.html.
#Within the template, the object_list  or the book_list variable will contain the list of books to display.
#Or more generically <model_name>_list.
# The generic views look for tempaltes in /application_name/model_name_list.html
#in this case, /locallibrary/catalog/book_list.html).
#inside the applciaiton's (/application_name/templates/) directory.
#/catalog/templates/catalog/book_list.html
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
    ## this is a generic view example that fetches the object based on the primary key(pk) 
    ## the only catch is that it expects the URL parameter to be named pk
    ## if you use generic.DetailsView the url configuration must use the name pk because the generic view looks  for the exact names



from django.contrib.auth.mixins import LoginRequiredMixin  ## this is used to ensure that only logged in users can access the view
                                                           ## which we are going to create for the loaned books by user
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    

## Challenge:Yourself
## Create a similar page that is only visible for librarians, that displays all books that are currently on loan.

from django.contrib.auth.mixins import PermissionRequiredMixin  ##ensures that the user has the required permission to access the view

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10
    
    




#form handling
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

## A basic Model form containing  the same field as the original RenewBookForm is shown
##You need to add class Meta with the associated (BookInstance)  and  list of model 
## fields that you want to include in the form.

from django.forms import ModelForm
from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': ('New renewal date')}
        help_texts = {'due_back': ('Enter a date between now and 4 weeks (default 3).')}