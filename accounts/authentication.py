import sys
from  django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            # print(request)
            # print(uid)
            # uid = request.GET.get('token')
            user = User.objects.all().get(email=email)
            if not check_password(password, user.password):
                print('no matching passwords : authenticate')
                return None
        except User.DoesNotExist:
            print('user nao existe: authenticate')

            return None

        print(f'user{user.email} pass{user.password}')
        return user


    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
