from django.db import models
from django.contrib.auth.models import AbstractUser
from json import JSONEncoder

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=255, primary_key=True)
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    def get_username(self) -> str:
        return self.email


class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
