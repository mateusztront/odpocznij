# Generated by Django 3.1.7 on 2021-03-10 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_room_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
