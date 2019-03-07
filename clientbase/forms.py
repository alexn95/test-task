from django import forms
from django.forms import ModelForm, DateField, Form

from clientbase.enums import OrderBy
from .models import Client
from app import settings


class ClientForm(ModelForm):
    """
    Form for create a new client
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


class ClientListForm(Form):
    """
    Client list form
    """
    query_string = forms.CharField(required=False, initial='')
    page = forms.IntegerField(required=False, initial=None)
    order_by = forms.ChoiceField(choices=[x.value for x in OrderBy],
                                 required=False)
