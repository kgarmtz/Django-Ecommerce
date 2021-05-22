from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .managers import AccountManager

# Custom User Model
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    # Required fields for the AbstractBaseUser class when we are creating a custom user model
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    # is_staff: if the user has permission to access to the admin site
    is_staff        = models.BooleanField(default=False)
    # is_active: if the user account can be used for authentication
    is_active       = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    # We have to indicate with which field the user will log in into our application
    USERNAME_FIELD = 'email'
    # Extra fields that are required for our model
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # Linking the manager to our model
    objects = AccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    # If the user is superuser, then has the permission to do any changes
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True