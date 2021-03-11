from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from main.forms import UserRegistrationForm, LoginForm
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


class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'main/login.html', {'form': form, 'error': 'Brak użytkownika o podanym loginie'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(request.META['HTTP_REFERER'])


class EditUserView(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'
    template_name = 'main/user_form.html'

    # def get(self, request, id):
    #     form = UserRegistrationForm() #jak usunę initial to jest ok, ale nie wyswietla wartosci w polach initial=request.user
    #     return render(request, 'main/user_form.html', {'form': form})
    #
    # def post(self, request, id):
    #     form = UserRegistrationForm(data=request.POST)
    #     if form.is_valid():
    #         User.objects.update(
    #             username=form.cleaned_data['username'],
    #             first_name=form.cleaned_data['first_name'],
    #             last_name=form.cleaned_data['last_name'],
    #             password=form.cleaned_data['password'],
    #             email=form.cleaned_data['email']
    #         )
    #         return redirect('user')
    #     else:
    #         return render(request, 'main/user_form.html', {'form': form})



class UserView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, 'main/user.html', {'user': user})
