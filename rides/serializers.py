from rest_framework import serializers
from rides.models import Ride, Passenger

# class UserSerializer(serializers.ModelSerializer):	
# 	class Meta:
# 		model = User
# 		fields = ('id','username', 'date_created', 'email', 'password')

class RideSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Ride
		fields = ('id','total_seats', 'destination_text', 'date_created','riders')

class PassengerSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Passenger
		fields = ('rider', 'ride')