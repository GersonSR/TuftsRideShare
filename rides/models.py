import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# class User(models.Model):
# 	username = models.CharField(max_length = 200, unique=True)
# 	date_created = models.DateTimeField(auto_now_add=True, blank=True)
# 	email = models.CharField(max_length = 200, unique=True)
# 	password = models.CharField(max_length = 200)
# 	def __str__(self):
# 		return self.email

class Ride(models.Model):
	total_seats = models.IntegerField()
	seats_avaliable = models.IntegerField()
	destination = models.CharField(max_length = 200)
	date_created = models.DateTimeField(auto_now_add=True, blank=True)
	meetup_location = models.CharField(default= 'N/A', max_length = 200)
	meetup_time = models.DateTimeField(default= '2017/01/01 11:59')
	transportation_type = models.CharField(default="Personal Car", max_length = 200)
	total_cost = models.DecimalField(default = 10.0, max_digits=10, decimal_places=2)
	cost_per_person = models.DecimalField(default = 10.0, max_digits=10, decimal_places=2)
	creator = models.CharField(max_length = 200, default = 'N/A')
	riders = models.ManyToManyField(AUTH_USER_MODEL, through='Passenger')

	def __str__(self):
		return self.destination

class Passenger(models.Model):
	rider = models.ForeignKey(AUTH_USER_MODEL,  related_name='rider', on_delete=models.CASCADE)
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('rider', 'ride',)
	
class PassengerInline(admin.TabularInline):
	model = Passenger
	extra = 1

class RideAdmin(admin.ModelAdmin):
	inlines = (PassengerInline,)	
	
# class UserAdmin(admin.ModelAdmin):
# 	inlines = (DestinationInline,)

def regions_changed(sender, **kwargs):
	if kwargs['instance'].riders.count() > total_seats:
		raise ValidationError("No more room!")
m2m_changed.connect(regions_changed, sender=Ride.riders.through)