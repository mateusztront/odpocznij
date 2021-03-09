import random

from django.core.management import BaseCommand

from main.models import Feature, Room


class Command(BaseCommand):
    help = 'Populate database with rooms'

    def handle(self, *args, **options):
        for room in Room.objects.all():
            features = Feature.objects.all()
            numb = random.randint(4, len(features))
            list_of_features_id = [f.id for f in features]
            out = random.sample(list_of_features_id, numb)
            room.feature_set.set(out)
