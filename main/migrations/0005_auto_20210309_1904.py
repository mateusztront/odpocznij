# Generated by Django 3.1.7 on 2021-03-09 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_premises_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='premises',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='main.premises'),
        ),
    ]
