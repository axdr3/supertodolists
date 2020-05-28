from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token
from unittest.mock import patch, call
import accounts.views


class SendLoginEmailViewTest(TestCase):

	def test_redirects_to_home_page(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		self.assertRedirects(response, '/')

	def test_creates_token_associated_with_email(self):
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		token = Token.objects.first()
		self.assertEqual(token.email, 'edith@example.com')

	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})

		token = Token.objects.first()
		expected_url = f'http://testserver/accounts/login?token={token.uid}'
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)

	# The patch decorator takes a dot-notation name of an object to monkeypatch. That’s the equivalent of
	# manually replacing the send_mail in accounts.views. The advantage of the decorator is that,
	# firstly, it automatically replaces the target with a mock. And secondly, it automatically puts the
	# original object back at the end! (Otherwise, the object stays monkeypatched for the rest of the
	# test run, which might cause problems in other tests.)
	@patch('accounts.views.send_mail')

	# patch then injects the mocked object into the test as an argument to the test method. We can
	# choose whatever name we want for it, but I usually use a convention of mock_ plus the original
	# name of the object.
	def test_sends_mail_to_address_from_post(self, mock_send_mail):

		self.client.post('/accounts/send_login_email', data={
			# We call our function under test as usual, but everything inside this test method has our mock
			# applied to it, so the view won’t call the real send_mail object; it’ll be seeing mock_send_mail
			# instead.
			'email': 'edith@example.com'
		})

		# And we can now make assertions about what happened to that mock object during the test. We can see
		# it was called…​
		self.assertTrue(mock_send_mail.called)
		# …​and we can also unpack its various positional and keyword call arguments, and examine what it was called with.
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertEqual(subject, 'Your login link for Supertodolists')
		self.assertEqual(from_email, 'noreply@supertodolists')
		self.assertEqual(to_list, ['edith@example.com'])

	def test_adds_success_message(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		}, follow=True)

		message = list(response.context['messages'])[0]
		self.assertEqual(
			message.message,
			"Check your email, we've sent you a link you can use to log in."
		)
		self.assertEqual(message.tags, "success")


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

	def test_redirects_to_home_page(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')
		print(response)
		self.assertRedirects(response, '/')

	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')

		# We check that it’s called with the request object that the view sees, and
		# the "user" object that the authenticate function returns. Because
		# authenticate is also mocked out, we can use its special "return_value"
		# attribute.
		self.assertEqual(
			mock_auth.login.call_args,
			call(response.wsgi_request, mock_auth.authenticate.return_value)
		)

	# We expect to be using the django.contrib.auth module in views.py, and we mock it out here.
    # Note that this time, we’re not mocking out a function, we’re mocking out a whole module, and
    # thus implicitly mocking out all the functions (and any other objects) that module contains.
    # As usual, the mocked object is injected into our test method.
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):

		# This time, we’ve mocked out a module rather than a function. So we examine the
		# call_args not of the mock_auth module, but of the mock_auth.authenticate function. Because all the
		# attributes of a mock are more mocks, that’s a mock too. You can start to see why Mock objects are so
		# convenient, compared to trying to build your own.
		#
		# Now, instead of "unpacking" the call args, we use the call function
		# for a neater way of saying what it should have been called with—​that
		# is, the token from the GET request.
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(request=None, uid='abcd123')
		)

	def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
		mock_auth.authenticate.return_value = None
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(mock_auth.login.called, False)
