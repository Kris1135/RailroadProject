# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models, connection 
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

class FareTypes(models.Model):
    fare_id = models.AutoField(primary_key=True)
    fare_name = models.CharField(max_length=20, blank=True, null=True)
    rate = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_types'


class Passengers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passenger_id = models.AutoField(primary_key=True)
    #fname = models.CharField(max_length=30, blank=True, null=True)
    #lname = models.CharField(max_length=100, blank=True, null=True)
    #email = models.CharField(max_length=100, blank=True, null=True)
    #password = models.CharField(max_length=100, blank=True, null=True)
    preferred_card_number = models.CharField(max_length=16, blank=True, null=True)
    preferred_billing_address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passengers'     

@receiver(post_save, sender=User)
 

def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Passengers.objects.create(user=instance)
    instance.passengers.save()

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    reservation_date = models.DateTimeField(blank=True, null=True)
    paying_passenger = models.ForeignKey(Passengers, models.DO_NOTHING)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    billing_address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservations'


class SeatsFree(models.Model):
    train = models.OneToOneField('Trains', models.DO_NOTHING, primary_key=True)
    segment = models.ForeignKey('Segments', models.DO_NOTHING)
    seat_free_date = models.DateField()
    freeseat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seats_free'
        unique_together = (('train', 'segment', 'seat_free_date'),)


class Segments(models.Model):
    segment_id = models.AutoField(primary_key=True)
    seg_n_end = models.ForeignKey('Stations', models.DO_NOTHING, db_column='seg_n_end', related_name = 'seg_n_end')
    seg_s_end = models.ForeignKey('Stations', models.DO_NOTHING, db_column='seg_s_end', related_name = 'seg_s_end')
    seg_fare = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'segments'


class Stations(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=40)
    station_symbol = models.CharField(unique=True, max_length=3)

    def __str__ (self):
        return self.station_name

    class Meta:
        managed = False
        db_table = 'stations'


class StopsAt(models.Model):
    train = models.OneToOneField('Trains', models.DO_NOTHING, primary_key=True)
    station = models.ForeignKey(Stations, models.DO_NOTHING)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stops_at'
        unique_together = (('train', 'station'),)


class Trains(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_start = models.ForeignKey(Stations, models.DO_NOTHING, db_column='train_start', related_name = 'train_start')
    train_end = models.ForeignKey(Stations, models.DO_NOTHING, db_column='train_end', related_name = 'train_end')
    train_direction = models.IntegerField(blank=True, null=True)
    train_days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trains'


class Trips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_date = models.DateField()
    trip_seg_start = models.ForeignKey(Segments, models.DO_NOTHING, db_column='trip_seg_start', related_name = 'trip_seg_start')
    trip_seg_ends = models.ForeignKey(Segments, models.DO_NOTHING, db_column='trip_seg_ends', related_name = 'trip_seg_ends')
    fare_type = models.ForeignKey(FareTypes, models.DO_NOTHING, db_column='fare_type')
    fare = models.DecimalField(max_digits=7, decimal_places=2)
    trip_train = models.ForeignKey(Trains, models.DO_NOTHING)
    reservation = models.ForeignKey(Reservations, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'trips'

class Reservation_conn(models.Model):
    time_choice = (
        (0, 'Morning'),
        (1, 'Afternoon'),
        (2, 'Evening'),
        (3, 'Night'),
    )

    time_of_day = models.IntegerField(blank=True, null=True, choices = time_choice)
    reserve_day = models.DateField()
    start_loc = models.ForeignKey(Stations, related_name='StartLoc')
    end_loc = models.ForeignKey(Stations, related_name='EndLoc')

    def search(tod, day, strt, end):
        cur = connection.cursor()
        cur.callproc('filter_res', (tod, day, strt, end) )
        try:
            results = cur.fetchall()
        finally:
            cur.close()
        return results

    def book_reservation(pass_id, train_id, date, strt_time, end_time, start_loc, end_loc, price):
        cur = connection.cursor()
        cur.callproc('book_res', (pass_id, train_id, date, strt_time, end_time, start_loc, end_loc, price) )

        try:
            results = cur.fetchall()
        finally:
            cur.close()
        return results

    def curr_reservation(pass_id):
        cur = connection.cursor()
        cur.callproc('curr_reservations', (pass_id,))
        try:
            results = cur.fetchall()
        finally:
            cur.close()
        return results

    def del_reservation(pass_id, reserve_id):
        cur = connection.cursor()
        cur.callproc('delete_res', (pass_id,reserve_id,))
        try:
            results = cur.fetchall()
        finally:
            cur.close()
        return results

    def edit_reservation(res_id, train, booking_date, trip_start, trip_end, start_txt, end_txt, price):
        cur = connection.cursor()
        cur.callproc('edit_res', (res_id, train, booking_date, trip_start, trip_end, start_txt, end_txt, price,))
        try:
            results = cur.fetchall()
        finally:
            cur.close()
        return results

