# Generated by Django 3.0.7 on 2021-07-23 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0039_usertransaction_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertransaction',
            name='user_email',
        ),
    ]
