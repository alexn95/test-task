"""
Module contain django models, managers and functions with used in this models
"""

from datetime import datetime

from django.db import models
from django.db.models import Q

from .enums import OrderBy
from .upload_photo import upload_photo
from app import settings


class ClientManager(models.Manager):
    """
    Manager for client model
    """
    def get_clients_by_name(self, query_string, order_by=OrderBy.fn.value[0]):
        """
        Search clients by query_string
        :param query_string: the string which contains first name
            and last name of a client
        :param order_by: the string by which the sort order is set
        :return: formatted client list
        """
        clients = None
        order_by_value = OrderBy.get_value(order_by)
        if query_string:
            for query in query_string.split():
                clients = super().get_queryset().filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query)
                ).order_by(order_by_value)
        else:
            clients = super().get_queryset().order_by(order_by_value)
        return clients

    def get_clients_photo_data(self):
        """
        Formatting and return client photo list using get_client_photo_data()
        :return: clients list
        """
        clients = super().all().order_by('id')
        data = list(map(
            lambda client: client.get_client_photo_data(), clients)
        )
        return data

    def get_like_data_in_string(self, clients_id):
        """
        Get clients by clients_id list.
        Return id, first name and likes count of this clients in string format.
        :param clients_id: list of clients id
        :return: id, first name and likes count in sting format
        """
        result = ''
        for client_id in clients_id:
            client = super().get(id=client_id)
            result += '{0}. {1} - {2} likes \n'.format(
                client_id, client.first_name, client.likes)
        return result


class Client(models.Model):
    """
    Client model class
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to=upload_photo)
    likes = models.IntegerField(default=0)
    objects = ClientManager()

    def get_client_data(self):
        """
        Return client data with age and photo url
        :return: client data
        """
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date': self.date_of_birth,
            'photo': self.photo.url,
            'age': self.get_client_age(),
        }
        return data

    def get_client_photo_data(self):
        """
        Return client photo and like for it
        :return: client data
        """
        data = {
            'id': self.id,
            'photo': self.photo.url,
            'likes': self.likes,
        }
        return data

    def get_client_age(self):
        """
        Calculate and return the client age
        :return: the client age
        """
        today = try_parsing_string_to_date(str(datetime.now().date()))
        born = try_parsing_string_to_date(str(self.date_of_birth))
        age = today.year - born.year - (
                (today.month, today.day) < (born.month, born.day)
        )
        return age


def try_parsing_string_to_date(date):
    """
    Parsing date from string, check all possible formats
    :param date: Date in string format
    :return: date
    """
    for fmt in settings.DATE_INPUT_FORMATS:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')



