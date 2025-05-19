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
        return Flight.objects.filter(departure_time__date=timezone.now().date())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bookings'] = Booking.objects.filter(status='CONFIRMED').count()
        context['today_departures'] = Flight.objects.filter(departure_time__date=timezone.now().date()).count()
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
        return context

# Flight Views
class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'airline_app/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10

    def get_queryset(self):
        queryset = Flight.objects.all()
        
        # Apply filters if provided
        flight_number = self.request.GET.get('flight_number', '')
        if flight_number:
            queryset = queryset.filter(flight_number__icontains=flight_number)
        
        source = self.request.GET.get('source', '')
        if source:
            queryset = queryset.filter(source_airport_id=source)
        
        destination = self.request.GET.get('destination', '')
        if destination:
            queryset = queryset.filter(destination_airport_id=destination)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['airports'] = Airport.objects.all()
        return context


class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'airline_app/flight_detail.html'
    context_object_name = 'flight'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        queryset = Passenger.objects.all()
        
        # Apply search filter if provided
        search = self.request.GET.get('search', '')
        if search:
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
        context['bookings'] = self.object.bookings.all()
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
        queryset = Booking.objects.all()
        
        # Apply filters if provided
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        
        flight = self.request.GET.get('flight', '')
        if flight:
            queryset = queryset.filter(flight__flight_number__icontains=flight)
        
        passenger = self.request.GET.get('passenger', '')
        if passenger:
            queryset = queryset.filter(passenger__name__icontains=passenger)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add booking statistics
        context['confirmed_count'] = Booking.objects.filter(status='CONFIRMED').count()
        context['pending_count'] = Booking.objects.filter(status='PENDING').count()
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
        queryset = Payment.objects.all()
        
        # Apply filters if provided
        method = self.request.GET.get('method', '')
        if method:
            queryset = queryset.filter(payment_method=method)
        
        date_from = self.request.GET.get('date_from', '')
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(payment_date__date__gte=date_from)
            except ValueError:
                pass
        
        date_to = self.request.GET.get('date_to', '')
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
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
        queryset = BoardingPass.objects.all()
        
        # Apply filters if provided
        flight = self.request.GET.get('flight', '')
        if flight:
            queryset = queryset.filter(flight__flight_number__icontains=flight)
        
        gate = self.request.GET.get('gate', '')
        if gate:
            queryset = queryset.filter(gate_number__icontains=gate)
        
        date = self.request.GET.get('date', '')
        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
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
        queryset = Schedule.objects.all()
        
        # Apply filters if provided
        flight = self.request.GET.get('flight', '')
        if flight:
            queryset = queryset.filter(flight__flight_number__icontains=flight)
            
        staff = self.request.GET.get('staff', '')
        if staff:
            queryset = queryset.filter(staff__icontains=staff)
            
        date_filter = self.request.GET.get('date', '')
        if date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
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
        month_schedules = Schedule.objects.filter(date__year=year, date__month=month)
        
        # Add calendar data
        calendar_data = get_calendar_data(year, month, month_schedules)
        context.update(calendar_data)
        
        return context

    
    def get_calendar_data(self, year, month, schedules=None):
        today = date.today()
        
        cal = calendar.monthcalendar(year, month)
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
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = 'CONFIRMED'
        booking.save()
        
        # Create a ticket if it doesn't exist
        if not hasattr(booking, 'ticket'):
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
    
    total_amount = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    credit_card_amount = Payment.objects.filter(payment_method='CREDIT_CARD').aggregate(Sum('amount'))['amount__sum'] or 0
    this_month_amount = Payment.objects.filter(payment_date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate average amount
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

# If you want to protect all views, add this function to check if user is authenticated
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