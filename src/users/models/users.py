import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


def get_default_avatar_image():
    return None


class UnikubeUser(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar_image = models.FileField(blank=True, null=True, default=get_default_avatar_image)
