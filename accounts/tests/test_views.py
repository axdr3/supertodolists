from unittest.mock import Mock
from django.test import TestCase, Client
from unittest.mock import patch, call
from django.http import HttpRequest
import accounts.views
from accounts.views import signup, login_view, logout_view
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


	def test_redirects_to_home_page(self, mock_form):

		response = signup(self.request)
		response.client = Client()
		self.assertRedirects(response, '/')

	@patch('accounts.views.render')
	def test_renders_correct_html(self, mock_render, mock_form):
		self.request.method = 'GET'
		mock_a_form = mock_form.return_value
		response = signup(self.request)
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
		response = login_view(self.request)
		# response.client = Client()
		mock_render.assert_called_once_with(self.request, 'accounts/login.html', {'form': mock_a_login})


	def test_calls_auth_login_with_user_if_there_is_one(self, mock_login, mock_auth):
		self.request.method = 'POST'
		mock_a_login = mock_login.return_value
		mock_a_login.is_valid.return_value = True
		response = login_view(self.request)
		mock_auth.login.assert_called_once()

	def test_doesnt_login_if_loginform_not_valid(self, mock_login, mock_auth):
		self.request.method = 'POST'
		mock_a_login = mock_login.return_value
		mock_a_login.is_valid.return_value = False
		response = login_view(self.request)
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
