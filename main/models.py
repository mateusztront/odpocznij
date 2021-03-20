from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
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
    name = models.CharField("Nazwa", max_length=256)
    address = models.CharField("Adres", max_length=1024)
    zip_code = models.CharField("Kod pocztowy", max_length=12)
    city = models.CharField("Miejscowość", max_length=1024)
    country = CountryField()
    type = models.CharField(max_length=32, choices=TYPES)
    description = models.TextField()

    def __str__(self):
        return self.name



class Room(models.Model):
    people_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.FloatField(null=True, blank=True)
    premises = models.ForeignKey(Premises, related_name='rooms', on_delete=models.CASCADE)



class Feature(models.Model):
    name = models.CharField(max_length=256)
    rooms = models.ManyToManyField(Room)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE) #zaminiec na room

    def get_absolute_url(self):
        return reverse('reservation', args=[self.id])


class Review(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation, related_name='reviews', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    premise = models.ForeignKey(Premises, on_delete=models.CASCADE)

