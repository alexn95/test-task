"""
Module contain tests of form functionality
"""


from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app import settings
from clientbase.enums import OrderBy
from clientbase.forms import ClientPhotoForm, ClientListForm
from ..forms import ClientForm


class FormsTestCase(TestCase):
    """
    Test cases of application forms
    """
    def test_client_form(self):
        """
        Test create client form.
        Test create image object, positive validation form,
        negative validation form.
        """
        url = settings.MEDIA_ROOT + 'photo/test_photo.png'
        photo = SimpleUploadedFile(name='test_photo.png',
                                   content=open(url, 'rb').read(),
                                   content_type='image/png')

        form_data = {
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'date_of_birth': '24-02-1995',
            'photo': photo.name
        }
        form = ClientForm(form_data, {'photo': photo})
        self.assertTrue(form.is_valid())

        form_data = {
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'date_of_birth': '24441995',
            'photo': photo.name
        }
        form = ClientForm(form_data, {'photo': photo})
        self.assertFalse(form.is_valid())

        form = ClientForm({}, {'photo': photo})
        self.assertFalse(form.is_valid())

    def test_client_photo_form(self):
        """
        Test client photo form.
        Positive and negative validation form.
        """
        form_data = {
            'client_id': 1
        }
        form = ClientPhotoForm(form_data)
        self.assertTrue(form.is_valid())

        form = ClientForm({})
        self.assertFalse(form.is_valid())

    def test_client_list_form(self):
        """
        Test client list form.
        Positive and negative validation form.
        """
        form = ClientListForm({})
        self.assertTrue(form.is_valid())

        form_data = {
            'query_string': 'str',
            'page': 1,
            'order_by': OrderBy.fn.value[0],
        }
        form = ClientListForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'query_string': 'str',
        }
        form = ClientListForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'page': 1,
        }
        form = ClientListForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'order_by': OrderBy.fn.value[0],
        }
        form = ClientListForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'order_by': 1,
        }
        form = ClientListForm(form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'page': 'str',
        }
        form = ClientListForm(form_data)
        self.assertFalse(form.is_valid())
