from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from django.db import connection
from django.http import JsonResponse
import datetime

from decimal import Decimal, getcontext
from .forms import PassengersForm, SearchForm, BookForm, DeleteForm
from .models import Reservation_conn
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

def search(request):
    if request.method == 'POST' and 'bookForm_submit' in request.POST:
        bookForm = BookForm(request.POST)
        print('\n')
        print(bookForm.is_valid())
        print(request.POST.get("start_loc1", ""))
        print(type(request.POST.get("start_loc1", "")))
        #Process data...
        form_data = bookForm.cleaned_data
        price = form_data['price'] 
        strt_time = form_data['departure']
        end_time = form_data['arrival']
        train_id = form_data['train']
        start_loc = form_data['start_loc1']
        end_loc = form_data['end_loc1']   
        date = form_data['res_day']
        pass_id = request.user.id
        exec_sp = Reservation_conn.book_reservation(pass_id, train_id, date, strt_time, end_time, start_loc, end_loc, price)
        print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERE")
        return redirect(current)
         
    else:
        bookForm = BookForm()

    if request.method == 'POST' and 'searchForm_submit' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            #Process data...
            tod = form.cleaned_data.get('time_of_day')
            day = form.cleaned_data.get('reserve_day')
            strt = form.cleaned_data.get('start_loc')
            end = form.cleaned_data.get('end_loc')

            srch = Reservation_conn.search(tod,day,strt,end)
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
            # for x in srch:
            #     print(x)
            return render(request, 'book_reservation.html', {'form': form, 'bookForm': bookForm, 'context': context})        

    else:
        form = SearchForm()


    return render(request, 'book_reservation.html', {'form': form, 'bookForm': bookForm})        

def current(request):
    pass_id = request.user.id 
    exec_sp1 = Reservation_conn.curr_reservation(pass_id)
    
    res_id = []
    res_date = []
    trip_date = []
    start_loc = []
    end_loc = []
    price = []
    train = []
    strt_time = []
    end_time = []
    card = []
    addr = []
    #Clean data for table...
    for x in exec_sp1:
        res_id.append( x[0] )
        res_date.append( x[1].strftime('%H:%M:%S %m/%d/%Y') )
        trip_date.append( x[2].strftime('%m/%d/%Y') )
        start_loc.append( x[3] )
        end_loc.append( x[4] )
        price.append( float(x[5]) )
        train.append(x[6])
        strt_time.append( x[7].strftime('%H:%M:%S') )
        end_time.append( x[8].strftime('%H:%M:%S') )
        card.append( x[9] )
        addr.append( x[10] )

    context = {
        'reserve_id' : res_id,
        'reserve_date' :res_date,
        'trip_date':trip_date,
        'start_loc':start_loc,
        'end_loc':end_loc,
        'price':price,
        'train':train,
        'strt_time': strt_time,
        'end_time': end_time,
        'card': card,
        'addr': addr,
    }

    # Delete reservation process...
    if request.method == 'POST' and 'deleteConfirm' in request.POST:
        deleteForm = DeleteForm(request.POST)
        if deleteForm.is_valid():
            res_id = deleteForm.cleaned_data['reserve_id']
            del_sp = Reservation_conn.del_reservation(pass_id, res_id)
        return redirect('current')
    else:
        deleteForm = DeleteForm()

    chcksrch = request.POST.get("action", "")
    if request.method == 'POST' and ('searchForm_submit' == chcksrch):
        form = SearchForm(request.POST)
        #Process data...
        tod = request.POST.get("time_of_day", "")
        dayconv = request.POST.get("reserve_day", "")
        day = datetime.datetime.strptime(dayconv, '%m/%d/%Y')
        strt = request.POST.get("start_loc", "")
        end = request.POST.get("end_loc", "")
        srch = Reservation_conn.search(tod,day,strt,end)
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

        print(train_ids)
        context1 = {
            'train_id' : train_ids,
            'departure' : departs,
            'start' : strts,
            'arrival' : arrivs,
            'end' : ends ,
            'date' : days ,
            'free_seats' : seats,
            'price' : prices
        }
        # for x in srch:
        #     print(x)
        return JsonResponse(context1)
        #return render(request, 'current_reservations.html', {'context': context, 'deleteForm': deleteForm, 'form': form, 'context1': context1,})    

    else:
        form = SearchForm()

    return render(request, 'current_reservations.html', {'context': context, 'deleteForm': deleteForm, 'form': form, })

def edit(request):
    if request.method == 'POST':
        #Process data...
        res = request.POST.get("reservation_id", "")
        train = request.POST.get("train", "")
        dayconv = request.POST.get("reservation_day", "")
        day = datetime.datetime.strptime(dayconv, '%m/%d/%Y')
        strt_time = request.POST.get("departure", "")
        end_time = request.POST.get("arrival", "")
        strt = request.POST.get("start_location", "")
        end = request.POST.get("end_location", "")
        getcontext().prec = 2
        price = Decimal(request.POST.get("fare", ""))
        print(price)
        print(price)
        subm = Reservation_conn.edit_reservation(res, train, day, strt_time, end_time, strt, end, price)
        return redirect('current')

    return redirect('current')
