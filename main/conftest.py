import pytest
from django.contrib.auth.models import User

from main.models import Premises, Room, Reservation


@pytest.fixture
def new_premises():
    new_premises = Premises.objects.create(name='ośrodek', address='ul. Obrońców 27',
                                               zip_code='01-237', city='Miasto',
                                               country='PL', type='ZOL', description='qwe')
    return new_premises

@pytest.fixture
def new_premises_Szczecin():
    new_premises = Premises.objects.create(name='ośrodek', address='ul. Obrońców 27',
                                               zip_code='01-237', city='Szczecin',
                                               country='PL', type='ZOL', description='qwe')
    return new_premises

@pytest.fixture
def new_user():
    new_user = User.objects.create_user(username='qwe', password='qwe')
    return new_user


@pytest.fixture
def new_room(new_premises):
    new_room = Room.objects.create(people_number=2, price=127.1, capacity=32, premises=new_premises)
    return new_room


@pytest.fixture
def new_reservation(new_user, new_room):
    new_reservation = Reservation.objects.create(start_date='2021-01-01',
                                                 end_date='2021-01-10',
                                                 rooms_id=new_room.id,
                                                 user=new_user)
    return new_reservation