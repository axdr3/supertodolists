# from django.urls import path, include
from django.contrib import auth
from django.contrib import admin
admin.autodiscover()
User = auth.get_user_model()
from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope



class RegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def save(self):
		user = User(
				email=self.validated_data['email'],
		)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match'})

		user.set_password(password)
		user.save()
		return user