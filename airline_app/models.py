from django.db import models
import uuid


class Airport(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.airport_name} ({self.location}, {self.country})"


class Aircraft(models.Model):
    aircraft_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.model} ({self.airline})"


class CrewMember(models.Model):
    ROLE_CHOICES = [
        ('PILOT', 'Pilot'),
        ('CO_PILOT', 'Co-Pilot'),
        ('FLIGHT_ATTENDANT', 'Flight Attendant'),
        ('ENGINEER', 'Engineer'),
    ]

    crew_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    contact_information = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_number = models.CharField(max_length=10, unique=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    source_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='departing_flights')
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='arriving_flights')
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.CASCADE, related_name='flights')
    crew = models.ManyToManyField(CrewMember, related_name='flights')

    def __str__(self):
        return f"{self.flight_number}: {self.source_airport.airport_name} to {self.destination_airport.airport_name}"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='schedules')
    staff = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"Schedule for {self.flight.flight_number} on {self.date}"


class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    passenger_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    passport_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} (Passport: {self.passport_number})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=5)
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"Booking {self.booking_id} - {self.passenger.name} on {self.flight.flight_number}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]

    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=15, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment')

    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount} for Booking {self.booking.booking_id}"


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    seat_number = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=10)
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='tickets')
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='ticket')

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.passenger.name} on {self.flight.flight_number}"


class Baggage(models.Model):
    BAGGAGE_TYPE_CHOICES = [
        ('CABIN', 'Cabin'),
        ('CHECKED', 'Checked'),
        ('OVERSIZED', 'Oversized'),
    ]

    baggage_id = models.AutoField(primary_key=True)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Weight in kg")
    type = models.CharField(max_length=10, choices=BAGGAGE_TYPE_CHOICES)
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name='baggage')

    def __str__(self):
        return f"{self.get_type_display()} Baggage ({self.weight}kg) for {self.passenger.name}"


class BoardingPass(models.Model):
    boarding_pass_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='boarding_pass')
    gate_number = models.CharField(max_length=5)
    boarding_time = models.DateTimeField()
    seat_number = models.CharField(max_length=5)
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='boarding_passes')
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name='boarding_passes')
    barcode = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boarding Pass {self.boarding_pass_id} - {self.passenger.name} on {self.flight.flight_number}"
