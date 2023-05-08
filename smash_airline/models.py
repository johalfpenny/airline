from django.db import models


class Airport(models.Model):
    code = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.code + "-" + self.name


class FlightInfo(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    flight_price = models.FloatField()

    def __str__(self):
        return f"{self.departure_date} - {self.flight_number} - {self.departure_airport} -> {self.destination_airport}"


class Booking(models.Model):
    # id = models.OneToOneField(PassengerSeatInfo, on_delete=models.CASCADE, primary_key=True, related_name='booking')
    passenger_type = models.CharField(max_length=25, default=None, blank=True, null=True)
    email = models.CharField(max_length=50, default=None, null=True)
    transaction_id = models.IntegerField(default=None, null=True)
    number_tickets = models.IntegerField(default=None, null=True)
    seat_class = models.CharField(max_length=20, default=None, null=True)
    total_price = models.FloatField(default=None, null=True)
    cancelled = models.BooleanField(default=False)


class PassengerSeatInfo(models.Model):
    code = models.CharField(max_length=4)
    first_name = models.CharField(max_length=25, default=None, blank=True)
    surname = models.CharField(max_length=25, default=None, blank=True)
    seat_class = models.CharField(max_length=20)
    price = models.FloatField()
    passenger_type = models.CharField(max_length=10, default=None, blank=True)
    reserved = models.BooleanField(default=False)
    booking_id = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    flight = models.ForeignKey(FlightInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.flight}"

