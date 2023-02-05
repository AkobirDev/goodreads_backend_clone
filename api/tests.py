from django.test import TestCase
from rest_framework.test import APITestCase
from books.models import Book, BookReview
from users.models import CustomUser
from rest_framework.reverse import reverse
# Create your tests here.

class BookReviewApiTestCases(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir')
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='AkobirDev', password='somepass')

    def test_book_reviews(self):
        user_two = CustomUser.objects.create(username='AkobirDev2', first_name='Akobir2')
        
        book = Book.objects.create(title='book1', description='lorem1', isbn='111')
        # book_two = Book.objects.create(title='book2', description='lorem2', isbn='222')
        br_two = BookReview.objects.create(book=book, review_text='some text2', user=user_two, stars=3)
        br = BookReview.objects.create(book=book, review_text='some text1', user=self.user, stars=5)

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['stars'], br_two.stars)
        self.assertEqual(response.data['results'][0]['review_text'], br_two.review_text)
        self.assertEqual(response.data['results'][1]['stars'], br.stars)
        self.assertEqual(response.data['results'][1]['review_text'], br.review_text)
        self.assertEqual(response.data['results'][0]['user']['username'], user_two.username)  
        self.assertEqual(response.data['results'][1]['user']['username'], self.user.username)
        

    def test_book_review_detail(self):
        book = Book.objects.create(title='book', description='lorem', isbn='111')
        br = BookReview.objects.create(book=book, review_text='some text', user=self.user, stars=5)
        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))


        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars'], 5)
        self.assertEqual(response.data['review_text'], 'some text')
        # self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'book')
        self.assertEqual(response.data['book']['description'], 'lorem')
        self.assertEqual(response.data['book']['isbn'], '111')
        self.assertEqual(response.data['user']['username'], 'AkobirDev')
        # self.assertEqual(response.data['user']['password'], 'somepass')


    def test_delete_review(self):
        book = Book.objects.create(title='book1', description='lorem1', isbn='111')
        br = BookReview.objects.create(book=book, review_text='some text1', user=self.user, stars=5)

        response = self.client.delete(reverse('api:review_detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    
    def test_patch_review(self):
        book = Book.objects.create(title='book1', description='lorem1', isbn='111')
        br = BookReview.objects.create(book=book, review_text='some text1', user=self.user, stars=5)

        response = self.client.patch(
            reverse('api:review-detail', kwargs={'id': br.id}),
            data = {
                'stars': 3
            }
            )

        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars, 3)

        response = self.client.patch(
            reverse('api:review-detail', kwargs={'id': br.id}),
            data = {
                'review_text': 'Edited text'
            }
            )

        br.refresh_from_db()

        self.assertEqual(br.review_text, 'Edited text')

    
    def test_put_review(self):
        book = Book.objects.create(title='book1', description='lorem1', isbn='111')
        br = BookReview.objects.create(book=book, review_text='some text1', user=self.user, stars=5)

        response = self.client.put(
        reverse('api:review-detail', kwargs={'id': br.id}),
        data = {
            'stars': 4,
            'review_text': 'Edited text',
            'book_id': book.id,
            'user_id': self.user.id
        }
        )

        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars, 4)
        self.assertEqual(br.review_text, 'Edited text')

    
    def test_create_review(self):
        book = Book.objects.create(title='book1', description='lorem1', isbn='111')
        
        response = self.client.post(
        reverse('api:review-list'),
        data = {
            'stars': 4,
            'review_text': 'New text',
            'book_id': book.id,
            'user_id': self.user.id
        }
        )

        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars, 4)
        self.assertEqual(br.review_text, 'New text')