from django import forms
# from managers import CustomUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
User = get_user_model()

ERR_PASS_MATCH = 'Passwords must match.'
ERR_EMAIL_EXISTS = 'Email is already registered.'
ERR_WRONG_PASS_EMAIL = 'Email or password is incorrect.'


class SignupForm(forms.models.ModelForm):

	password2 = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'password', 'password2']

	def clean(self):
		cleaned_data = super(SignupForm, self).clean()
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')

		if password != password2:
			raise ValidationError({'password': ERR_PASS_MATCH})

		try:
			User.objects.all().get(email=email)
			raise ValidationError({'email': ERR_EMAIL_EXISTS})
		except User.DoesNotExist:
			# self.cleaned_data = cleaned_data
			return cleaned_data

	def save(self):
		# saved = super(LoginForm, self).save()
		# cleaned_data = self.clean()
		self.is_valid()
		user = User.objects.create_user(
			self.cleaned_data.get('email'),
			self.cleaned_data.get('password')
		)
		return user

class LoginForm(forms.models.ModelForm):

	class Meta:
		model = User
		fields = ['email', 'password']

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')

		try:
			user = User.objects.all().get(email=email)
		except User.DoesNotExist:
			raise ValidationError({'email': ERR_WRONG_PASS_EMAIL})

		if authenticate(email=email, password=password):
			return cleaned_data

		raise ValidationError({'password': ERR_WRONG_PASS_EMAIL})
