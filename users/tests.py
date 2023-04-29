from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthTokenTest(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@test.com'
        )

    def test_auth_token(self):
        response = self.client.post(
            self.url, {'username': 'test@test.com', 'password': 'testpassword'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertIsNotNone(response.data['token'])

    def test_auth_token_bad_credentials(self):
        response = self.client.post(
            self.url, {'username': 'testuser', 'password': 'badpassword'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.user_data = {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpassword'}

    def test_register_user(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'test@test.com')

    def test_register_user_bad_data(self):
        bad_data = {'username': 'testuser', 'email': 'bademail', 'password': 'testpassword'}
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTest(APITestCase):
    def setUp(self):
        self.url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout_user(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)


class OrderViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('my-order-list')

    def test_order_view_authenticated(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
