from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_slug_generator

phone_message = 'Please enter a valid phone number.'

phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message=phone_message
)

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_admin, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, 
                          is_active=True, 
                          is_admin=is_admin,
                          is_superuser=is_superuser, 
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(
                                        verbose_name='email address',
                                        max_length=255,
                                        unique=True,
                                    )
    mobile_number   = models.CharField(validators=[phone_regex], max_length=10, unique=True,)
    username        = models.CharField(max_length=255, unique=True,)
    is_staff        = models.BooleanField(('staff status'), default=False,
                    help_text=('Designates whether the user can log into this admin '
                    'site.'))
    is_active       = models.BooleanField(('active'), default=True,
                    help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_admin 		= models.BooleanField(default=False)
    date_joined     = models.DateTimeField(('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number', 'username',]

    def __str__(self):
        return self.email



class UserProfile(models.Model):
    user            = models.ForeignKey(MyUser, on_delete=models.CASCADE,)
    firstname       = models.CharField(max_length=255, blank=True)
    lastname        = models.CharField(max_length=255, blank=True)
    date_of_birth   = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.firstname + self.lastname