# Generated by Django 3.0.7 on 2021-07-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0028_user_no_of_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='no_of_transactions',
            field=models.IntegerField(null=True),
        ),
    ]
