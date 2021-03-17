from pytest_django.asserts import assertTemplateUsed #działa, nie usuwac
import pytest
from django.test import Client
from django.urls import reverse

from main.models import Premises

client = Client()

def test_landingpage():
        response = client.get(reverse('landing-page'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/landingpage.html')

@pytest.mark.django_db
def test_main():
        response = client.get(reverse('main-page'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/main.html')
        #przetestowac po dodawaniu premises
