import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed  # działa, nie usuwac

from main.models import Reservation

client = Client()


def test_landingpage():
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/landingpage.html')


@pytest.mark.django_db
def test_main(new_premises_Szczecin):
    response = client.get(reverse('main-page'), {'search': 'Szczecin'})
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/main.html')
    assert response.context['results'].first().city == 'Szczecin'


@pytest.mark.django_db
def test_premises(new_premises):
    response = client.get(reverse('premises', args=[new_premises.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/premises_view.html')


@pytest.mark.django_db
def test_reservation_list(new_user, new_reservation):
    client.login(username='qwe', password='qwe')
    response = client.get(reverse('reservations', args=[new_reservation.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_reservation(new_user, new_premises, new_room):
    client.login(username='qwe', password='qwe')
    response = client.get(reverse('new-reservation', args=[new_room.id]))
    assert response.status_code == 200
    assert response.context['room'].premises.name == 'ośrodek'
    response = client.post(reverse('new-reservation', args=[new_room.id]), {'start_date': '2022-01-02',
                                                                            'end_date': '2022-01-10'})
    assert response.status_code == 302
    assert Reservation.objects.first().start_date == datetime.date(2022, 1, 2)

    response = client.post(reverse('new-reservation', args=[new_room.id]), {'start_date': '2022-01-01',
                                                                            'end_date': '2022-01-04'})
    assert response.status_code == 200
    assert 'error' in response.context

    response = client.post(reverse('new-reservation', args=[new_room.id]), {'start_date': '2022-01-08',
                                                                            'end_date': '2022-01-12'})
    assert response.status_code == 200
    assert 'error' in response.context

    response = client.post(reverse('new-reservation', args=[new_room.id]), {'start_date': '2022-01-05',
                                                                            'end_date': '2022-01-07'})
    assert response.status_code == 200
    assert 'error' in response.context

@pytest.mark.django_db
def test_clientregistrationview():
    client.post(reverse('client-registration'), {'username': 'username',
                                                 'first_name': 'Barbara',
                                                 'last_name': 'Radziwiłłówna',
                                                 'password': 'qwe',
                                                 'second_password': 'qwe',
                                                 'email': 'bar@ba.ra'})
    user = User.objects.first()
    assert user.first_name == 'Barbara'  # porownac z username u gory
    assert user.last_name == 'Radziwiłłówna'
    assert user.email == 'bar@ba.ra'
