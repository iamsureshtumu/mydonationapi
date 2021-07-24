from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _
# from django.db.models.manager import EmptyManager
# from django.contrib import auth
# from django.core.exceptions import PermissionDenied
from .utils import create_new_ref_number

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
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    profile_picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', null=True, blank=True) # default='/Images/None/No-img.jpg'
    #password is at serializers.py model field

    no_of_transactions = models.IntegerField(_('no of transactions'), null=True)
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_ip = models.GenericIPAddressField(null = True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.client_ip)

    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    # CHOICES = (
    # ('5 star','5 star'),
    # ('4 star','4 star'),
    # ('3 star','3 star'),
    # ('2 star','2 star'),
    # ('1 star','1 star'),)


    # rating = models.CharField(max_length=6, choices=CHOICES, default='5 star')
    # feedback_text = models.TextField(max_length=1000,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        # return self.email
        return str(self.id)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __unicode__(self):
        return u"photo {0}".format(self.file.url)


class GuestUser(AbstractBaseUser):
    secret_key = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique=True)
    transaction_successful_ID= models.CharField(null=True, max_length=1000)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=False) #unique turned into flase, coz many people can donate using single mailID
    portfolio_name = models.CharField(max_length=1000)
    amount = models.IntegerField(null=True)
    charities = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_ip = models.GenericIPAddressField(null = True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


CHOICES = (
    ('5 star','5 star'),
    ('4 star','4 star'),
    ('3 star','3 star'),
    ('2 star','2 star'),
    ('1 star','1 star'),)

class RatingFeedback(models.Model):
    name =models.CharField(max_length=20,null=True)
    rating = models.CharField(max_length=6, choices=CHOICES, default='5 star')
    feedback_text = models.TextField(max_length=1000,null=True)

    def __str__(self):
        return self.rating


class UserTransaction(models.Model):
    referrence_number = models.CharField(_('referrence number'),primary_key=True, max_length = 10, blank=True, editable=False, unique=True, default=create_new_ref_number)
    transaction_successful_ID= models.CharField(null=True, max_length=1000)
    portfolio_name = models.CharField(max_length=1000, null=True)
    amount = models.IntegerField(null=True)
    charities = models.TextField(max_length=10000,null=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=False, default=True) #it will return email because the username field is email

    # def __str__(self):
    #     return self.user_id

    def __str__(self):
        return str(self.user_id)

    # class Meta:
    #     ordering = ['portfolio_name']