from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.contrib import auth
from accounts.authentication import CustomAuthenticationBackend
from unittest.mock import patch, call
from django.http import HttpRequest
User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_password(self):
        password = 'abcdefghjkl'
        User.objects.create_user(email='example@email.com', password=password)
        result = CustomAuthenticationBackend.authenticate(email='example@email.com')
        self.assertIsNone(result)

    def test_returns_user_if_password_good(self):
        password = 'abcdefghjkl'
        user = User.objects.create_user(email='example@email.com', password=password)
        result = CustomAuthenticationBackend.authenticate(email='example@email.com', password=password)
        self.assertEqual(result, user)

    def test_user_is_authenticated_after_login(self):
        password = 'abcdefghjkl'
        print(User.objects.all())
        user = User.objects.create_user(email='example@email.com', password=password)
        # user.is_active = True
        request = HttpRequest()
        # request.method = 'POST'
        # request.user = user
        response = self.client.post('/accounts/login/', data={'email': 'example@email.com', 'password': password}, follow=True)
        print(response.context['user'])
    # def test_returns_None_if_no_such_token(self):
    #     result = PasswordlessAuthenticationBackend().authenticate(
    #         'no-such-token'
    #     )
    #     self.assertIsNone(result)

    # def test_returns_new_user_with_correct_email_if_token_exists(self):
    #     email = 'edith@example.com'
    #     token = Token.objects.create(email=email)
    #     user = PasswordlessAuthenticationBackend().authenticate(None, uid=token.uid)
    #     new_user = User.objects.get(email=email)
    #     self.assertEqual(user, new_user)

    # def test_returns_existing_user_with_correct_email_if_token_exists(self):
    #     email = 'edith@example.com'
    #     existing_user = User.objects.create(email=email)
    #     token = Token.objects.create(email=email)
    #     user = PasswordlessAuthenticationBackend().authenticate(None, uid=token.uid)
    #     self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = CustomAuthenticationBackend().get_user(
            'edith@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            CustomAuthenticationBackend().get_user('edith@example.com')
        )
