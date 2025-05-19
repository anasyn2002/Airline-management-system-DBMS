from django.core.management.base import BaseCommand
from django.utils import timezone
from airline_app.models import *
import random
import datetime

class Command(BaseCommand):
    help = 'Creates sample data for the airline management system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create Airports
        airports_data = [
            {'airport_name': 'JFK International', 'location': 'New York', 'country': 'USA'},
            {'airport_name': 'Heathrow', 'location': 'London', 'country': 'UK'},
            {'airport_name': 'Charles de Gaulle', 'location': 'Paris', 'country': 'France'},
            {'airport_name': 'Dubai International', 'location': 'Dubai', 'country': 'UAE'},
            {'airport_name': 'Changi', 'location': 'Singapore', 'country': 'Singapore'},
        ]
        
        airports = []
        for data in airports_data:
            airport, created = Airport.objects.get_or_create(**data)
            airports.append(airport)
            if created:
                self.stdout.write(f'Created airport: {airport.airport_name}')
        
        # Create Aircraft
        aircraft_data = [
            {'model': 'Boeing 747', 'capacity': 366, 'manufacturer': 'Boeing', 'airline': 'Delta'},
            {'model': 'Airbus A380', 'capacity': 525, 'manufacturer': 'Airbus', 'airline': 'Emirates'},
            {'model': 'Boeing 787', 'capacity': 280, 'manufacturer': 'Boeing', 'airline': 'British Airways'},
            {'model': 'Airbus A320', 'capacity': 180, 'manufacturer': 'Airbus', 'airline': 'Air France'},
        ]
        
        aircrafts = []
        for data in aircraft_data:
            aircraft, created = Aircraft.objects.get_or_create(**data)
            aircrafts.append(aircraft)
            if created:
                self.stdout.write(f'Created aircraft: {aircraft.model}')
        
        # Create Crew Members
        crew_data = [
            {'name': 'John Smith', 'role': 'PILOT', 'experience': 15, 'contact_information': 'john@airline.com', 'airline': 'Delta'},
            {'name': 'Jane Doe', 'role': 'CO_PILOT', 'experience': 8, 'contact_information': 'jane@airline.com', 'airline': 'Delta'},
            {'name': 'Emma Wilson', 'role': 'FLIGHT_ATTENDANT', 'experience': 5, 'contact_information': 'emma@airline.com', 'airline': 'British Airways'},
            {'name': 'Michael Brown', 'role': 'PILOT', 'experience': 12, 'contact_information': 'michael@airline.com', 'airline': 'Emirates'},
        ]
        
        crew_members = []
        for data in crew_data:
            crew, created = CrewMember.objects.get_or_create(**data)
            crew_members.append(crew)
            if created:
                self.stdout.write(f'Created crew member: {crew.name}')
        
        # Create Flights
        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)
        
        flight_data = [
            {
                'flight_number': 'DL123',
                'departure_time': now.replace(hour=10, minute=0),
                'arrival_time': now.replace(hour=14, minute=0),
                'source_airport': airports[0],
                'destination_airport': airports[1],
                'aircraft': aircrafts[0]
            },
            {
                'flight_number': 'BA456',
                'departure_time': now.replace(hour=13, minute=30),
                'arrival_time': now.replace(hour=15, minute=45),
                'source_airport': airports[1],
                'destination_airport': airports[2],
                'aircraft': aircrafts[2]
            },
            {
                'flight_number': 'EK789',
                'departure_time': tomorrow.replace(hour=8, minute=15),
                'arrival_time': tomorrow.replace(hour=20, minute=30),
                'source_airport': airports[3],
                'destination_airport': airports[4],
                'aircraft': aircrafts[1]
            }
        ]
        
        flights = []
        for data in flight_data:
            flight, created = Flight.objects.get_or_create(**data)
            if created:
                # Add crew to flight
                for crew in random.sample(crew_members, min(2, len(crew_members))):
                    flight.crew.add(crew)
                flights.append(flight)
                self.stdout.write(f'Created flight: {flight.flight_number}')
        
        # Create Passengers
        passenger_data = [
            {'name': 'Alice Johnson', 'date_of_birth': '1985-05-15', 'gender': 'F', 'email': 'alice@example.com', 'phone_number': '1234567890', 'passport_number': 'AB123456', 'address': '123 Main St, New York'},
            {'name': 'Bob Williams', 'date_of_birth': '1990-10-20', 'gender': 'M', 'email': 'bob@example.com', 'phone_number': '0987654321', 'passport_number': 'CD789012', 'address': '456 Oak Ave, London'},
            {'name': 'Charlie Davis', 'date_of_birth': '1978-03-08', 'gender': 'M', 'email': 'charlie@example.com', 'phone_number': '5551237890', 'passport_number': 'EF345678', 'address': '789 Pine Blvd, Paris'},
        ]
        
        passengers = []
        for data in passenger_data:
            # Convert date string to date object
            data['date_of_birth'] = datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            passenger, created = Passenger.objects.get_or_create(**data)
            passengers.append(passenger)
            if created:
                self.stdout.write(f'Created passenger: {passenger.name}')
        
        # Create Bookings
        booking_data = [
            {'passenger': passengers[0], 'flight': flights[0], 'seat_number': '12A', 'status': 'CONFIRMED'},
            {'passenger': passengers[1], 'flight': flights[0], 'seat_number': '14B', 'status': 'CONFIRMED'},
            {'passenger': passengers[2], 'flight': flights[1], 'seat_number': '8C', 'status': 'PENDING'},
        ]
        
        bookings = []
        for data in booking_data:
            booking, created = Booking.objects.get_or_create(**data)
            bookings.append(booking)
            if created:
                self.stdout.write(f'Created booking for {booking.passenger.name} on {booking.flight.flight_number}')
        
        # Create Tickets
        ticket_data = [
            {'seat_number': '12A', 'price': 350.00, 'booking_status': 'CONFIRMED', 'passenger': passengers[0], 'flight': flights[0], 'booking': bookings[0]},
            {'seat_number': '14B', 'price': 350.00, 'booking_status': 'CONFIRMED', 'passenger': passengers[1], 'flight': flights[0], 'booking': bookings[1]},
            {'seat_number': '8C', 'price': 450.00, 'booking_status': 'PENDING', 'passenger': passengers[2], 'flight': flights[1], 'booking': bookings[2]},
        ]
        
        tickets = []
        for data in ticket_data:
            ticket, created = Ticket.objects.get_or_create(**data)
            tickets.append(ticket)
            if created:
                self.stdout.write(f'Created ticket for {ticket.passenger.name}')
        
        # Create Payments
        payment_data = [
            {'amount': 350.00, 'payment_method': 'CREDIT_CARD', 'booking': bookings[0]},
            {'amount': 350.00, 'payment_method': 'PAYPAL', 'booking': bookings[1]},
        ]
        
        payments = []
        for data in payment_data:
            payment, created = Payment.objects.get_or_create(**data)
            payments.append(payment)
            if created:
                self.stdout.write(f'Created payment for booking {payment.booking.booking_id}')
        
        # Create Baggage
        baggage_data = [
            {'weight': 23.5, 'type': 'CHECKED', 'passenger': passengers[0]},
            {'weight': 8.0, 'type': 'CABIN', 'passenger': passengers[0]},
            {'weight': 18.7, 'type': 'CHECKED', 'passenger': passengers[1]},
        ]
        
        baggage_list = []
        for data in baggage_data:
            baggage, created = Baggage.objects.get_or_create(**data)
            baggage_list.append(baggage)
            if created:
                self.stdout.write(f'Created baggage for {baggage.passenger.name}')
        
        # Create Boarding Passes
        boarding_pass_data = [
            {
                'booking': bookings[0],
                'gate_number': 'G12',
                'boarding_time': now.replace(hour=9, minute=0),
                'seat_number': '12A',
                'flight': flights[0],
                'passenger': passengers[0],
                'barcode': 'BP12345678'
            },
            {
                'booking': bookings[1],
                'gate_number': 'G12',
                'boarding_time': now.replace(hour=9, minute=0),
                'seat_number': '14B',
                'flight': flights[0],
                'passenger': passengers[1],
                'barcode': 'BP87654321'
            }
        ]
        
        boarding_passes = []
        for data in boarding_pass_data:
            boarding_pass, created = BoardingPass.objects.get_or_create(**data)
            boarding_passes.append(boarding_pass)
            if created:
                self.stdout.write(f'Created boarding pass for {boarding_pass.passenger.name}')
        
        # Create Schedules
        schedule_data = [
            {'date': now.date(), 'time': now.time().replace(hour=10, minute=0), 'flight': flights[0], 'staff': 'Team A'},
            {'date': now.date(), 'time': now.time().replace(hour=13, minute=30), 'flight': flights[1], 'staff': 'Team B'},
            {'date': tomorrow.date(), 'time': tomorrow.time().replace(hour=8, minute=15), 'flight': flights[2], 'staff': 'Team C'},
        ]
        
        schedules = []
        for data in schedule_data:
            schedule, created = Schedule.objects.get_or_create(**data)
            schedules.append(schedule)
            if created:
                self.stdout.write(f'Created schedule for flight {schedule.flight.flight_number}')
        
        self.stdout.write(self.style.SUCCESS('Sample data creation complete!'))
