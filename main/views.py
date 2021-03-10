from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from main.form import UserRegistrationForm
from main.models import Premises


class LandingPageView(View):
    def get(self, request):
        return render(request, 'main/landingpage.html')


class MainView(View):
    def get(self, request):
        search = request.GET.get('search')
        request.session['search'] = search
        results = Premises.objects.all().filter(city=search)
        return render(request, 'main/main.html', {'results': results})


class PremisesView(View):
    def get(self, request, id):
        premises = Premises.objects.get(pk=id)
        room_types = premises.rooms.order_by('people_number')
        return render(request, "main/premises_view.html", {"premises": premises, "room_types": room_types})

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'main/user_form.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            return redirect('/')
        else:
            return render(request, 'main/user_form.html', {'form': form})
