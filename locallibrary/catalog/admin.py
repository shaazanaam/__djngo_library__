from django.contrib import admin

# Register your models here.
# This code registers the models with the admin site. and then 
# calls the admin.site.register() method to register the models

from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
## AUTHOR ADMIN
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    
# Register the AuthorAdmin class with the model 
admin.site.register(Author, AuthorAdmin)

#BOOK INSTANCE INLINE
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0



## BOOK ADMIN
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'display_language')
    inlines = [BooksInstanceInline]
    
# Register the BookAdmin class with the model
admin.site.register(Book, BookAdmin)

## BOOK INSTANCE ADMIN
## added the borrower field in thebook admin class
# this will make the field visible in the Admin section allowing us to assign a User to a 
# Book instance when needed
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ( 'book','status','borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets=(
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
# Register the BookInstanceAdmin class with the model
admin.site.register(BookInstance, BookInstanceAdmin)


# The line above assumes that you accepted the challenge to create model to represent the natural language of the book.


