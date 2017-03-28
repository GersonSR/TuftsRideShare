import django_tables2 as tables
from .models import Ride, Passenger
from django_tables2.utils import A 

class RideTable(tables.Table):
    Details = tables.LinkColumn('ridedetails', text='Check out Ride!', args=[A('pk')], orderable=False, empty_values=())
    class Meta:
        model = Ride
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class MyTable(tables.Table):
    Details = tables.LinkColumn('ridedetails', text='Check out Ride!', args=[A('pk')], orderable=False, empty_values=())
    Delete = tables.LinkColumn("deleteride", text='Delete Ride!', args=[A('pk')], orderable=False, empty_values=())
    class Meta:
        model = Ride
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class JoinedTable(tables.Table):
    Ride_id = tables.Column(verbose_name='Id', accessor='ride.pk', empty_values=())
    Total_seats = tables.Column(verbose_name='Total Seats', accessor='ride.total_seats', empty_values=())
    seats_avaliable = tables.Column(verbose_name='Seats Avaliable', accessor='ride.seats_avaliable', empty_values=())
    Destination = tables.Column(verbose_name='Destination', accessor='ride.destination', empty_values=())
    Date_created = tables.Column(verbose_name='Date Created', accessor='ride.date_created', empty_values=())
    Meetup_location = tables.Column(verbose_name='Meetup Location', accessor='ride.meetup_location', empty_values=())
    Meetup_time = tables.Column(verbose_name='Meetup Time', accessor='ride.meetup_time', empty_values=())
    Transportation_type = tables.Column(verbose_name='Transportation Type', accessor='ride.transportation_type', empty_values=())
    Total_cost = tables.Column(verbose_name='Total Cost', accessor='ride.total_cost', empty_values=())
    Cost_per_person = tables.Column(verbose_name='Cost Per Person', accessor='ride.cost_per_person', empty_values=())
    Creator = tables.Column(verbose_name='Creator', accessor='ride.creator', empty_values=())
    Details = tables.LinkColumn('ridedetails', text='Check out Ride!', args=[A('ride.id')], orderable=False, empty_values=())
    Leave = tables.LinkColumn('leaveride', text='Leave Ride!', args=[A('ride.pk')], orderable=False, empty_values=())

    class Meta:
        model = Passenger
        # add class="paleblue" to <table> tag
        fields = ()
        attrs = {'class': 'paleblue'}
    