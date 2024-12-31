from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from authentications.models import Account
from authentications.modules.account import (authenticate, refresh, logout)
from authentications.modules.token import validate_refresh_token
from utilities.exceptions import MultiLanguageException


class TestFeeds(TestCase):
    """Test cases for the functions related to authentication."""

    fixtures = ['account.json']

    @classmethod
    def setUpClass(cls):
        """Set up common fixture data for all test cases."""
        cls.fixture_email = 'marzie.7900@gmail.com'
        cls.fixture_password = '456fghj^$J'
        cls.user_data = {
            'email': cls.fixture_email,
            'password': cls.fixture_password
        }
        super().setUpClass()

    def test_sign_in_green(self):
        """Test successful user authentication."""
        authenticate(self.fixture_email, self.fixture_password)
        tokens = authenticate(self.fixture_email, self.fixture_password)

        self.assertEqual(['access_token', 'refresh_token'],
                         list(tokens.keys()))

    def test_sign_in_red(self):
        """Test authentication failure with incorrect password."""
        authenticate(self.fixture_email, self.fixture_password)

        with self.assertRaises(MultiLanguageException):
            authenticate(self.fixture_email, self.fixture_password[:1])

    def test_refresh_green(self):
        """Test successful token refresh."""
        tokens = authenticate(self.fixture_email, self.fixture_password)

        new_tokens = refresh(tokens['refresh_token'])

        self.assertNotEqual(tokens['access_token'], new_tokens['access_token'])
        self.assertNotEqual(tokens['refresh_token'],
                            new_tokens['refresh_token'])

    def test_logout_green(self):
        """Test successful user logout and token invalidation."""
        tokens = authenticate(self.fixture_email, self.fixture_password)

        logout(tokens['refresh_token'])

        with self.assertRaises(MultiLanguageException):
            validate_refresh_token(tokens['refresh_token'])

    def test_register_user_green(self):
        """Test user registration."""
        response = self.client.post(reverse('authentication'), {
            'email': 'newuser@example.com',
            'password': 'Newpassword123.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_register_user_red(self):
        """Test user registration."""
        response = self.client.post(reverse('authentication'), {
            'email': 'newuser@example.com',
            'password': 'Newpass345678'
        })
        self.assertEqual(response.status_code,
                         status.HTTP_417_EXPECTATION_FAILED)

    def test_login_user_green(self):
        """Test user login."""
        response = self.client.post(reverse('authentication'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_refresh_token_green(self):
        """Test token refresh."""
        login_response = self.client.post(
            reverse('authentication'), self.user_data)
        refresh_token = login_response.data['refresh_token']
        response = self.client.post(reverse('token-refresh'), {
            'refresh_token': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_logout_user_green(self):
        """Test user logout."""
        login_response = self.client.post(
            reverse('authentication'), self.user_data)
        refresh_token = login_response.data['refresh_token']
        access_token = login_response.data['access_token']
        response = self.client.post(reverse('logout'), {
            'refresh_token': refresh_token
        },
            HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_force_delete_green(self):
        """Test force deletion of an account."""
        account = Account.objects.all().last()
        account_email = account.__str__()
        account.delete(force_delete=True)
        self.assertFalse(Account.all_objects.filter(
            email=account_email).exists())

    def test_account_soft_delete_green(self):
        """Test soft deletion of an account."""
        account = Account.objects.all().last()
        account_email = account.__str__()
        account.delete()
        self.assertTrue(Account.all_objects.filter(
            email=account_email).exists())
