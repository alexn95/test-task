from django import forms
from django.forms import ModelForm, DateField, Form

from .models import Client
from app import settings


class ClientForm(ModelForm):
    """
    Client form class
    """
    date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo')


class ClientPhotoForm(Form):
    """
    Client photo set like form
    """
    client_id = forms.IntegerField()
