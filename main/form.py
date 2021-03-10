from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.forms as forms


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

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['second_password']:
            raise ValidationError("Proszę wprowadzić dwa razy to samo hasło")