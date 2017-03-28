from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rides.models import Ride
from crispy_forms.helper import FormHelper


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class RideForm(forms.ModelForm):
    total_seats = forms.IntegerField(help_text='Include your seat.', min_value=1, max_value=24)
    seats_avaliable = forms.IntegerField(min_value=1, max_value=10)
    destination = forms.CharField(max_length = 100)
    meetup_location = forms.CharField(widget=forms.TextInput(attrs={'class':'datetime'}), max_length = 100)
    meetup_time = forms.DateTimeField(help_text='DD/MM/YYYY HH:MM:SS format.', input_formats=['%d/%m/%Y %H:%M:%S'], widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S'))
    transportation_type = forms.CharField(max_length = 100)
    total_cost = forms.DecimalField(help_text='In $', max_digits=10, decimal_places=2)
    cost_per_person = forms.DecimalField(help_text='In $', max_digits=10, decimal_places=2)
    # creator = forms.CharField(max_length = 100, help_text='Your Username')
    class Meta:
        model = Ride
        fields = ['total_seats', 'seats_avaliable', 'destination', 'meetup_location', 'meetup_time', 'transportation_type', 'total_cost', 'cost_per_person']
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(RideForm, self).__init__(*args, **kwargs)