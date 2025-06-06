# Generated by Django 5.2.1 on 2025-05-18 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('aircraft_id', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('manufacturer', models.CharField(max_length=100)),
                ('airline', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_id', models.AutoField(primary_key=True, serialize=False)),
                ('airport_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CrewMember',
            fields=[
                ('crew_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('PILOT', 'Pilot'), ('CO_PILOT', 'Co-Pilot'), ('FLIGHT_ATTENDANT', 'Flight Attendant'), ('ENGINEER', 'Engineer')], max_length=20)),
                ('experience', models.PositiveIntegerField(help_text='Experience in years')),
                ('contact_information', models.CharField(max_length=100)),
                ('airline', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('passenger_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('passport_number', models.CharField(max_length=20, unique=True)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_number', models.CharField(max_length=10, unique=True)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='airline_app.aircraft')),
                ('crew', models.ManyToManyField(related_name='flights', to='airline_app.crewmember')),
                ('destination_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriving_flights', to='airline_app.airport')),
                ('source_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_flights', to='airline_app.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('seat_number', models.CharField(max_length=5)),
                ('status', models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('PENDING', 'Pending'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=10)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='airline_app.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='airline_app.passenger')),
            ],
            options={
                'unique_together': {('flight', 'seat_number')},
            },
        ),
        migrations.CreateModel(
            name='BoardingPass',
            fields=[
                ('boarding_pass_id', models.AutoField(primary_key=True, serialize=False)),
                ('gate_number', models.CharField(max_length=5)),
                ('boarding_time', models.DateTimeField()),
                ('seat_number', models.CharField(max_length=5)),
                ('barcode', models.CharField(max_length=100, unique=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='boarding_pass', to='airline_app.booking')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boarding_passes', to='airline_app.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boarding_passes', to='airline_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Baggage',
            fields=[
                ('baggage_id', models.AutoField(primary_key=True, serialize=False)),
                ('weight', models.DecimalField(decimal_places=2, help_text='Weight in kg', max_digits=5)),
                ('type', models.CharField(choices=[('CABIN', 'Cabin'), ('CHECKED', 'Checked'), ('OVERSIZED', 'Oversized')], max_length=10)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baggage', to='airline_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('DEBIT_CARD', 'Debit Card'), ('PAYPAL', 'PayPal'), ('BANK_TRANSFER', 'Bank Transfer')], max_length=15)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='airline_app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('staff', models.CharField(blank=True, max_length=100, null=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='airline_app.flight')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('seat_number', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_status', models.CharField(max_length=10)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='airline_app.booking')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='airline_app.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='airline_app.passenger')),
            ],
        ),
    ]
