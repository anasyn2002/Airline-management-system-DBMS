from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import *  # We'll create these forms next
import calendar
from datetime import datetime, date
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Dashboard View
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'airline_app/dashboard.html'
    context_object_name = 'flights'
    
    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_flight 
        # WHERE DATE(departure_time) = CURRENT_DATE;
        return Flight.objects.filter(departure_time__date=timezone.now().date())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # SQL: SELECT COUNT(*) FROM airline_app_booking 
        # WHERE status = 'CONFIRMED';
        context['total_bookings'] = Booking.objects.filter(status='CONFIRMED').count()
        
        # SQL: SELECT COUNT(*) FROM airline_app_flight 
        # WHERE DATE(departure_time) = CURRENT_DATE;
        context['today_departures'] = Flight.objects.filter(departure_time__date=timezone.now().date()).count()
        
        # SQL: SELECT COUNT(*) FROM airline_app_booking 
        # WHERE status = 'PENDING';
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
        return context

# Flight Views
class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'airline_app/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_flight;
        queryset = Flight.objects.all()
        
        # Apply filters if provided
        flight_number = self.request.GET.get('flight_number', '')
        if flight_number:
            # SQL: SELECT * FROM airline_app_flight 
            # WHERE flight_number LIKE '%{flight_number}%';
            queryset = queryset.filter(flight_number__icontains=flight_number)
        
        source = self.request.GET.get('source', '')
        if source:
            # SQL: SELECT * FROM airline_app_flight 
            # WHERE source_airport_id = {source};
            queryset = queryset.filter(source_airport_id=source)
        
        destination = self.request.GET.get('destination', '')
        if destination:
            # SQL: SELECT * FROM airline_app_flight 
            # WHERE destination_airport_id = {destination};
            queryset = queryset.filter(destination_airport_id=destination)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        # SQL: SELECT * FROM airline_app_airport;
        context['airports'] = Airport.objects.all()
        return context


class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'airline_app/flight_detail.html'
    context_object_name = 'flight'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # SQL: SELECT * FROM airline_app_booking 
        # WHERE flight_id = {self.object.id};
        context['bookings'] = self.object.bookings.all()
        return context

class FlightCreateView(LoginRequiredMixin, CreateView):
    model = Flight
    template_name = 'airline_app/flight_form.html'
    form_class = FlightForm
    success_url = reverse_lazy('flight-list')

class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = Flight
    template_name = 'airline_app/flight_form.html'
    form_class = FlightForm
    success_url = reverse_lazy('flight-list')

# Passenger Views
class PassengerListView(LoginRequiredMixin, ListView):
    model = Passenger
    template_name = 'airline_app/passenger_list.html'
    context_object_name = 'passengers'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_passenger;
        queryset = Passenger.objects.all()
        
        # Apply search filter if provided
        search = self.request.GET.get('search', '')
        if search:
            # SQL: SELECT * FROM airline_app_passenger 
            # WHERE name LIKE '%{search}%' 
            # OR email LIKE '%{search}%' 
            # OR passport_number LIKE '%{search}%';
            queryset = queryset.filter(
                models.Q(name__icontains=search) | 
                models.Q(email__icontains=search) | 
                models.Q(passport_number__icontains=search)
            )
        
        return queryset

class PassengerDetailView(LoginRequiredMixin, DetailView):
    model = Passenger
    template_name = 'airline_app/passenger_detail.html'
    context_object_name = 'passenger'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # SQL: SELECT * FROM airline_app_booking 
        # WHERE passenger_id = {self.object.id};
        context['bookings'] = self.object.bookings.all()
        
        # SQL: SELECT * FROM airline_app_baggage 
        # WHERE passenger_id = {self.object.id};
        context['baggage'] = self.object.baggage.all()
        return context

class PassengerCreateView(LoginRequiredMixin, CreateView):
    model = Passenger
    template_name = 'airline_app/passenger_form.html'
    form_class = PassengerForm
    success_url = reverse_lazy('passenger-list')

# Booking Views
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'airline_app/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_booking;
        queryset = Booking.objects.all()
        
        # Apply filters if provided
        status = self.request.GET.get('status', '')
        if status:
            # SQL: SELECT * FROM airline_app_booking 
            # WHERE status = {status};
            queryset = queryset.filter(status=status)
        
        flight = self.request.GET.get('flight', '')
        if flight:
            # SQL: SELECT * FROM airline_app_booking b
            # JOIN airline_app_flight f ON b.flight_id = f.id
            # WHERE f.flight_number LIKE '%{flight}%';
            queryset = queryset.filter(flight__flight_number__icontains=flight)
        
        passenger = self.request.GET.get('passenger', '')
        if passenger:
            # SQL: SELECT * FROM airline_app_booking b
            # JOIN airline_app_passenger p ON b.passenger_id = p.id
            # WHERE p.name LIKE '%{passenger}%';
            queryset = queryset.filter(passenger__name__icontains=passenger)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add booking statistics
        # SQL: SELECT COUNT(*) FROM airline_app_booking 
        # WHERE status = 'CONFIRMED';
        context['confirmed_count'] = Booking.objects.filter(status='CONFIRMED').count()
        
        # SQL: SELECT COUNT(*) FROM airline_app_booking 
        # WHERE status = 'PENDING';
        context['pending_count'] = Booking.objects.filter(status='PENDING').count()
        
        # SQL: SELECT COUNT(*) FROM airline_app_booking 
        # WHERE status = 'CANCELLED';
        context['cancelled_count'] = Booking.objects.filter(status='CANCELLED').count()
        
        return context

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'airline_app/booking_detail.html'
    context_object_name = 'booking'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'airline_app/booking_form.html'
    form_class = BookingForm
    success_url = reverse_lazy('booking-list')

