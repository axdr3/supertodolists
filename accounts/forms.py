from django import forms
# from managers import CustomUserManager
from django.contrib.auth import get_user_model
from .authentication import CustomAuthenticationBackend
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
User = get_user_model()

ERR_PASS_MATCH = 'Passwords must match.'
ERR_EMAIL_EXISTS = 'Email is already registered.'
ERR_WRONG_PASS_EMAIL = 'Email or password is incorrect.'


class SignupForm(forms.models.ModelForm):

	# password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
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
		# self.is_valid()
		user = User.objects.create_user(
			self.cleaned_data.get('email'),
			self.cleaned_data.get('password')
		)
		return user

	class Meta:
		model = User
		fields = ['email', 'password', 'password2']

class LoginForm(forms.Form):

	email = forms.EmailField(label=_('Email Address'), max_length=50)
	password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, max_length=30)

	def __init__(self, request=None, *args, **kwargs):
		"""
		The 'request' parameter is set for custom auth use by subclasses.
		The form data comes in via the standard 'data' kwarg.
		"""
		self.request = request
		# self.user_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')
		if CustomAuthenticationBackend.authenticate(self, email=email, password=password):
			return cleaned_data
		else:
			raise ValidationError({'email': ERR_WRONG_PASS_EMAIL})

	def save(self):
		email = self.cleaned_data.get('email')
		user = User.objects.all().get(email=email)
		return user
