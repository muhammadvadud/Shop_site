from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class SignupTestCase(TestCase):
    def test_signup_view(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'first_name': 'adminjon',
                'username': 'adminjon',
                'email': 'admin@gmail.com',
                'password1': '4B5-ajq-cHt-wyX',
                'password2': '4B5-ajq-cHt-wyX',
            }
        )
        user = CustomUser.objects.get(username='adminjon')
        self.assertEqual(user.first_name, 'adminjon')
        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertTrue(user.check_password('4B5-ajq-cHt-wyX'))

        second_response = self.client.get('/users/profile/')

        self.assertEqual(second_response.status_code, 200)

        # login
        self.client.login(username='adminjon', password='4B5-ajq-cHt-wyX')

        third_response = self.client.post(
            reverse('users:profile'),
            data={
                'username': 'adminjon2',
                'first_name': 'adminjon2',
                'last_name': 'adminaliyev',
                'email': 'admin@hmail.com',
                'phone_nubmer': '+998940105669',
                'tg_username': 'username',
            }
        )
        user = get_user(self.client)
        print(user.is_authenticated)
        self.assertEqual(user.phone_nubmer, '+998940105669')
        self.assertEqual(user.first_name, 'adminjon2')
        self.assertNotEquals(user.first_name, 'adminjon')
        self.assertEqual(third_response.status_code, 302)
