from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTestCases(TestCase):
    def test_reviews(self):
        book = Book.objects.create(title='Book', description='lorem', isbn=111)

        user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir')
        user.set_password('somepass')
        user.save()

        self.client.login(username='AkobirDev', password='somepass')

        review1 = BookReview.objects.create(book=book, user=user, stars=3, review_text='Nice book')
        review2 = BookReview.objects.create(book=book, user=user, stars=4, review_text='Very good book')
        review3 = BookReview.objects.create(book=book, user=user, stars=5, review_text='Awesome')
        response = self.client.get(reverse('home_page') + '?page_size=2' +  '&page=1')


        self.assertContains(response, review3.review_text)
        self.assertContains(response, review2.review_text)
        self.assertNotContains(response, review1.review_text)