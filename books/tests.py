from django.test import TestCase
from django.urls import reverse

from books.models import Author, Book, BookReview
from users.models import CustomUser

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


    # def test_book_author(self):
    #     book1 = Book.objects.create(title='Book1', description='lorem1', isbn = '111')
    #     author1 = Author.objects.create(first_name='Ali', last_name='Vali', email='ali@mail.ru')
    #     author2 = Author.objects.create(first_name='Vali', last_name='Ali', email='vali@mail.ru')
    #     authors = book1.bookauthor_set.all()
    #     response = self.client.get(reverse('books:detail', kwargs={id:book1.id}))


class BookReviewTestCases(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description='lorem1', isbn = '111')

        user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir')
        user.set_password('somepass')
        user.save()
        
        self.client.login(username='AkobirDev', password='somepass')

        response = self.client.post(
            reverse('books:reviews', kwargs={'id':book.id} ),
            data={
                'stars': 6,
                'review_text': 'Nice book'
            }
        )



        response = self.client.post(
            reverse('books:reviews', kwargs={'id':book.id} ),
            data={
                'stars': 3,
                'review_text': 'Nice book'
            }
        )

        book_reviews = book.bookreview_set.all()    

        count = BookReview.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(book_reviews[0].stars, 3)
        self.assertEqual(book_reviews[0].review_text, 'Nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)