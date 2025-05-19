from django.contrib import admin
from .models import *

class BaggageInline(admin.TabularInline):
    model = Baggage
    extra = 1

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class BoardingPassInline(admin.TabularInline):
    model = BoardingPass
    extra = 0

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'passport_number', 'email', 'phone_number')
    search_fields = ('name', 'passport_number', 'email')
    inlines = [BaggageInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'passenger', 'flight', 'seat_number', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('passenger__name', 'flight__flight_number')
    inlines = [TicketInline, PaymentInline, BoardingPassInline]

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'source_airport', 'destination_airport', 'departure_time', 'arrival_time')
    list_filter = ('source_airport', 'destination_airport')
    search_fields = ('flight_number',)
    date_hierarchy = 'departure_time'

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('model', 'airline', 'capacity', 'manufacturer')
    list_filter = ('airline', 'manufacturer')
    search_fields = ('model', 'airline')

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'airline', 'experience')
    list_filter = ('role', 'airline')
    search_fields = ('name',)

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('airport_name', 'location', 'country')
    list_filter = ('country',)
    search_fields = ('airport_name', 'location')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('flight', 'date', 'time')
    list_filter = ('date',)
    date_hierarchy = 'date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'passenger', 'flight', 'seat_number', 'price')
    list_filter = ('flight',)
    search_fields = ('passenger__name', 'flight__flight_number')

@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
    list_display = ('baggage_id', 'passenger', 'type', 'weight')
    list_filter = ('type',)

@admin.register(BoardingPass)
class BoardingPassAdmin(admin.ModelAdmin):
    list_display = ('boarding_pass_id', 'passenger', 'flight', 'gate_number', 'boarding_time')
    search_fields = ('passenger__name', 'flight__flight_number', 'barcode')
