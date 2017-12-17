from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from django.db import connection
import datetime

from .forms import PassengersForm, SearchForm
from .models import Search
# Create your views here.
# def index(request):
#     return render(request, 'index.html')

def index(request):
    if request.user.is_authenticated():
        return render(request, 'about.html')

    if request.method == 'POST':
        form = PassengersForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.passengers.preferred_card_number = form.cleaned_data.get('preferred_card_number')
            user.passengers.preferred_billing_address = form.cleaned_data.get('preferred_billing_address')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('about')
    else:
        form = PassengersForm()
    return render(request, 'index.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def book(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #Process data...
            tod = form.cleaned_data.get('time_of_day')
            day = form.cleaned_data.get('reserve_day')
            strt = form.cleaned_data.get('start_loc')
            end = form.cleaned_data.get('end_loc')

            srch = Search.reservations(tod,day,strt,end)
            train_ids = []
            departs = []
            strts = []
            arrivs = []
            ends = [] 
            days = []
            seats = []
            prices = []
            for x in srch:
                train_ids.append( x[0] )
                departs.append( x[1].strftime('%H:%M:%S') )
                strts.append(x[2])
                arrivs.append( x[3].strftime('%H:%M:%S') )
                ends.append(x[4])
                days.append(x[5].strftime('%m/%d/%Y'))
                seats.append(x[6])
                prices.append( float(x[7]) )
            context = {
                'train_id' : train_ids,
                'departure' : departs,
                'start' : strts,
                'arrival' : arrivs,
                'end' : ends ,
                'date' : days ,
                'free_seats' : seats,
                'price' : prices
            }
            for x in srch:
                print(x)
            return render(request, 'book_reservation.html', {'form': form, 'context': context})
    else:
        form = SearchForm()
    return render(request, 'book_reservation.html', {'form': form})

def current(request):
    return render(request, 'current_reservations.html')

        
