"""
Module contain tests of view functionality
"""

from random import randint, randrange

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test import Client as TestClient
from django.urls import reverse

from ..models import Client


class ViewsTestCase(TestCase):
    """
    Test cases of application views
    """
    def setUp(self):
        """
        Create test clients
        """
        self.test_client = TestClient()

        self.client1_id = randint(0, 100000)
        Client.objects.create(
            id=self.client1_id,
            first_name='FirstNameOne',
            last_name='LastNameOne',
            date_of_birth='1995-02-24',
            photo='test_photo.png'
        )
        self.client1 = Client.objects.get(id=self.client1_id)

        self.client2_id = randint(0, 100000)
        Client.objects.create(
            id=self.client2_id,
            first_name='FirstNameTwo',
            last_name='LastNameTwo',
            date_of_birth='1995-02-24',
            photo='test_photo.png'
        )
        self.client2 = Client.objects.get(id=self.client2_id)

    def test_clients_list_view(self):
        """
        Check clients list by full name
        Check clients list by part of client name
        Check clients list by part of one client name
        Check clients list by non-existent name
        """
        response = self.test_client.get(
            reverse('client_list'), {'query_string': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'FirstName LastName'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'Name'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'One'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        not in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data()
                        not in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        not in response.context['clients'])

    def test_client_card_view(self):
        """
        Check client card content
        Check client card by non-existent id
        """
        response = self.test_client.get(
            reverse('client_card', kwargs={'pk': self.client1_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client1.get_client_data(), response.context['client'])

        response = self.test_client.get(
            reverse('client_card', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, 404)

    def test_client_create_view(self):
        """
        Check create client view
        """
        response = self.test_client.get(reverse('client_create'))
        self.assertEqual(response.status_code, 200)

    def test_client_delete_view(self):
        """
        Check delete client view
        """
        response = self.test_client.post(
            reverse('client_delete', kwargs={'pk': self.client1_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRaises(ObjectDoesNotExist,
                          Client.objects.get,
                          id=self.client1_id)

    def test_client_photo_view(self):
        """
        Check client photo view
        """
        response = self.test_client.get(reverse('client_photo'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_photo_data()
                        in response.context['clients'])
