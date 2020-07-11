from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand
User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email, password):
    user = User.objects.create_user(email=email, password=password)
    # user.save()
    print(user.pk)
    session = SessionStore()
    session[SESSION_KEY] = str(user.pk)
    print(session[SESSION_KEY])
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key
