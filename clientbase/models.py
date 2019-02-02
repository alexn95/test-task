from django.db import models
from datetime import datetime
from django.db.models import Q

import os
from uuid import uuid4

from app import settings


class ClientManager(models.Manager):
    # Return the clients list by First Name and Last Name 
    # or return all clients if name is None
    # and order this list by order_by parameter
    def get_clients_by_name(self, name, order_by='first_name'):
        clients = None
        if name:
            for query in name.split():
                clients = super().get_queryset().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))\
                    .order_by(order_by)
        else:
            clients = super().get_queryset().order_by(order_by)
        return clients

    # Return full data for all clients
    def get_all_clients_data(self):
        clients = super().all()
        data = list(map(lambda client: client.get_client_data(), clients))
        return data


# Formatting the path to the client's photo
def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


# Model of the client
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to=path_and_rename('photos'))
    objects = ClientManager()

    # Format and return the client data
    def get_client_data(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date': self.date_of_birth,
            'photo': self.photo.url,
            'age': self.get_client_age()
        }
        return data
    
    # Calculate and return the client age
    def get_client_age(self):
        today = try_parsing_date(str(datetime.now().date()))
        born = try_parsing_date(str(self.date_of_birth))
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return age


# Parsing date from string, check all possible formats
def try_parsing_date(date):
    for fmt in settings.DATE_INPUT_FORMATS:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')



