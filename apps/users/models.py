from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class User(BaseModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
