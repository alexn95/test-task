from django.db import models
from datetime import datetime
from django.db.models import Q

from clientbase.services import try_parsing_date


class ClientManager(models.Manager):
    # Return the clients list by First Name and Last Name 
    # or return all clients if name is None
    # and order this list by order_by parameter
    def get_clients_by_name(self, name, order_by='first_name'):
        clients = None
        if name:
            for query in name.split():
                clients = super().get_queryset().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).order_by(order_by)
        else:
            clients = super().get_queryset().order_by(order_by)
        return clients


# Model of the client
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='photos')
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
