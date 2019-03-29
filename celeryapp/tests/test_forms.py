"""
Module contain test cases of forms
"""

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from celeryapp.forms import ProductDataAdminForm


class FormsTestCase(TestCase):
    """
    Test cases of ProductData forms
    """
    def setUp(self):
        pass

    def test_product_data_admin_form(self):
        """
        Check that ProductDataAdminForm work correctly
        """
        file = upload_json_file('test_data_1.json')
        data = {
            'data_file': os.path.join(settings.TEST_DATA_FILE_DIR, file.name)
        }
        form = ProductDataAdminForm(data, {'data_file': file})
        self.assertTrue(form.is_valid())

        file = upload_json_file('test_data_2.json')
        data = {
            'data_file': os.path.join(settings.TEST_DATA_FILE_DIR, file.name)
        }
        form = ProductDataAdminForm(data, {'data_file': file})
        self.assertTrue(form.is_valid())

        file = upload_json_file('invalid_data_1.json')
        data = {
            'data_file': os.path.join(settings.TEST_DATA_FILE_DIR, file.name)
        }
        form = ProductDataAdminForm(data, {'data_file': file})
        self.assertFalse(form.is_valid())

        file = upload_json_file('invalid_data_2.json')
        data = {
            'data_file': os.path.join(settings.TEST_DATA_FILE_DIR, file.name)
        }
        form = ProductDataAdminForm(data, {'data_file': file})
        self.assertFalse(form.is_valid())

    def tearDown(self):
        pass


def upload_json_file(file_name):
    base_path = os.path.join(
        settings.MEDIA_ROOT,
        settings.PRODUCT_DATA_DIR
    )
    url = os.path.join(base_path, settings.TEST_DATA_FILE_DIR, file_name)
    file = SimpleUploadedFile(name=file_name,
                              content=open(url, 'rb').read(),
                              content_type='json')
    return file
