from django.db import models

# Create your models here.

class Subscribe_model(models.Model):
    email = models.EmailField(max_length=30, null= False)
    name = models.CharField(max_length=20, null=False)