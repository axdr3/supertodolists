from django.urls import re_path
from lists import api

urlpatterns = [
    re_path(r'^lists/(\d+)/$', api.list, name='api_list'),
]
