import sys
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(request=None, email=None, password=None, **kwargs):
        try:
            # print(request)
            # print(uid)
            # uid = request.GET.get('token')
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        return user


    def get_user(self, email):
        try:
            print(email)
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
