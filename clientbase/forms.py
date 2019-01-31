from django.forms import ModelForm, DateField

from app import settings
from clientbase.models import Client


class ClientForm(ModelForm):
    date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo')
