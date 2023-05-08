import pytz
from django.db.models import Count

from .models import FlightInfo, PassengerSeatInfo, Booking
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from threading import Timer
import datetime

timers = {}


@api_view(['GET'])
def flights_available(request, departure, destination, date, seat_class, adult_ticket, child_ticket):
    try:
        flights = FlightInfo.objects.filter(departure_airport=departure, destination_airport=destination,
                                            departure_date__date=date).values('id', 'flight_number', 'departure_airport',
                                                                              'destination_airport', 'departure_date',
                                                                              'arrival_date', 'flight_price')
    except FlightInfo.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    number_of_tickets = adult_ticket+child_ticket
    flight_data = []
    for flight in flights:
        id = flight['id']
        flight_number = flight['flight_number']
        departure_airport = flight['departure_airport']
        destination_airport = flight['destination_airport']
        departure_date = flight['departure_date']
        arrival_date = flight['arrival_date']
        flight_price = flight['flight_price']
        flight_duration = arrival_date - departure_date
        flight_duration_str = str(flight_duration - timedelta(microseconds=flight_duration.microseconds))

        seat_data = []
        passenger_seats = PassengerSeatInfo.objects.filter(flight_id=id, seat_class=seat_class, reserved=False).values(
            'code', 'seat_class')
        for seat in passenger_seats:
            code = seat['code']
            seat_dict = {'code': code}
            seat_data.append(seat_dict)
        if len(seat_data) < number_of_tickets:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if seat_class == 'Economy':
            total_price = flight_price * (adult_ticket + 0.8 * child_ticket)
        elif seat_class == 'Business':
            total_price = flight_price * 1.3 * (adult_ticket + 0.8 * child_ticket)

        flight_dict = {
            'id': id,
            'flight_number': flight_number,
            'seats_available': seat_data,
            'departure_airport': departure_airport,
            'destination_airport': destination_airport,
            'departure_date': departure_date,
            'arrival_date': arrival_date,
            'duration': flight_duration_str,
            'price': total_price
        }

        flight_data.append(flight_dict)
    if not flight_data:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(flight_data, safe=False)


def release_seat_cancel_booking(passenger_seats, booking_id):
    booking = Booking.objects.get(id=booking_id)
    for seat in passenger_seats:
        if seat.reserved:
            seat.reserved = False
            seat.save()
    booking.delete()


@api_view(['POST'])
def seat_selection(request, flight_number, seat_codes):
    try:
        seat_list = seat_codes.split(',')
        flight_id = FlightInfo.objects.filter(flight_number=flight_number).values('id').first()['id']
        passenger_seats = PassengerSeatInfo.objects.filter(flight_id=flight_id, code__in=seat_list)

        booking = Booking.objects.create(number_tickets=len(passenger_seats))
        for seat in passenger_seats:
            if seat.reserved:
                booking.delete()
                return HttpResponse(status=status.HTTP_306_RESERVED)
            if not seat.reserved:
                seat.reserved = True
                seat.booking_id = booking
                seat.save()
                timer = Timer(1200, release_seat_cancel_booking, args=(passenger_seats, booking.id))
                timers[booking.id] = timer
                timer.start()
    except PassengerSeatInfo.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(booking.id)


@api_view(['POST'])
def confirm_booking(request, booking_id):
    timer = timers.get(booking_id)
    if timer:
        timer.cancel()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.filter(id=booking_id)[0]
        seat = PassengerSeatInfo.objects.filter(booking_id=booking)[0]
        departure_time = seat.flight.departure_date.replace(tzinfo=pytz.UTC)  # make departure_time offset-aware
        time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)  # make time_now offset-aware
        time_diff = departure_time - time_now
        print(time_diff)
        print(datetime.timedelta(hours=48))
        if time_diff > datetime.timedelta(hours=48):
            passenger_seats = PassengerSeatInfo.objects.filter(booking_id=booking)

            for seat in passenger_seats:
                print(seat)
                seat.reserved = False
                seat.save()
            booking.delete()

    except Booking.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(status=status.HTTP_200_OK)