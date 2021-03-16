"""odpocznij URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import LandingPageView, MainView, PremisesView, LoginFormView, LogoutView, \
    EditUserView, UserView, ReservationListView, NewReservationView, ClientRegistrationView, EditReservationView, \
    DeleteReservationView, CreateReviewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('index/', MainView.as_view(), name='main-page'),
    path('index/<int:id>/', PremisesView.as_view(), name='premises'),
    path('user/<int:pk>/reservations/', ReservationListView.as_view(), name='reservations'),
    path('index/<int:id>/new_reservation/', NewReservationView.as_view(), name='new-reservation'),
    path('index/<int:pk>/edit_reservation/', EditReservationView.as_view(), name='edit-reservation'),
    path('index/<int:pk>/delete_reservation/', DeleteReservationView.as_view(), name='delete-reservation'),
    path('client_registration/', ClientRegistrationView.as_view(), name='client-registration'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/', UserView.as_view(), name='user'),
    path('user/<int:pk>/edit_user/', EditUserView.as_view(), name='edit-user'),
    path('index/<int:pk>/reservations/new_review/', CreateReviewView.as_view(), name='new-review')
]
