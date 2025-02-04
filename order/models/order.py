from django.db import models
from django.contrib.auth.models import user

class Order(models.Model):
    product = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(User, null=False)