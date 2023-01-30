from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user

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

        user = CustomUser.objects.get(username='AkobirDev')
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

        count = CustomUser.objects.count()
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

        count = CustomUser.objects.count()
        self.assertEqual(count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    
    def test_unique_username(self):
        user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir')
        user.set_password('somepassword')
        user.save()
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'AkobirDev'
            }
        )

        count = CustomUser.objects.count()
        self.assertEqual(count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCases(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username = 'AkobirDev', first_name = 'Akobir')
        self.db_user.set_password('somepass')
        self.db_user.save()

        return super().setUp()


    def test_successfull_login(self):
        self.client.post(
            reverse('users:login'),
            data = {
               'username': 'AkobirDev',
               'password': 'somepass'     
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)


    def test_wrong_login(self):
        self.client.post(
            reverse('users:login'),
            data = {
               'username': 'wrong-username',
               'password': 'somepass'     
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        

        self.client.post(
            reverse('users:login'),
            data = {
               'username': 'AkobirDev',
               'password': 'wrong-password'     
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        self.client.login(username='AkobirDev', password='somepass')
        self.client.get(reverse('users:logout'))
        
        user = get_user(self.client)
        # response = self.client.get(reverse('users:logout'))


        self.assertFalse(user.is_authenticated)


class ProfileTestCases(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.url, reverse('users:login'))

    def test_profile_details(self):
        user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir', last_name='Tursunov', email='akobir@mail.com')
        user.set_password('somepass')
        user.save()

        self.client.login(username='AkobirDev', password='somepass')
        
        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_change_profile(self):
        user = CustomUser.objects.create(username='AkobirDev', first_name='Akobir', last_name='Tursunov', email='akobir@mail.com')
        user.set_password('somepass')
        user.save()

        self.client.login(username='AkobirDev', password='somepass')

        response = self.client.post(
            reverse('users:profile_edit'),
            data = {
                'username': 'AkobirDev',
                'first_name': 'Akobir3',
                'last_name': 'Tursunov',
                'email': 'akobir@mail.commmm',
                
            }
        )
        user = CustomUser.objects.get(pk = user.pk)
        self.assertEqual(user.first_name, 'Akobir3')
        self.assertEqual(user.email, 'akobir@mail.commmm')
        self.assertEqual(response.url, reverse('users:profile'))
