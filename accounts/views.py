from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
# from accounts.models import CustomUUID
from django.urls import reverse


def send_login_email(request):
	pass
# 	email = request.POST['email']
# 	uuid = CustomUUID.objects.create(email=email)
# 	url = request.build_absolute_uri(
# 		reverse('login') + '?CustomUUID=' + str(uuid.uid))
# 	message_body = f'Use this link to log in:\n\n{url}'
# 	send_mail(
# 		'Your login link for Supertodolists',
# 		message_body,
# 		'noreply@supertodolists',
# 		[email],
# 	)
# 	messages.success(
# 		request,
# 		"Check your email, we've sent you a link you can use to log in."
# 	)
# 	return redirect('/')


def login(request):
	user = auth.authenticate()
	if user:
		auth.login(request, user)
	return redirect('/')

def logout_view(request):
	auth.logout(request)
	return redirect('/')