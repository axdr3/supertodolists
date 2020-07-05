import sys
from accounts.models import User, Token
from django.contrib.auth.backends import ModelBackend


class PasswordAuthenticationBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            # print(request)
            # print(uid)
            # uid = request.GET.get('token')
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            print(email)
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
