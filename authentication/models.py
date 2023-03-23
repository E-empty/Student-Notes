from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    pass1 = models.CharField(max_length=50)
    pass2 = models.CharField(max_length=100)
