from django.test import TestCase
from django.urls import reverse

from books.models import Book

# Create your tests here.

class BooksTestCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No Books Found...')

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='lorem1', isbn = '111')
        book2 = Book.objects.create(title='Book2', description='lorem2', isbn = '222')
        book3 = Book.objects.create(title='Book3', description='lorem3', isbn = '333')
        
        response = self.client.get(reverse('books:list') + '?page=1' + '?page_size=2')

        # books = Book.objects.all()
        for book in [book1, book2]:
            self.assertContains(response, book.title)

        
        response = self.client.get(reverse('books:list') + '?page=2' + '?page_size=2')

        self.assertNotContains(response, book3.title)
        

    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='lorem1', isbn = '111')
        
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))


        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        

    def test_search_book(self):
        book1 = Book.objects.create(title='Book1', description='lorem1', isbn = '111')
        book2 = Book.objects.create(title='Book2', description='lorem2', isbn = '222')
        book3 = Book.objects.create(title='Book3', description='lorem3', isbn = '333')

        response = self.client.get(reverse('books:list') + '?q=book1')
        print(response)
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)