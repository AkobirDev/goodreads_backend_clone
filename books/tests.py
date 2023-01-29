from django.test import TestCase
from django.urls import reverse

from books.models import Book

# Create your tests here.

class BooksTestCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No Books Found...')

    def test_book_list(self):
        Book.objects.create(title='Book1', description='lorem1', isbn = '111')
        Book.objects.create(title='Book2', description='lorem2', isbn = '222')
        Book.objects.create(title='Book3', description='lorem3', isbn = '333')
        
        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)


    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='lorem1', isbn = '111')
        
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))


        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        

