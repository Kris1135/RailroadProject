from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passengers, Reservation_conn, Stations

from django.forms.widgets import Select
    
class PassengersForm(UserCreationForm):
    preferred_card_number = forms.CharField(max_length=16, required=True)
    preferred_billing_address = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'preferred_card_number', 'preferred_billing_address',)

class SearchForm(forms.ModelForm):

    class Meta:
        model = Reservation_conn
        widgets = {
            'reserve_day': forms.DateInput(attrs={'class':'datepicker'}),
        }
        labels = {
            "time_of_day": "Time Range",
            "reserve_day": "Date",
            "start_loc": "Start",
            "end_loc": "End",
        }
        fields = '__all__'

class BookForm(forms.ModelForm):
    train = forms.CharField(max_length=1,required=True)
    departure = forms.TimeField(required=True)
    arrival = forms.TimeField(required=True)
    price = forms.FloatField(required=True)
    start_loc1 = forms.CharField(max_length=40, required=True)
    end_loc1 = forms.CharField(max_length=40, required=True)
    res_day = forms.DateField(required=True)

    class Meta:
        model = Reservation_conn
        fields = ('train', 'departure', 'arrival', 'price', 'start_loc1', 'end_loc1')

class DeleteForm(forms.ModelForm):
    reserve_id = forms.IntegerField(required=True)

    class Meta:
        model = Reservation_conn
        fields = ('reserve_id',)