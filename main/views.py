from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from main.forms import UserRegistrationForm, LoginForm, NewReservationForm, UserForm
from main.models import Premises, Reservation, Room, Review


class LandingPageView(View):
    def get(self, request):
        return render(request, 'main/landingpage.html')


class MainView(View):
    def get(self, request):
        search = request.GET.get('search')
        request.session['search'] = search  # przekazywanie wyikow wyszukiwania w innych widokach
        results = Premises.objects.all().filter(city=search).annotate(avg_score=Avg('review__score'))
        return render(request, 'main/main.html', {'results': results})


class PremisesView(View):
    def get(self, request, id):
        premises = Premises.objects.get(pk=id)
        room_types = premises.rooms.order_by('people_number')
        return render(request, "main/premises_view.html", {"premises": premises, "room_types": room_types})


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewReservationView(LoginRequiredMixin, View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        form = NewReservationForm()
        return render(request, 'main/reservation_form.html', {'form': form, 'room': room})

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        user = request.user
        form = NewReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            start_date = reservation.start_date
            end_date = reservation.end_date
            case_1 = Reservation.objects.filter(rooms=room, start_date__lte=start_date, end_date__gte=end_date).exists()
            case_2 = Reservation.objects.filter(rooms=room, start_date__lte=end_date, end_date__gte=end_date).exists()
            case_3 = Reservation.objects.filter(rooms=room, start_date__gte=start_date, end_date__lte=end_date).exists()
            if case_1 or case_2 or case_3:
                return render(request, 'main/reservation_form.html',
                              {'id': room.id, 'form': form, 'room': room,
                               'error': 'Pokój jest zajęty w podanych dniach'})

            reservation.rooms = room
            reservation.user = user
            reservation.save()
            return redirect('reservations', user.id)
        else:
            return render(request, 'main/reservation_form.html', {'form': form})


class EditReservationView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ['start_date', 'end_date']
    template_name_suffix = '_update_form'


class DeleteReservationView(LoginRequiredMixin, DeleteView):
    model = Reservation

    def get_success_url(self):
        reservation_id = self.kwargs['pk']
        return reverse_lazy('reservations', kwargs={'pk': reservation_id})


class ClientRegistrationView(View):
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


class EditUserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = UserForm(instance=user)
        return render(request, 'main/user_form.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            User.objects.update(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            return redirect('user')
        else:
            return render(request, 'main/user_form.html', {'form': form})


class UserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, 'main/user.html', {'user': user})


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'score', 'content']

    def form_valid(self, form):
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        form.instance.users = self.request.user
        form.instance.reservations = reservation
        form.instance.premise = reservation.rooms.premises
        return super().form_valid(form)

    def get_success_url(self):
        user_id = self.kwargs['pk']
        return reverse_lazy('reservations', kwargs={'pk': user_id})
