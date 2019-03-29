"""
Module contain test cases of models
"""

import os

from django.conf import settings
from django.test import TestCase

from ..models import ProductData


class ModelsTestCase(TestCase):
    """
    Test cases of ProductData model
    """
    def setUp(self):
        self.product_data_1 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_1.json'
        )
        self.product_data_2 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_2.json'
        )
        self.product_data_3 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_3.json'
        )
        self.product_data_4 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_4.json'
        )
        self.product_data_5 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_5.json'
        )
        self.product_data_6 = ProductData.objects.create(
            data_file=settings.PRODUCT_DATA_DIR + '/tests/test_data_6.json'
        )

    def test_get_json_data(self):
        """
        Test that get_json_data return correct json data
        """
        json_data = self.product_data_1.get_json_data()
        self.assertIsNotNone(json_data)
        self.assertTrue(len(json_data) == 2)
        self.assertEqual(json_data[0]['shop'], 'DNS')
        self.assertEqual(json_data[1]['shop'], 'Technopoint')

    def test_get_json_data_by_id_list(self):
        """
        Test that json_data_by_id_list return correct list of json data
        according the input id list.
        """
        json_data = ProductData.objects.get_json_data_by_id_list(
            [self.product_data_1.id, self.product_data_2.id]
        )
        self.assertIsNotNone(json_data)
        self.assertTrue(len(json_data) == 4)
        self.assertEqual(json_data[0]['shop'], 'DNS')
        self.assertEqual(json_data[1]['shop'], 'Technopoint')
        self.assertEqual(json_data[2]['shop'], 'DNS')
        self.assertEqual(json_data[3]['shop'], 'Technopoint')

    def test_collect_product_data(self):
        """
        Test that collect_product_data work correctly
        """
        collect_product_id = ProductData.objects.collect_product_data(
            [self.product_data_1.id, self.product_data_2.id]
        )
        self.assertIsNotNone(collect_product_id)
        self.collect_product_object = ProductData.objects.get(
            id=collect_product_id)
        self.assertIsNotNone(self.collect_product_object)
        self.assertEqual(len(self.collect_product_object.get_json_data()), 4)

        # Remove json file
        remove_file_if_exist(self.collect_product_object.data_file.name)

    def test_remove_repetitions(self):
        """
        Test that remove_repetitions work correctly
        """
        self.product_data_3.remove_repetitions()
        self.product_data_3 = ProductData.objects.get(
            id=self.product_data_3.id)
        self.assertIsNotNone(self.product_data_3)
        json_data = self.product_data_3.get_json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 4)
        self.assertEqual(json_data[0]['price'], 500)

        # Remove json file
        remove_file_if_exist(self.product_data_3.data_file.name)

    def test_write_cheap_products(self):
        """
        Test that write_cheap_products work correctly
        """
        self.product_data_4.write_cheap_products()
        self.product_data_4 = ProductData.objects.get(
            id=self.product_data_4.id)
        self.assertIsNotNone(self.product_data_4)
        json_data = self.product_data_4.get_json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0], 2)
        self.assertEqual(json_data[1], 5)

        # Remove json file
        remove_file_if_exist(self.product_data_4.data_file.name)

    def test_write_product_avr_prices_list(self):
        """
        Test that write_product_avr_list work correctly
        """
        self.product_data_5.write_product_avr_prices_list()
        self.product_data_5 = ProductData.objects.get(
            id=self.product_data_5.id)
        self.assertIsNotNone(self.product_data_5)
        json_data = self.product_data_5.get_json_data()

        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data['1']['DNS'], 300)
        self.assertEqual(json_data['1']['Technopoint'], 400)
        self.assertEqual(json_data['2']['DNS'], 100)
        self.assertEqual(json_data['2']['Technopoint'], 500)

        # Remove json file
        remove_file_if_exist(self.product_data_5.data_file.name)

    def test_write_analog_list_of_product_list(self):
        """
        Test that write_analog_list_of_product_list work correctly
        """
        self.product_data_6.write_analog_list_of_product_list()
        self.product_data_6 = ProductData.objects.get(
            id=self.product_data_6.id)
        self.assertIsNotNone(self.product_data_6)
        json_data = self.product_data_6.get_json_data()

        self.assertIsNotNone(json_data)
        self.assertEqual(json_data['1'], [3])
        self.assertEqual(json_data['3'], [1])
        self.assertEqual(json_data['4'], [1, 5])
        self.assertEqual(json_data['5'], [1, 4])

    def tearDown(self):
        pass


def remove_file_if_exist(file):
    """
    Remove media file if file exist in this path
    :param file: particle file path
    """
    path = os.path.join(settings.MEDIA_ROOT, file)
    if file and os.path.exists(path):
        os.remove(path)
