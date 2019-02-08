from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4

from app import settings


@deconstructible
class UploadPhoto(object):
    """
    Custom upload_to for client photo
    """
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        """
        Set random name to photo
        :param instance: FileField instance
        :param filename: name of photo
        :return: photo path with new name
        """
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)


upload_photo = UploadPhoto(settings.CLIENT_PHOTO_DIR)


def upload_photo_func(instance, filename):
    """
    Set random name to photo
    :param instance: FileField instance
    :param filename: name of photo
    :return: photo path with new name
    """
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(settings.CLIENT_PHOTO_DIR, filename)
