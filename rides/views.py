from rest_framework import generics
from rides.models import Ride, Passenger
from rides.serializers import RideSerializer
from rides.tables import RideTable, MyTable, JoinedTable
from rides.forms import SignUpForm
from rides.forms import RideForm

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import RequestConfig

from templated_email import send_templated_mail

import datetime
from datetime import date
from datetime import timedelta



AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class AvaliableRides(LoginRequiredMixin, APIView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ridelist.html'

    def get(self, request):
        startdate = date.today()
        enddate = startdate + timedelta(days=60)
        table = RideTable(Ride.objects.filter(meetup_time__range=[startdate, enddate]))
        RequestConfig(request, paginate=False).configure(table)
        return render(request, 'ridelist.html', {'table': table})
        # return Response({'table': table})

class MyRides(LoginRequiredMixin, APIView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'myrides.html'

    def get(self, request):
        user = request.user
        table = MyTable(Ride.objects.filter(creator=user))
        RequestConfig(request, paginate=False).configure(table)
        # queryset1 = Ride.objects.filter(riders=request.user.id).exists()
        return render(request, 'myrides.html', {'table': table})

class JoinedRides(LoginRequiredMixin, APIView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'joinedrides.html'

    def get(self, request):
        user = request.user
        # queryset = Passenger.objects.filter(rider=request.user)
        table = JoinedTable(Passenger.objects.filter(rider=request.user))
        RequestConfig(request, paginate=False).configure(table)
        # queryset1 = Ride.objects.filter(riders=request.user.id).exists()
        return render(request, 'joinedrides.html', {'table': table})


# class UserList(generics.ListCreateAPIView):
# 	"""
# 	API endpoint for listing and creating User objects
# 	"""
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

class RideList(generics.ListCreateAPIView):
	"""
	API endpoint for listing and creating Ride objects
	"""
	queryset = Ride.objects.all()
	serializer_class = RideSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
# 	"""
# 	API endpoint for listing and creating User objects
# 	"""
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

class RideDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	API endpoint for listing and creating Ride objects
	"""
	queryset = Ride.objects.all()
	serializer_class = RideSerializer

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def create(request):
    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.meetup = form['meetup_time']
            post.save()
            Passenger.objects.create(rider=request.user, ride=post)
            return redirect('ridelist')
    else:
        form = RideForm()
    return render(request, 'createride.html', {'form': form})

@login_required(login_url='/login/')
def ridedetail(request, pk):
    try:
        ride = Ride.objects.get(pk = pk);
        riders = Passenger.objects.filter(ride=pk);
    except Ride.DoesNotExist:
        raise Http404("Ride Does Not Exist")
    return render(request, 'ridedetail.html', {'ride': ride, 'riders':riders})

@login_required(login_url='/login/')
def userdetail(request, username):
    user = User.objects.get(username=username)
    return render(request, 'userdetail.html', {"user":user})

@login_required(login_url='/login/')
def deleteride(request, pk):
    try:
        Ride.objects.filter(pk=pk).delete()
    except Ride.DoesNotExist:
        raise Http404("Ride Does Not Exist")
    return render(request, 'delete.html')

@login_required(login_url='/login/')
def leaveride(request, pk):
    try:
        Passenger.objects.filter(ride=pk, rider=request.user).delete()
        ride = Ride.objects.get(pk=pk)
        ride.seats_avaliable = ride.seats_avaliable + 1
        ride.save()
    except Passenger.DoesNotExist:
        raise Http404("Could not leave!")
    return render(request, 'leave.html')


@login_required(login_url='/login/')
def addrider(request, pk):
    try:
    	ride = Ride.objects.get(pk=pk)
    	riders = Passenger.objects.filter(ride=pk)
    	seats_taken = riders.count()
    	if seats_taken != ride.total_seats:
            Passenger.objects.create(rider=request.user, ride=ride)
            ride.seats_avaliable = ride.seats_avaliable - 1
            creator = User.objects.get(username__iexact=ride.creator)
            creator_email = creator.email
            send_templated_mail(
                template_name='joined',
                from_email='noreply@unirideshare.xyz',
                recipient_list=[creator.email],
                context={
                    'destination':ride.destination,
                    'creator_username':creator.username,
                    'joined_username':request.user.username,
                    'ridepk':pk,
                    'creator_full_name':creator.get_full_name(),
                },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
            )
            ride.save()
    	else:
        	return render(request, 'ridedetail.html', {
        		'ride': ride,
        		'riders':riders,
        		'error_message': "No Room!",
        	})  		
    except IntegrityError:
        return render(request, 'ridedetail.html', {
            'ride': ride,
            'riders':riders,
            'error_message': "Your're Already In!",
        })
    return render(request, 'ridedetail.html', {'ride': ride, 'riders':riders, 'error_message': "Your're In!"})
