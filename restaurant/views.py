from datetime import datetime

from django.core import serializers
from django.shortcuts import render

from .forms import BookingForm
from .models import Booking, Menu


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            form = BookingForm()
    return render(request, 'book.html', {'form': form})


def bookings(request):
    date = request.GET.get('date', datetime.today().date())
    booking_list = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', booking_list)
    return render(
        request,
        'bookings.html',
        {'bookings': booking_json, 'date': date},
    )


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {'menu': menu_data}
    return render(request, 'menu.html', {'menu': main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, 'menu_item.html', {'menu_item': menu_item})
