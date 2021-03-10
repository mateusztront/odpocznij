from lorem_text import lorem
from django.core.management import BaseCommand
from main.models import Premises


class Command(BaseCommand):
    help = 'Populate database with description of rooms'

    def handle(self, *args, **options):
        for premise in Premises.objects.all():
            premise.description = lorem.paragraph()
            premise.save()