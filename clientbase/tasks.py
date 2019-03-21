"""
Module contain celery tasks
"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core import mail

from clientbase.models import Client


@shared_task
def send_report(clients_id):
    content = Client.objects.get_like_data_in_string(clients_id)
    with mail.get_connection() as connection:
        mail.EmailMessage(
            'Clients like data', content, 'to@mail.ru', ['from@mail.ru'],
            connection=connection,
        ).send()
