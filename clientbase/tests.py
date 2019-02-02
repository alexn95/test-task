from random import randint, randrange
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client as TestClient
from django.urls import reverse

from app.settings import MEDIA_ROOT
from clientbase.forms import ClientForm
from clientbase.models import Client, try_parsing_date


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

    def test_get_client_by_id(self):
        # Get created client by id and check his id and first_name
        client = Client.objects.get(id=self.client_id)
        self.assertEqual(client.id, self.client_id)
        self.assertEqual(client.first_name, 'FirstName')

    def test_get_clients_by_name(self):
        # Get created client by full query string, check if it is found and check her id
        query_set = Client.objects.get_clients_by_name('FirstName LastName')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

        # Get created client by parts of one of name, check if it is found and check her id
        query_set = Client.objects.get_clients_by_name('Name')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

        # Get created client by parts of both names, check if it is found and check her id
        query_set = Client.objects.get_clients_by_name('first last')
        self.assertTrue(len(query_set) > 0)
        self.assertEqual(list(query_set)[0].id, self.client_id)

    def test_client_model(self):
        client = Client.objects.get(id=self.client_id)

        # Get client age
        self.assertIsNotNone(client.get_client_age())

        # Get created client data and check that data is correct
        self.assertIsNotNone(client.get_client_data())
        self.assertEqual(client.get_client_data()['id'], self.client_id)
        self.assertEqual(client.get_client_data()['age'], client.get_client_age())
        self.assertEqual(client.get_client_data()['first_name'], client.first_name)

    def test_try_parsing_date(self):
        # Check try_parsing_date to correctly parse various types of dates
        self.assertIsInstance(try_parsing_date('2000.01.20'), datetime.date)
        self.assertIsInstance(try_parsing_date('20.01.2000'), datetime.date)
        self.assertIsInstance(try_parsing_date('2000/01/20'), datetime.date)
        self.assertIsInstance(try_parsing_date('20/01/2000'), datetime.date)
        self.assertIsInstance(try_parsing_date('2000-01-20'), datetime.date)
        self.assertIsInstance(try_parsing_date('20-01-2000'), datetime.date)
        self.assertIsInstance(try_parsing_date('2000 01 20'), datetime.date)
        self.assertIsInstance(try_parsing_date('20 01 2000'), datetime.date)

        # Check for try_parsing_date to receive an error when the date format is incorrect
        self.assertRaises(ValueError, try_parsing_date, '20-01-20')
        self.assertRaises(ValueError, try_parsing_date, '20012000')
        self.assertRaises(ValueError, try_parsing_date, 'abc')

# class ServicesTestCase(TestCase):


class ViewsTestCase(TestCase):
    def setUp(self):
        self.test_client = TestClient()

        # Create test client one
        self.client1_id = randint(0, 100000)
        Client.objects.create(
            id=self.client1_id,
            first_name='FirstNameOne',
            last_name='LastNameOne',
            date_of_birth='1995-02-24',
            photo='test_photo.png'
        )
        self.client1 = Client.objects.get(id=self.client1_id)

        # Create test client two
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
        # Check clients list
        response = self.test_client.get(reverse('client_list'), {'query_string': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data() in response.context['clients'])
        self.assertTrue(self.client2.get_client_data() in response.context['clients'])

        # Check clients list by full name
        response = self.test_client.get(reverse('client_list'), {'query_string': 'FirstName LastName'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data() in response.context['clients'])
        self.assertTrue(self.client2.get_client_data() in response.context['clients'])

        # Check clients list by part of client name
        response = self.test_client.get(reverse('client_list'), {'query_string': 'Name'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data() in response.context['clients'])
        self.assertTrue(self.client2.get_client_data() in response.context['clients'])

        # Check clients list by part of one client name
        response = self.test_client.get(reverse('client_list'), {'query_string': 'One'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data() in response.context['clients'])
        self.assertTrue(self.client2.get_client_data() not in response.context['clients'])

        # Check clients list by non-existent name
        response = self.test_client.get(reverse('client_list'), {'query_string': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client1.get_client_data() not in response.context['clients'])
        self.assertTrue(self.client2.get_client_data() not in response.context['clients'])

    def test_client_card_view(self):
        # Check client card content
        response = self.test_client.get(reverse('client_card', kwargs={'client_id': self.client1_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client1.get_client_data(), response.context['client'])

        # Check client card by non-existent id
        response = self.test_client.get(reverse('client_card', kwargs={'client_id': 0}))
        self.assertEqual(response.status_code, 404)

    def test_client_create_view(self):
        # Check create client view
        response = self.test_client.get(reverse('client_create'))
        self.assertEqual(response.status_code, 200)

    def test_client_delete_view(self):
        # Check delete client view
        response = self.test_client.get(reverse('client_delete', kwargs={'client_id': self.client1_id}))
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, Client.objects.get, id=self.client1_id)


class FormsTestCase(TestCase):
    def test_client_form(self):
        # Create image object
        url = MEDIA_ROOT + 'photos/test_photo.png'
        photo = SimpleUploadedFile(name='test_photo.png', content=open(url, 'rb').read(), content_type='image/png')

        # Positive validation form
        form_data = {
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'date_of_birth': '24-02-1995',
            'photo': photo.name
        }
        form = ClientForm(form_data, {'photo': photo})
        self.assertTrue(form.is_valid())

        # Negative validation form
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
        self.first_name_list = ['Toby', 'Dusty', 'Lana', 'Rocky', 'Dexter', 'Cris', 'Scarlet', 'Danette']
        self.last_name_list = ['Roger', 'Black', 'Maloof', 'Silk', 'Kush', 'Tootle', 'Odriscoll', 'White']

    # Write 10 client in base
    def test_create_clients(self):
        for i in range(10):
            first_name = self.first_name_list[randrange(len(self.first_name_list))]
            last_name = self.first_name_list[randrange(len(self.last_name_list))]
            Client.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth='199%s-01-01' % randint(1, 9),
                photo='test_photo.png'
            )
