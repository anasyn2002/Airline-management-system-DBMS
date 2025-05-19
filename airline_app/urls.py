from django.urls import path
from . import views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('logout/', TemplateView.as_view(template_name='airline_app/logout.html'), name='logout'),
    #path('api/logout/', views.custom_logout_view, name='api-logout'),  # This will be called by fetch
    path('logout/', views.custom_logout_view, name='logout'),


    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Flights
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight-detail'),
    path('flights/create/', views.FlightCreateView.as_view(), name='flight-create'),
    path('flights/<int:pk>/update/', views.FlightUpdateView.as_view(), name='flight-update'),
    
    # Passengers
    path('passengers/', views.PassengerListView.as_view(), name='passenger-list'),
    path('passengers/<int:pk>/', views.PassengerDetailView.as_view(), name='passenger-detail'),
    path('passengers/create/', views.PassengerCreateView.as_view(), name='passenger-create'),
    
    # Bookings
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/confirm/', views.confirm_booking, name='booking-confirm'),

    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    
    # Boarding Passes
    path('boarding-passes/', views.BoardingPassListView.as_view(), name='boarding-pass-list'),
    path('boarding-passes/create/', views.BoardingPassCreateView.as_view(), name='boarding-pass-create'),
    
    # Schedules
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/edit/', views.ScheduleUpdateView.as_view(), name='schedule-edit'),
]
