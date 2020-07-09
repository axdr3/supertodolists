from django import forms
# from managers import CustomUserManager
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
User = get_user_model()

ERR_PASS_MATCH = 'Passwords must match.'
ERR_EMAIL_EXISTS = 'Email is already registered.'
ERR_WRONG_PASS_EMAIL = 'Email or password is incorrect.'


# class SignupForm(forms.models.ModelForm):

# 	password2 = forms.CharField(widget=forms.PasswordInput)

# 	def clean(self):
# 		cleaned_data = super().clean()
# 		email = cleaned_data.get('email')
# 		password = cleaned_data.get('password')
# 		password2 = cleaned_data.get('password2')

# 		if password != password2:
# 			raise ValidationError({'password': ERR_PASS_MATCH})

# 		try:
# 			User.objects.all().get(email=email)
# 			raise ValidationError({'email': ERR_EMAIL_EXISTS})
# 		except User.DoesNotExist:
# 			# self.cleaned_data = cleaned_data
# 			return cleaned_data

# 	def save(self):
# 		# saved = super(LoginForm, self).save()
# 		# cleaned_data = self.clean()
# 		# self.is_valid()
# 		user = User.objects.create_user(
# 			self.cleaned_data.get('email'),
# 			self.cleaned_data.get('password')
# 		)
# 		return user

# 	class Meta:
# 		model = User
# 		fields = ['email', 'password', 'password2']

# class LoginForm(forms.models.ModelForm):

# 	def clean(self):
# 		cleaned_data = super().clean()
# 		email = cleaned_data.get('email')
# 		# print(email)
# 		password = cleaned_data.get('password')
# 		if authenticate(email=email, password=password):
# 			print(self.errors)
# 			return cleaned_data
# 		else:
# 			print('a')
# 			raise ValidationError({'email': ERR_WRONG_PASS_EMAIL})

# 	def save(self):
# 		# self.is_valid()
# 		user = User.objects.get(email=self.cleaned_data['email'])
# 		print(f'passei {user}')
# 		return user

# 	class Meta:
# 		model = User
# 		fields = ['email', 'password']