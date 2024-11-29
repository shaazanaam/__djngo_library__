from django.contrib import admin

# Register your models here.
# This code registers the models with the admin site. and then 
# calls the admin.site.register() method to register the models

from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)


# The line above assumes that you accepted the challenge to create model to represent the natural language of the book.


