# Generated by Django 3.0.7 on 2021-07-10 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_auto_20210710_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingfeedback',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]