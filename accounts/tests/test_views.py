from unittest.mock import Mock
from django.test import TestCase, Client
from unittest.mock import patch, call
from django.http import HttpRequest
from django.core import mail
import accounts.views
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.views import signup, login_view, logout_view, activate_account
import string
import re
# import unittest.skip

@patch('accounts.views.forms.SignupForm')
# @patch('accounts.mode')
# @patch('accounts.views.SignupForm.save')
class SignupViewTest(TestCase):

	def setUp(self):
		self.request = HttpRequest()
		# self.request.user = AnonymousUser()
		self.request.user = None
		data = {
				'email': 'ola@alo.com',
				'password': 'aloc666123',
				'password2': 'aloc666123',
		}
		self.request.method = 'POST'
		self.request.POST = data
		middleware = SessionMiddleware()
		middleware.process_request(self.request)
		self.request.session.save()
		middleware = MessageMiddleware()
		middleware.process_request(self.request)
		self.request.session.save()
		self.request.META['HTTP_HOST'] = '127.0.0.1'

	def test_redirects_to_home_page(self, mock_form):

		response = signup(self.request)
		response.client = Client()
		self.assertRedirects(response, '/')

	@patch('accounts.views.render')
	def test_renders_correct_html(self, mock_render, mock_form):
		self.request.method = 'GET'
		mock_a_form = mock_form.return_value
		signup(self.request)
		# response.client = Client()
		mock_render.assert_called_once_with(self.request, 'accounts/signup.html', {'form': mock_a_form})
		# self.assertTemplateUsed(response, '/accounts/signup.html')

	def test_signup_POST_sent_to_form(self, mock_form):

		mock_a_form = mock_form.return_value
		mock_a_form.is_valid.return_value = True
		# mock_a_form(data=self.request.POST)
		signup(self.request)
		mock_form.assert_called_once_with(data=self.request.POST)

	def test_saves_user_after_save_method(self, mock_form):
		mock_a_form = mock_form.return_value
		signup(self.request)
		mock_a_form.save.assert_called_once()

	def test_doesnot_save_if_form_invalid(self, mock_form):
		mock_a_form = mock_form.return_value
		mock_a_form.is_valid.return_value = False
		signup(self.request)
		self.assertFalse(mock_a_form.save.called)

	def test_confirmation_email_is_sent(self, mock_form):
		mock_a_form = mock_form.return_value
		mock_a_form.is_valid.return_value = True
		mock_a_form.save.return_value = Mock(data=self.request.POST)
		mock_user = mock_a_form.save.return_value
		signup(self.request)
		email = mail.outbox[0]
		self.assertIn(mock_user.email, email.to)
		self.assertEqual(email.subject, 'Activate Your Supertodolists Account')


@patch('accounts.views.auth')
@patch('accounts.views.forms.LoginForm')
class LoginViewTest(TestCase):
	def setUp(self):
		self.request = HttpRequest()
		# self.request.user = AnonymousUser()
		self.request.user = None
		data = {
				'email': 'ola@alo.com',
				'password': 'aloc666123',
		}
		self.request.POST = data
		middleware = SessionMiddleware()
		middleware.process_request(self.request)
		self.request.session.save()
		middleware = MessageMiddleware()
		middleware.process_request(self.request)
		self.request.session.save()

	def test_redirects_to_home_page(self, mock_login, mock_auth):
		self.request.method = 'POST'
		mock_auth.authenticate.return_value = True
		mock_a_login = mock_login.return_value
		mock_a_login.is_valid.return_value = True
		response = login_view(self.request)
		response.client = Client()
		self.assertRedirects(response, '/')

	@patch('accounts.views.render')
	def test_renders_correct_html(self, mock_render, mock_login, mock_auth):
		self.request.method = 'GET'
		mock_a_login = mock_login.return_value
		login_view(self.request)
		# response.client = Client()
		mock_render.assert_called_once_with(self.request, 'accounts/login.html', {'form': mock_a_login})

	def test_calls_auth_login_with_user_if_there_is_one(self, mock_login, mock_auth):
		self.request.method = 'POST'
		mock_a_login = mock_login.return_value
		mock_a_login.is_valid.return_value = True
		login_view(self.request)
		mock_auth.login.assert_called_once()

	def test_doesnt_login_if_loginform_not_valid(self, mock_login, mock_auth):
		self.request.method = 'POST'
		mock_a_login = mock_login.return_value
		mock_a_login.is_valid.return_value = False
		login_view(self.request)
		mock_auth.login.assert_not_called()

	def test_redirect_homepage_if_already_loggedin(self, mock_login, mock_auth):
		self.request.method = 'POST'
		self.request.user = Mock()
		self.request.user(data=self.request.POST)
		self.assertTrue(self.request.user.is_authenticated())
		response = login_view(self.request)
		response.client = Client()
		self.assertRedirects(response, '/')

	def test_logout(self, mock_login, mock_auth):
		self.request.method = 'POST'
		self.request.user = Mock(data=self.request.POST)
		self.assertTrue(self.request.user.is_authenticated())
		mock_auth.logout.return_value = True
		# self.request.user = None
		logout_view(self.request)
		self.assertTrue(mock_auth.logout.return_value)

	# def test_doesnt_login_if_not_email_activated(self, mock_login, mock_auth):
	# 	self.request.method = 'POST'
	# 	# self.request.user = Mock()
	# 	response = login_view(self.request)
	# 	response.client = Client()



class ActivateAccTest(TestCase):

	def test_email_sent(self):
		password = 'abcdegfd'
		email = 'example@gmail.com'
		self.client.post(
			'/accounts/signup/',
			data={'email': 'example@email.com', 'password': password, 'password2': password},
			follow=True
		)
		# self.assertTemplateUsed()
		print(mail.outbox[0].from_email)
		self.assertIn('Please click on the link below to confirm your registration:', mail.outbox[0].body)

	def test_user_is_authenticated_after_activation(self):
		password = 'abcdegfd'
		email = 'example@gmail.com'
		self.client.post(
			'/accounts/signup/',
			data={'email': 'example@email.com', 'password': password, 'password2': password},
			follow=True
		)
		email_body = mail.outbox[0].body
		# res = re.sub('['+string.punctuation+']', '', email_body).split()
		res = email_body.split()
		count = len(res)
		res = res[count-1]
		response = self.client.get(res, follow=True)
		self.assertTrue(response.context['user'].is_authenticated)
		# print()

	def test_doesnt_login_if_not_email_activated(self):
		password = 'abcdegfd'
		email = 'example@gmail.com'
		self.client.post(
			'/accounts/signup/',
			data={'email': 'example@email.com', 'password': password, 'password2': password},
			follow=True
		)
		response = self.client.get('/accounts/login', data={'email': email, 'password': password}, follow=True)
		self.assertFalse(response.context['user'].is_authenticated)
		print(response.context['user'])
