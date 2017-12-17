from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passengers, Search, Stations

from django.forms.widgets import Select
    
class PassengersForm(UserCreationForm):
    preferred_card_number = forms.CharField(max_length=16, required=True)
    preferred_billing_address = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'preferred_card_number', 'preferred_billing_address',)

class SearchForm(forms.ModelForm):

    class Meta:
        loc_choices = Stations.objects.all()
        model = Search
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
