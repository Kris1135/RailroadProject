from django.contrib import admin
from Application.models import FareTypes, Passengers, Reservations, SeatsFree, Segments, Stations, StopsAt, Trains, Trips

# Register your models here.
admin.site.register(FareTypes)
admin.site.register(Passengers)
admin.site.register(Reservations)
admin.site.register(SeatsFree)
admin.site.register(Segments)
admin.site.register(Stations)
admin.site.register(StopsAt)
admin.site.register(Trains)
admin.site.register(Trips)