# Payment Views
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'airline_app/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_payment;
        queryset = Payment.objects.all()
        
        # Apply filters if provided
        method = self.request.GET.get('method', '')
        if method:
            # SQL: SELECT * FROM airline_app_payment 
            # WHERE payment_method = {method};
            queryset = queryset.filter(payment_method=method)
        
        date_from = self.request.GET.get('date_from', '')
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                # SQL: SELECT * FROM airline_app_payment 
                # WHERE DATE(payment_date) >= {date_from};
                queryset = queryset.filter(payment_date__date__gte=date_from)
            except ValueError:
                pass
        
        date_to = self.request.GET.get('date_to', '')
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                # SQL: SELECT * FROM airline_app_payment 
                # WHERE DATE(payment_date) <= {date_to};
                queryset = queryset.filter(payment_date__date__lte=date_to)
            except ValueError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Payment statistics
        payment_stats = get_payment_stats()
        context.update(payment_stats)
        
        return context
    

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'airline_app/payment_form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('payment-list')

# Boarding Pass Views
class BoardingPassListView(LoginRequiredMixin, ListView):
    model = BoardingPass
    template_name = 'airline_app/boarding_pass_list.html'
    context_object_name = 'boarding_passes'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_boardingpass;
        queryset = BoardingPass.objects.all()
        
        # Apply filters if provided
        flight = self.request.GET.get('flight', '')
        if flight:
            # SQL: SELECT * FROM airline_app_boardingpass bp
            # JOIN airline_app_flight f ON bp.flight_id = f.id
            # WHERE f.flight_number LIKE '%{flight}%';
            queryset = queryset.filter(flight__flight_number__icontains=flight)
        
        gate = self.request.GET.get('gate', '')
        if gate:
            # SQL: SELECT * FROM airline_app_boardingpass 
            # WHERE gate_number LIKE '%{gate}%';
            queryset = queryset.filter(gate_number__icontains=gate)
        
        date = self.request.GET.get('date', '')
        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
                # SQL: SELECT * FROM airline_app_boardingpass 
                # WHERE DATE(boarding_time) = {date};
                queryset = queryset.filter(boarding_time__date=date)
            except ValueError:
                pass
        
        return queryset

class BoardingPassCreateView(LoginRequiredMixin, CreateView):
    model = BoardingPass
    template_name = 'airline_app/boarding_pass_form.html'
    form_class = BoardingPassForm
    success_url = reverse_lazy('boarding-pass-list')

# Schedule Views
class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'airline_app/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 10

    def get_queryset(self):
        # SQL: SELECT * FROM airline_app_schedule;
        queryset = Schedule.objects.all()
        
        # Apply filters if provided
        flight = self.request.GET.get('flight', '')
        if flight:
            # SQL: SELECT * FROM airline_app_schedule s
            # JOIN airline_app_flight f ON s.flight_id = f.id
            # WHERE f.flight_number LIKE '%{flight}%';
            queryset = queryset.filter(flight__flight_number__icontains=flight)
            
        staff = self.request.GET.get('staff', '')
        if staff:
            # SQL: SELECT * FROM airline_app_schedule 
            # WHERE staff LIKE '%{staff}%';
            queryset = queryset.filter(staff__icontains=staff)
            
        date_filter = self.request.GET.get('date', '')
        if date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                # SQL: SELECT * FROM airline_app_schedule 
                # WHERE date = {date_obj};
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calendar view data
        today = date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Get schedules for the selected month (for calendar view)
        # SQL: SELECT * FROM airline_app_schedule 
        # WHERE EXTRACT(YEAR FROM date) = {year} 
        # AND EXTRACT(MONTH FROM date) = {month};
        month_schedules = Schedule.objects.filter(date__year=year, date__month=month)
        
        # Add calendar data
        calendar_data = get_calendar_data(year, month, month_schedules)
        context.update(calendar_data)
        
        return context

    
    def get_calendar_data(self, year, month, schedules=None):
        today = date.today()
        
        cal = calendar.monthcalendar(year, month)
        # SQL: SELECT * FROM airline_app_schedule 
        # WHERE EXTRACT(YEAR FROM date) = {year} 
        # AND EXTRACT(MONTH FROM date) = {month};
        month_schedules = schedules if schedules is not None else Schedule.objects.filter(date__year=year, date__month=month)
        
        # Group schedules by day
        scheduled_days = {}
        for schedule in month_schedules:
            day = schedule.date.day
            if day not in scheduled_days:
                scheduled_days[day] = []
            scheduled_days[day].append(schedule)
        
        # Prepare calendar data
        calendar_weeks = []
        for week in cal:
            week_dict = {}
            for i, day in enumerate(week):
                if day == 0:
                    week_dict[day] = []
                else:
                    week_dict[day] = scheduled_days.get(day, [])
            calendar_weeks.append(week_dict)
        
        # Calculate previous and next month
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        return {
            'calendar_weeks': calendar_weeks,
            'current_month': month,
            'current_year': year,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'current_month_name': calendar.month_name[month],
            'prev_month_name': calendar.month_name[prev_month],
            'next_month_name': calendar.month_name[next_month],
            'today_day': today.day,
            'today_month': today.month,
            'today_year': today.year,
        }

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    template_name = 'airline_app/schedule_form.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('schedule-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    template_name = 'airline_app/schedule_form.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('schedule-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# airline_app/views.py (additional custom view methods)

