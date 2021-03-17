import random

from django.core.management.base import BaseCommand
from faker import Faker

from main.models import Premises, Room


class Command(BaseCommand):
    help = 'Populate database with rooms'

    def handle(self, *args, **options):
        for premise in Premises.objects.all():
            if not premise.rooms.first():
                for _ in range(5, 50):
                    Room.objects.create(
                        people_number=random.randint(1, 4),
                        capacity=random.randint(5, 50),
                        premises=premise,
                        price = random.randrange(50, 200, 50),
                    )
