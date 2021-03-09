from django.db import models
from django_countries.fields import CountryField

# Create your models here.

TYPES = [
    ('ZOL', 'Zakład opiekuńczo-leczniczy'),
    ('OR', 'Oddział Rehabilitacji'),
    ('S', 'Sanatorium'),
    ('DPS', 'Dom Pomocy Społecznej'),
    ('DOP', 'Długoterminowa opieka prywatna'),
    ('KOP', 'Krótkoterminowa opieka prywatna'),
]


class Premises(models.Model):
    COUNTRIES_FIRST = ['PL']
    name = models.CharField(max_length=256)
    address = models.CharField("Adres", max_length=1024)
    zip_code = models.CharField("Kod pocztowy", max_length=12)
    city = models.CharField("Miejscowość", max_length=1024)
    country = CountryField()
    type = models.CharField(max_length=32, choices=TYPES)


class Room(models.Model):
    people_number = models.IntegerField()
    capacity = models.FloatField(null=True, blank=True)
    premises = models.ForeignKey(Premises, related_name='premises', on_delete=models.CASCADE)


class Feature(models.Model):
    name = models.CharField(max_length=256)
    room = models.ManyToManyField(Room)
