from django.core.management.base import BaseCommand
from faker import Faker

import random

from main.models import TYPES, Premises


class Command(BaseCommand):
    help = 'Populate database with premises'

    def handle(self, *args, **options):
        fake = Faker('pl-PL')
        fake.company()
        fake.street_address()
        fake.postcode()
        fake.city()
        for key, _ in TYPES:
            for _ in range(10):
                Premises.objects.create(
                    name=fake.company(),
                    address=fake.street_address(),
                    zip_code=fake.postcode(),
                    city=fake.city(),
                    country='PL',
                    type=key
                )



