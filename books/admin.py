from django.contrib import admin
from .models import Book, BookAuthor, BookReview, Author
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn')
admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email')
admin.site.register(Author, AuthorAdmin)


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')
    list_display = ('book', 'author')
admin.site.register(BookAuthor, BookAuthorAdmin)


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('user', 'review_text', 'stars')
    list_display = ('user', 'review_text', 'stars')
admin.site.register(BookReview, BookReviewAdmin)