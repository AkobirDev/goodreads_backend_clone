from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class RegistrationTestCases(TestCase):
    
    def test_user_is_created(self):
        self.client.post(
            reverse('users:register'),
            data = {
                'username': 'AkobirDev',
                'first_name': 'Akobir', 
                'last_name': 'Tursunov',
                'email': 'akobir@mail.ru',
                'password': 'somepassword',
            }
        )

        user = User.objects.get(username='AkobirDev')
        self.assertEqual(user.first_name, 'Akobir')
        self.assertEqual(user.last_name, 'Tursunov')
        self.assertEqual(user.email, 'akobir@mail.ru')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))


    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data = {
                'first_name': 'Akobir',
                'last_name': 'Tursunov',
                'email': 'akobir@mail.ru'
            }
        )

        count = User.objects.count()
        self.assertEqual(count, 0)

        self.assertFormError(response, 'form', 'username', 'This field is required.' )
        self.assertFormError(response, 'form', 'password', 'This field is required.' )

    
    def test_email_is_valid(self):
        response = self.client.post(
            reverse('users:register'),
            data = {
                'username': 'AkobirDev',
                'first_name': 'Akobir', 
                'last_name': 'Tursunov',
                'email': 'akobir-mail.ru',
                'password': 'somepassword',
            }
        )

        count = User.objects.count()
        self.assertEqual(count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    
    def test_unique_username(self):
        user = User.objects.create(username='AkobirDev', first_name='Akobir')
        user.set_password('somepassword')
        user.save()
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'AkobirDev'
            }
        )

        count = User.objects.count()
        self.assertEqual(count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
