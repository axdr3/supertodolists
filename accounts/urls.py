from django.urls import path, re_path
from .views import send_login_email, login, logout_view, signup

urlpatterns = [
	path('send_login_email', send_login_email, name='send_login_email'),
	re_path(r'^login', login, name='login'),
	path('logout', logout_view, name='logout'),
	path('signup', signup, name='signup')
]