def confirm_booking(request, pk):
    if request.method == 'POST':
        # SQL: SELECT * FROM airline_app_booking WHERE id = {pk};
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = 'CONFIRMED'
        booking.save()
        
        # Create a ticket if it doesn't exist
        if not hasattr(booking, 'ticket'):
            # SQL: INSERT INTO airline_app_ticket 
            # (seat_number, price, booking_status, passenger_id, flight_id, booking_id) 
            # VALUES ({booking.seat_number}, 350.00, 'CONFIRMED', 
            # {booking.passenger.id}, {booking.flight.id}, {booking.id});
            Ticket.objects.create(
                seat_number=booking.seat_number,
                price=350.00,  # Default price - in a real app this would be calculated
                booking_status='CONFIRMED',
                passenger=booking.passenger,
                flight=booking.flight,
                booking=booking
            )
        
        messages.success(request, f"Booking #{booking.booking_id} has been confirmed.")
        return redirect('booking-detail', pk=booking.pk)
    return redirect('booking-detail', pk=pk)

# Payment stats for the payment list view
def get_payment_stats():
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # SQL: SELECT SUM(amount) FROM airline_app_payment;
    total_amount = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # SQL: SELECT SUM(amount) FROM airline_app_payment 
    # WHERE payment_method = 'CREDIT_CARD';
    credit_card_amount = Payment.objects.filter(payment_method='CREDIT_CARD').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # SQL: SELECT SUM(amount) FROM airline_app_payment 
    # WHERE payment_date >= {start_of_month};
    this_month_amount = Payment.objects.filter(payment_date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate average amount
    # SQL: SELECT COUNT(*) FROM airline_app_payment;
    payment_count = Payment.objects.count()
    average_amount = round(total_amount / payment_count, 2) if payment_count > 0 else 0
    
    return {
        'total_amount': total_amount,
        'credit_card_amount': credit_card_amount,
        'this_month_amount': this_month_amount,
        'average_amount': average_amount
    }

# Schedule calendar view helpers

def get_calendar_data(year, month, schedules=None):
    today = date.today()
    
    cal = calendar.monthcalendar(year, month)
    # SQL: SELECT * FROM airline_app_schedule 
    # WHERE EXTRACT(YEAR FROM date) = {year} 
    # AND EXTRACT(MONTH FROM date) = {month};
    month_schedules = Schedule.objects.filter(date__year=year, date__month=month) if schedules is None else schedules
    
    # Group schedules by day
    scheduled_days = {}
    for schedule in month_schedules:
        day = schedule.date.day
        if day not in scheduled_days:
            scheduled_days[day] = []
        scheduled_days[day].append(schedule)
    
    # Prepare calendar data
    calendar_weeks = []
    for week in cal:
        week_dict = {}
        for i, day in enumerate(week):
            if day == 0:
                week_dict[day] = []
            else:
                week_dict[day] = scheduled_days.get(day, [])
        calendar_weeks.append(week_dict)
    
    # Calculate previous and next month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    return {
        'calendar_weeks': calendar_weeks,
        'current_month': month,
        'current_year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'current_month_name': calendar.month_name[month],
        'prev_month_name': calendar.month_name[prev_month],
        'next_month_name': calendar.month_name[next_month],
        'today_day': today.day,
        'today_month': today.month,
        'today_year': today.year,
    }


class CustomLoginView(LoginView):
    template_name = 'airline_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

def redirect_if_not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def custom_logout_view(request):
    """Custom view to handle logout via GET request"""
    logout(request)
    return redirect('login')