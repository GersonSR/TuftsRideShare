from django.contrib import admin

from rides.models import Ride, RideAdmin

# admin.site.register(User, UserAdmin)
admin.site.register(Ride, RideAdmin)