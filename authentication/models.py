from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password=None, password2=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, first_name, last_name, email, password=None, password2=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(first_name, last_name, email, password, password2)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

   
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    profile_picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', null=True, blank=True) # default='/Images/None/No-img.jpg'
    #password is at serializers.py model field
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_ip = models.GenericIPAddressField(null=True)

    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    CHOICES = (
    ('1 star','1 star'),
    ('2 star', '2 star'),
    ('3 star','3 star'),
    ('4 star','4 star'),
    ('5 star','5 star'),)


    rating = models.CharField(max_length=6, choices=CHOICES, default='5 star')
    feedback_text = models.TextField(max_length=1000,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __unicode__(self):
        return u"photo {0}".format(self.file.url)

    # @staticmethod
    # def has_perm(perm, obj=None):
    #     # "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @staticmethod
    # def has_module_perms(app_label):
    #     # "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def __str__(self):
    #     return "{}".format(self.email)

