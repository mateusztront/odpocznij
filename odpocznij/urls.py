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

from main.views import LandingPageView, MainView, PremisesView, UserRegistrationView, LoginFormView, LogoutView, \
    EditUserView, UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('index/', MainView.as_view(), name='main-page'),
    path('index/<int:id>/', PremisesView.as_view(), name='premises'),
    path('client_form/', UserRegistrationView.as_view(), name='client-registration'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/', UserView.as_view(), name='user'),
    path('user/<int:pk>/edit_user/', EditUserView.as_view(), name='edit-user'),
]
