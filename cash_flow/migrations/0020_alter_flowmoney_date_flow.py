# Generated by Django 3.2.3 on 2023-01-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0019_auto_20230107_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowmoney',
            name='date_flow',
            field=models.DateField(blank=True, default='2023-01-08'),
        ),
    ]