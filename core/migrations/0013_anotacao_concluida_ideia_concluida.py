# Generated by Django 5.1.2 on 2024-12-17 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_notificacao_convite'),
    ]

    operations = [
        migrations.AddField(
            model_name='anotacao',
            name='concluida',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ideia',
            name='concluida',
            field=models.BooleanField(default=False),
        ),
    ]
