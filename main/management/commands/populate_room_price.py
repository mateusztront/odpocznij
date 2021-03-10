from django.core.management import BaseCommand
from main.models import Room
import random

class Command(BaseCommand):
    help = 'Populate database with description of rooms'

    def handle(self, *args, **options):
        for room in Room.objects.all():
            room.price = random.randrange(50, 200, 50)
            room.save()