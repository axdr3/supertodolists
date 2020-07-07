from django.test import TestCase
from django.contrib import auth
from unittest.mock import patch, call
from accounts.forms import (
	SignupForm, LoginForm,
	ERR_PASS_MATCH, ERR_EMAIL_EXISTS, ERR_WRONG_PASS_EMAIL
	)
from accounts.models import CustomUser
User = auth.get_user_model()
# patch('accounts.forms.SignupForm.is_valid')
class SignupFormTest(TestCase):

	def test_dont_validate_diff_passwords(self):
		password = 'ahahaha'
		form = SignupForm(data={'email': 'a@b.com', 'password': password, 'password2': password + 'a'})
		self.assertEqual(
			form.errors['password'][0],
			ERR_PASS_MATCH
		)

	def test_dont_validate_duplicate_email(self):
		User.objects.create_user(email='a@b.com', password='aloc')
		form = SignupForm(data={'email': 'a@b.com', 'password': 'aloc', 'password2': 'aloc'})
		self.assertEqual(
			form.errors['email'][0],
			ERR_EMAIL_EXISTS
		)

	def test_able_to_signup(self):
		form = SignupForm(data={'email': 'a@b.com', 'password': 'aloc', 'password2': 'aloc'})
		# print(form)
		user = form.save()
		self.assertIn(user, User.objects.all())



class LoginFormTest(TestCase):

	def test_wrong_password_or_email(self):
		User.objects.create_user(email='a@b.com', password='aloc')
		form = LoginForm(data={'email': 'a@b.com', 'password': 'alocc'})
		self.assertEqual(
			form.errors['password'][0],
			ERR_WRONG_PASS_EMAIL
		)
		form = LoginForm(data={'email': 'a@be.com', 'password': 'aloc'})
		self.assertEqual(
			form.errors['email'][0],
			ERR_WRONG_PASS_EMAIL
		)

	# def test_user_is_authenticated_after_form_completion(self):
	# 	user = User.objects.create_user(email='a@b.com', password='aloc')
	# 	form = LoginForm(data={'email': 'a@b.com', 'password': 'alocc'})
	# 	self.client.get()
	# 	self.assertTrue()