from django.urls import path, re_path
from .views import login_view, logout_view, signup, send_signup_email

app_name = 'accounts'

urlpatterns = [
	re_path(r'^login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('signup/', signup, name='signup'),
	path('send_signup_email/', send_signup_email, name='send_signup_email' )
]
