# Generated by Django 3.2.3 on 2021-07-17 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('check', models.BooleanField(default=False, verbose_name='Item completed')),
                ('value', models.DecimalField(decimal_places=4, default=0, max_digits=16)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.list')),
                ('responsible', models.ManyToManyField(blank=True, related_name='item_responsabilities', to=settings.AUTH_USER_MODEL, verbose_name='responsibles related')),
            ],
        ),
    ]
