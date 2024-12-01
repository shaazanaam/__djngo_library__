from django.db import models
from django.urls import reverse # USED IN THE get_absolute_url() method to get the URL for the specified ID
from django.db.models  import UniqueConstraint #   Constrains a field to unique values
from django.db.models.functions import Lower #  A function that converts a string to lowercase

# Create your models here.
## this model below is used to store information about the book category
#Here we are creating the model for the book category
## rathern than as free text or a selection list so that the possible 
#values can be managed in the data base 
# rather than being hard coded in the application code.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
                max_length=200, 
                unique=True,
                help_text="""Enter a book genre (e.g. Science Fiction, 
                French Poetry etc.)"""
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
# After the field, we declare a __str__() method, which returns the name 
# of the genre defined by a particular record. No verbose name has been defined, 
# so the field label will be Name when it is used in forms. Then we declare the get_absolute_url() method, 
# which returns a URL that can be used to access a detail record for this model (for this to work, we will 
# have to define a URL mapping that has the name genre-detail, and define an associated view and template).
    
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('genre-detail', args=[str(self.id)])
    ## used to declare the model level metadat for the Genre model
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="""A genre with this name already exists.
                case-insensitive match"""
                ),
                
        ]

## this model below is used to store information about the book####
## The book model stores information about a book, such as its title, author, and summary.
# But this does not include a particular physical instance of a book (which would be a BookInstance).

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
# Foreign Key used because book can only have one author, but authors can have multiple books
# Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book',
                               default='No summary available')
    isbn = models.CharField('ISBN', max_length=13,unique=True,default='0000000000000',
                             help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

# ManyToManyField used because genre can contain many books. Books can cover many genres.
# Genre class has already been defined so we can specify the object above.
#In both field types the related model class is declared as the first unnamed parameter using 
# either the model class or a string containing the name of the related model. You must use the name of the model
#  as a string if the associated class has not yet been defined in this file before it is referenced! 
# The other parameters of interest in the author field are null=True, which allows the database to store a 
# Null value if no author is selected, and on_delete=models.RESTRICT, which will prevent the book's associated 
# author being deleted if it is referenced by any book.


    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'
    
    ## this model below is used to store information about the book Instance
    ## The BookInstance model represents a specific copy of a 
    # book that someone might borrow and includes information about
    #  whether the copy is available or on loan, its due date, and so on.
    # Some of the fields and methods will now be familiar. The model uses:

    #ForeignKey to identify the associated Book 
    # (each book can have many copies, but a copy can only have one Book).
    #  The key specifies on_delete=models.RESTRICT to ensure that the Book 
    # cannot be deleted while referenced by a BookInstance.
    #CharField to represent the imprint (specific release) of the book.

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
    ## this model below is used to store information about the author

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'



##This model below is for the Language model
#The Language model is used to store information about the language in which the book is written.
#The model is very simple, with only a single field to store the language name.
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,unique= True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
        

    