"""
Module contain celery app forms
"""

import json
import os

from django import forms
from django.conf import settings

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .models import ProductData


class ProductDataAdminForm(forms.ModelForm):
    """
    Upload product data form
    """
    class Meta:
        model = ProductData
        fields = ('data_file',)

    def clean(self):
        """
        Check that json data is valid
        :return: valid data
        """
        cleaned_data = self.cleaned_data

        data_file = cleaned_data.get('data_file')
        data = data_file.read()

        try:
            json_data = json.loads(data)
            validate(instance=json_data,
                     schema=settings.PRODUCT_DATA_JSON_SCHEMA)
        except ValueError as er:
            raise forms.ValidationError(er)
        except ValidationError as er:
            raise forms.ValidationError(er)

        return cleaned_data
