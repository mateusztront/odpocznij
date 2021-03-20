from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.forms as forms

from main.models import Reservation, Review


def username_unique(username):
    if User.objects.filter(username=username):
        raise ValidationError('Login jest zajęty')


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='login', validators=[username_unique])
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)
    second_password = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(label='imię')
    last_name = forms.CharField(label='nazwisko')
    email = forms.EmailField(label='email')
    #zapytać Sławka
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data['password'] != cleaned_data['second_password']:
    #         raise ValidationError("Proszę wprowadzić dwa razy to samo hasło")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class LoginForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)


class NewReservationForm(forms.ModelForm):
    class Meta:
        labels = {'start_date': 'Data początkowa', 'end_date': 'Data końcowa'}
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {'start_date': forms.SelectDateWidget, 'end_date': forms.SelectDateWidget} #można zaimplementować datepicker https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html


class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'score', 'content']
        labels = {'title': 'Tytuł', 'score': 'Ocena', 'content': 'Treść'}


