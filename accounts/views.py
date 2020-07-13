from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from .authentication import CustomAuthenticationBackend
from django.urls import reverse
from django.template.loader import get_template
from . import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

User = auth.get_user_model()

def activate_account(request, uidb64, token):
	if request.method == 'GET':
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			# user.is_active = True
			user.email_confirmed = True
			user.save()
			auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, ('Your account have been confirmed.'))
			return redirect('/')
		else:
			messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return redirect('/')

def signup(request):
	# form = forms.SignupForm()
	if request.method == 'POST':
		form = forms.SignupForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(
				request,
				"You will be mailed a confirmation link to your email soon."
			)
			current_site = get_current_site(request)
			subject = 'Activate Your Supertodolists Account'
			message = render_to_string('accounts/activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			send_mail(
				subject,
				message,
				'axdr3test@gmail.com',
				[user.email],
			)
			return redirect('/')
		else:
			render(request, 'accounts/signup.html', {'form': form})
	return render(request, 'accounts/signup.html', {'form': forms.SignupForm()})

def login_view(request):
	# form = forms.LoginForm()

	if request.method == 'POST':
		form = forms.LoginForm(request=request, data=request.POST)
		# print(form)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			user = auth.authenticate(
					request,
				 	email=email,
				 	password=form.cleaned_data.get('password')
					)
			auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(
				request,
				f'You are now logged in as {email}'
			)
			return redirect('/')
		else:
			return render(request, 'accounts/login.html', {'form': form})

	return render(request, 'accounts/login.html', {'form': forms.LoginForm()})

def logout_view(request):
	auth.logout(request)
	return redirect('/')
