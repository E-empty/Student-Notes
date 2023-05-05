from django.conf import settings
from django.db import models
from django.forms import Select
from django.contrib.auth.models import AbstractUser, Permission


class MyGroup(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.CharField(max_length=255, default="admin")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def update(self, name=None, permissions=None):
        if name:
            self.name = name
        if permissions:
            self.permissions = permissions
        self.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
    
    @staticmethod
    def get_user_groups(user):
        return MyGroup.objects.filter(user=user)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    groups = models.ManyToManyField(
        MyGroup,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='user_groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='user_permissions',
    )


class Note(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    note = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to="media/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(MyGroup)

    def __str__(self):
        return self.title