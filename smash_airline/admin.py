from django.contrib import admin
from .models import FlightInfo, Airport, PassengerSeatInfo, Booking

admin.site.register(FlightInfo)
admin.site.register(Airport)
admin.site.register(PassengerSeatInfo)
admin.site.register(Booking)
