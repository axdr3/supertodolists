from django.urls import path, re_path
from .views import send_login_email, login

urlpatterns = [
	path('send_login_email', send_login_email, name='send_login_email'),
	re_path(r'^login', login, name='login')
]
