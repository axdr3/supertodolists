from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer


@api_view(['POST', ])
def registration_view(request):
	serializer = RegistrationSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		user = serializer.save()
		data['response'] = "Successfully registered new user"
		data['email'] = user.email
		data['first_name'] = user.first_name
		data['last_name'] = user.last_name
	else:
		data = serializer.errors
	return Response(data)
