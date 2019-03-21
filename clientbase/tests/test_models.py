"""
Module contain tests of model functionality
"""

import datetime
from random import randint
from django.test import TestCase

from ..models import try_parsing_string_to_date, Client


class ClientTestCase(TestCase):
    """
    Test cases of client model
    """
    def setUp(self):
        self.client_id = randint(1, 100000)
        Client.objects.create(
            id=self.client_id,
            first_name='FirstName',
            last_name='LastName',
            date_of_birth='1995-02-24',
            photo='test_photo.png'
        )
        self.client = Client.objects.get(id=self.client_id)

    def test_get_clients_by_name(self):
        """
        Get created client by full query string,
        check if it is found and check her id
        Get created client by parts of one of name,
        check if it is found and check her id
        Get created client by parts of both names, check if it is found
        and check her id
        """
        query_set = Client.objects.get_clients_by_name('FirstName LastName')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

        query_set = Client.objects.get_clients_by_name('Name')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

        query_set = Client.objects.get_clients_by_name('first last')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

    def test_client_model(self):
        """
        Get client age
        Get created client data and check that data is correct
        """
        self.assertIsNotNone(self.client.get_client_age())
        self.assertIsNotNone(self.client.get_client_data())
        self.assertEqual(self.client.get_client_data()['id'],
                         self.client_id)
        self.assertEqual(self.client.get_client_data()['age'],
                         self.client.get_client_age())
        self.assertEqual(self.client.get_client_data()['first_name'],
                         self.client.first_name)

    def test_try_parsing_date(self):
        """
        Check try_parsing_date to correctly parse various types of dates
        Check for try_parsing_date to receive an error when the date format
        is incorrect
        """

        self.assertIsInstance(try_parsing_string_to_date('2000.01.20'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('20.01.2000'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('2000/01/20'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('20/01/2000'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('2000-01-20'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('20-01-2000'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('2000 01 20'),
                              datetime.date)
        self.assertIsInstance(try_parsing_string_to_date('20 01 2000'),
                              datetime.date)

        self.assertRaises(ValueError, try_parsing_string_to_date, '20-01-20')
        self.assertRaises(ValueError, try_parsing_string_to_date, '20012000')
        self.assertRaises(ValueError, try_parsing_string_to_date, 'abc')

    def tearDown(self):
        Client.objects.get(id=self.client_id).delete()
