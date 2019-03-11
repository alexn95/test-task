from django.db import transaction
from django.db.models import F

from app import settings
from celeryapp.celery import app
from clientbase.models import Client


@app.task
def set_like(client_id):
    with transaction.atomic():
        result = Client.objects.select_for_update().filter(
            id=client_id, likes__lt=settings.MAX_LIKES
        ).update(likes=F('likes') + 1)
    return result
