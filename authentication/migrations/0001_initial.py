# Generated by Django 3.0.7 on 2021-07-24 17:24

import authentication.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m/%d/')),
                ('no_of_transactions', models.IntegerField(null=True, verbose_name='no of transactions')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_ip', models.GenericIPAddressField(null=True)),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuestUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('secret_key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('transaction_successful_ID', models.CharField(max_length=1000, null=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('portfolio_name', models.CharField(max_length=1000)),
                ('amount', models.IntegerField(null=True)),
                ('charities', models.TextField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_ip', models.GenericIPAddressField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RatingFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('rating', models.CharField(choices=[('5 star', '5 star'), ('4 star', '4 star'), ('3 star', '3 star'), ('2 star', '2 star'), ('1 star', '1 star')], default='5 star', max_length=6)),
                ('feedback_text', models.TextField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTransaction',
            fields=[
                ('referrence_number', models.CharField(blank=True, default=authentication.utils.create_new_ref_number, editable=False, max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='referrence number')),
                ('transaction_successful_ID', models.CharField(max_length=1000, null=True)),
                ('portfolio_name', models.CharField(max_length=1000, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('charities', models.TextField(max_length=10000, null=True)),
                ('user_id', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
