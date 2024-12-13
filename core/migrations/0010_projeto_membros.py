# Generated by Django 4.2.17 on 2024-12-11 17:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_notificacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='membros',
            field=models.ManyToManyField(blank=True, related_name='projetos', to=settings.AUTH_USER_MODEL),
        ),
    ]