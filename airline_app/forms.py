from django import forms
from .models import *


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'date_of_birth', 'gender', 'email',
                  'phone_number', 'passport_number', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'departure_time', 'arrival_time',
                  'source_airport', 'destination_airport', 'aircraft', 'crew']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'crew': forms.CheckboxSelectMultiple(),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger', 'flight', 'seat_number', 'status']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_method']


class BoardingPassForm(forms.ModelForm):
    class Meta:
        model = BoardingPass
        fields = ['booking', 'gate_number', 'boarding_time', 'seat_number']
        widgets = {
            'boarding_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BaggageForm(forms.ModelForm):
    class Meta:
        model = Baggage
        fields = ['passenger', 'weight', 'type']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['flight', 'date', 'time', 'staff']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
