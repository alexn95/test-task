from rest_framework import serializers

from clientbase.models import Client


class ClientPhotoSerializer(serializers.ModelSerializer):
    """
    Client serializer for photo page
    """
    class Meta:
        model = Client
        fields = ('id', 'photo', 'likes')
