from django.db import models
from django.contrib.auth.models import User
from django.forms import Select



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    note = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to="media/")
    owner = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=20)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    pass1 = models.CharField(max_length=50)
    pass2 = models.CharField(max_length=100)
    



