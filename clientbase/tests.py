from random import randint, randrange
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client as TestClient
from django.urls import reverse

from rest_framework import status

from .forms import ClientForm
from .models import Client, try_parsing_string_to_date
from .services import is_string_represent_an_int, try_parsing_date
from app.settings import MEDIA_ROOT


class ClientTestCase(TestCase):
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


class ViewsTestCase(TestCase):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'FirstName LastName'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client1.get_client_data()
                        in response.context['clients'])
        self.assertTrue(self.client2.get_client_data()
                        not in response.context['clients'])

        response = self.test_client.get(
            reverse('client_list'), {'query_string': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client1.get_client_data(), response.context['client'])

        response = self.test_client.get(
            reverse('client_card', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_client_create_view(self):
        """
        Check create client view
        """
        response = self.test_client.get(reverse('client_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_delete_view(self):
        """
        Check delete client view
        """
        response = self.test_client.post(
            reverse('client_delete', kwargs={'pk': self.client1_id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRaises(ObjectDoesNotExist,
                          Client.objects.get,
                          id=self.client1_id)

    def test_client_photo_view(self):
        """
        Check client photo view
        """
        response = self.test_client.get(reverse('client_photo'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client1.get_client_photo_data()
                        in response.context['clients'])


class FormsTestCase(TestCase):
    def test_client_form(self):
        """
        Test create client form
        Test create image object, positive validation form,
        negative validation form
        """
        url = MEDIA_ROOT + 'photo/test_photo.png'
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


class CreateDataTestCase(TestCase):
    def setUp(self):
        """
        Create client name list
        """
        self.first_name_list = ['Toby', 'Dusty', 'Lana', 'Rocky',
                                'Dexter', 'Cris', 'Scarlet', 'Danette']
        self.last_name_list = ['Roger', 'Black', 'Maloof', 'Silk',
                               'Ash', 'Tootle', 'Odriscoll', 'White']
        self.test_client = TestClient()

    def test_create_clients(self):
        """
        Write 10 client in base
        Get created clients by id and check them status_code
        """
        for i in range(100):
            first_name = self.first_name_list[
                randrange(len(self.first_name_list))
            ]
            last_name = self.first_name_list[
                randrange(len(self.last_name_list))
            ]
            Client.objects.create(
                id=i,
                first_name=first_name,
                last_name=last_name,
                date_of_birth='199%s-01-01' % randint(1, 9),
                photo='test_photo.png'
            )

        for i in range(100):
            response = self.test_client.get(
                reverse('client_card', kwargs={'pk': i})
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServicesTestCase(TestCase):

    def test_is_string_represent_an_int(self):
        """
        Check is_string_represent_an_int
        """
        self.assertTrue(is_string_represent_an_int('1'))
        self.assertFalse(is_string_represent_an_int('1asd'))

    def test_try_parsing_date(self):
        """
        Check try_parsing_date
        """
        self.assertIsInstance(try_parsing_date(datetime.datetime.now()), str)

    def test_try_parsing_string_to_date(self):
        """
        Check try_parsing_string_to_date with any available formats
        """
        date_list = (
            '2000-01-21', '21-01-2000',
            '2000/01/21', '21/01/2000',
            '2000.01.21', '21.01.2000',
            '2000 01 21', '21 01 2000',
        )
        for date in date_list:
            self.assertIsInstance(try_parsing_string_to_date(date),
                                  datetime.datetime)
