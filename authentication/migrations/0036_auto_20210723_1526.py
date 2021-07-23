# Generated by Django 3.0.7 on 2021-07-23 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0035_auto_20210723_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.IntegerField(default=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]