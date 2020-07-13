from django.test import TestCase
from django.contrib import auth

User = auth.get_user_model()


class UserModelTest(TestCase):

	def test_user_is_valid_with_email_and_pass(self):
		user = User(email='a@b.com', password='abcdefghjkl')
		user.full_clean()  # should not raise


	def test_no_problem_with_auth_login(self):
		user = User.objects.create(email='edith@example.com')
		user.backend = ''
		request = self.client.request().wsgi_request
		auth.login(request, user)  # should not raise

	def test_create_user(self):
		# User = get_user_model()
		user = User.objects.create_user(email='normal@user.com', password='foo')
		self.assertEqual(user.email, 'normal@user.com')
		# self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)
		try:
			# username is None for the AbstractUser option
			# username does not exist for the AbstractBaseUser option
			self.assertIsNone(user.username)
		except AttributeError:
			pass
		with self.assertRaises(TypeError):
			User.objects.create_user()
		with self.assertRaises(TypeError):
			User.objects.create_user(email='')
		with self.assertRaises(ValueError):
			User.objects.create_user(email='', password="foo")

	def test_uuid_is_pk(self):
		user = User.objects.create_user(email='normal@user.com', password='foo')
		self.assertEqual(user.id, user.pk)

	def test_email_confirmation_and_is_active_are_False(self):
		user = User(email='normal@user.com', password='foo')
		user.save()
		self.assertFalse(user.email_confirmed)
		self.assertFalse(user.is_active)


