from datetime import datetime

from django.db import models
from django.db.models import Q

from .upload_photo import upload_photo
from app import settings


class ClientManager(models.Manager):
    def get_clients_by_name(self, name, order_by='first_name'):
        """
        Search clients by name
        :param name: the string by which clients are searched
        :param order_by: the string by which the sort order is set
        :return: client list
        """
        clients = None
        if name:
            for query in name.split():
                clients = super().get_queryset().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))\
                    .order_by(order_by)
        else:
            clients = super().get_queryset().order_by(order_by)
        return clients

    def get_clients_data(self):
        """
        Clients data formatting using get_client_data()
        :return: clients list
        """
        clients = super().all()
        data = list(map(lambda client: client.get_client_data(), clients))
        return data

    def get_clients_photo_data(self):
        """
        Clients photo and likes formatting using get_client_photo_data()
        :return: clients list
        """
        clients = super().all().order_by('id')
        data = list(map(lambda client: client.get_client_photo_data(), clients))
        return data


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
        :return: formatted clients data for the list
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
        :return: formatted clients photo data for the list
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
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
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



