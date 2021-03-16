# Generated by Django 3.1.7 on 2021-03-16 13:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210316_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
