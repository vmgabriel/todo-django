# Generated by Django 3.2.3 on 2022-09-14 16:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0011_alter_flowmoney_date_flow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowmoney',
            name='date_flow',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 7, 31, 806928)),
        ),
    ]