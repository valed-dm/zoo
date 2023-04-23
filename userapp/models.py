# from django.contrib.auth.models import Use
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
