from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class CreateAdd(models.Model):
    item_name = models.CharField(max_length=250, unique=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=False)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
