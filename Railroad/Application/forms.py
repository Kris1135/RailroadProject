from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Passengers

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password','first_name', 'last_name', 'email')

# class PassengersForm(forms.ModelForm):
#     class Meta:
#         model = Passengers
#         fields = ('preferred_card_number', 'preferred_billing_address')

# class RegisterForm(UserCreationForm):
#     # first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
#     # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
#     preferred_card_number = forms.CharField(max_length=16, required=True)
#     preferred_billing_address = forms.CharField(max_length=100, required=True)
    
#     class Meta:
#         model = User
#         fields = 'username', 'first_name', 'last_name', 'email'

class PassengersForm(UserCreationForm):
    preferred_card_number = forms.CharField(max_length=16, required=True)
    preferred_billing_address = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'preferred_card_number', 'preferred_billing_address',)