from django.db import models

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=30)

class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    photo = models.FileField(blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=20)
    logo = models.FileField(blank=True, null=True)
