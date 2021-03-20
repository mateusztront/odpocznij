import datetime

import pytest
from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed  # działa, nie usuwac

from main.models import Reservation, Review


def test_landingpage(client):
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/landingpage.html')


@pytest.mark.django_db
def test_main(client, new_premises_Szczecin):
    response = client.get(reverse('main-page'), {'search': 'Szczecin'})
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/main.html')
    assert response.context['results'].first().city == 'Szczecin'


@pytest.mark.django_db
def test_premises(client, new_premises):
    response = client.get(reverse('premises', args=[new_premises.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/premises_view.html')


@pytest.mark.django_db
def test_reservation_list(client, new_user, new_reservation):
    client.login(username='qwe', password='qwe')
    response = client.get(reverse('reservations', args=[new_reservation.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_reservation(client, new_user, new_premises, new_room):
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
def test_editreservation(client, new_user, new_premises, new_room, new_reservation):
    response = client.get(reverse('edit-reservation', args=[new_reservation.id]))
    assert response.status_code == 302
    client.login(username='qwe', password='qwe')
    response = client.get(reverse('edit-reservation', args=[new_reservation.id]))
    assert response.status_code == 200
    assert response.context['form'].initial['start_date'] == datetime.date(2021, 1, 1)


@pytest.mark.django_db
def test_deletereservation(client, new_user, new_premises, new_room, new_reservation, new_reservation2):
    client.login(username='qwe', password='qwe')
    assert Reservation.objects.count() == 2
    reservation = Reservation.objects.first()
    response = client.get(reverse('delete-reservation', args=[reservation.id]))
    assert response.status_code == 200
    response = client.post(reverse('delete-reservation', args=[reservation.id]))
    assert response.status_code == 302
    assert Reservation.objects.count() == 1



@pytest.mark.django_db
def test_clientregistrationview(client):
    client.post(reverse('client-registration'), {'username': 'username',
                                                 'first_name': 'Barbara',
                                                 'last_name': 'Radziwiłłówna',
                                                 'password': 'qwe',
                                                 'second_password': 'qwe',
                                                 'email': 'bar@ba.ra'})
    user = User.objects.first()
    assert user.first_name == 'Barbara'
    assert user.last_name == 'Radziwiłłówna'
    assert user.email == 'bar@ba.ra'

@pytest.mark.django_db
def test_loginform(client, new_user):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    response = client.post(reverse('login'), {'login': 'qwe',
                                              'password': 'qwe'})
    assert response.status_code == 302
    user = auth.get_user(client)
    assert user.is_authenticated
    response = client.post(reverse('login'), {'login': '123',
                                              'password': '123'})
    assert response.status_code == 200
    assert 'error' in response.context

@pytest.mark.django_db
def test_loginout(client, new_user):
    client.login(username='qwe', password='qwe')
    user = auth.get_user(client)
    assert user.is_authenticated
    response = client.get(reverse('logout'), {}, HTTP_REFERER=reverse('landing-page'))
    user = auth.get_user(client)
    assert user.is_anonymous


@pytest.mark.django_db
def test_edituser(client, new_user):
    client.login(username='qwe', password='qwe')
    user = User.objects.first()
    response = client.get(reverse('edit-user', args=[user.id]))
    assert response.status_code == 200
    ctx = response.context['form']
    assert ctx.instance.username == 'qwe'
    response = client.post(reverse('edit-user', args=[user.id]), {'username': 'QWE'})
    assert response.status_code == 302
    assert User.objects.first().username == 'QWE'

@pytest.mark.django_db
def test_userview(client, new_user):
    client.login(username='qwe', password='qwe')
    user = User.objects.first()
    response = client.get(reverse('user', args=[user.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_createreview(client, new_user, new_reservation):
    client.login(username='qwe', password='qwe')
    response = client.get(reverse('new-review', args=[new_reservation.id]))
    assert response.status_code == 200
    assert Review.objects.count() == 0
    response = client.post(reverse('new-review', args=[new_reservation.id]),
                           {'title': 'review title',
                           'content': 'review content',
                           'score': '8',
                           'user': new_user.id,
                           'reservation': new_reservation.id,
                           'premise': new_reservation.rooms.premises})
    assert response.status_code == 302
    assert Review.objects.count() == 1
