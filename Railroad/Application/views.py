from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import UserForm, PassengersForm
from django.db import transaction

# Create your views here.
# def index(request):
#     return render(request, 'index.html')

def index(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pass_form = PassengersForm(request.POST)
        if user_form.is_valid() and pass_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            pass_ = pass_form.save()
            pass_.refresh_from_db()
            pass_.save()
            raw_password = user_form.cleaned_data.get('password')
            #user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        user_form = UserForm()
        pass_form = PassengersForm()
    return render(request, 'index.html', {'user_form': user_form, 'pass_form': pass_form})

