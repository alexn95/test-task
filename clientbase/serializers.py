from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers

from clientbase.models import Client


class ClientPhotoSerializer(serializers.ModelSerializer):
    """
    Client serializer for photo page
    """
    class Meta:
        model = Client
        fields = ('id', 'photo', 'likes')


class AuthenticateSerializer(serializers.Serializer):
    """
    User serializer for login api
    """
    login = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, data):
        """
        Check that user with credentials exist
        """
        user = authenticate(username=data['login'], password=data['password'])
        if not user:
            raise ValidationError(message='Invalid login or password')
        return user
