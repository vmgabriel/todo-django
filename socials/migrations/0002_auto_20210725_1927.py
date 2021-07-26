# Generated by Django 3.2.3 on 2021-07-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconnection',
            name='access_token',
            field=models.CharField(max_length=120, null=True, verbose_name='access_token'),
        ),
        migrations.AddField(
            model_name='socialconnection',
            name='refresh_token',
            field=models.CharField(max_length=120, null=True, verbose_name='refresh_token'),
        ),
    ]
