# Generated by Django 3.2.3 on 2023-01-22 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('to_buy', '0005_alter_itemlisttobuy_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemListComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=150)),
                ('enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ilc_creator', to=settings.AUTH_USER_MODEL)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ltb_list', to='to_buy.listtobuy')),
            ],
        ),
    ]
