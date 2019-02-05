import numpy as np
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render

from .computations.assignseats import SeatAssigner
from .models import Person


def index(request):
    people_list = Person.objects.all()
    context = {'people_list': people_list}
    return render(request, 'seating/index.html', context)


def compute(request):
    seats = SeatAssigner().valid_seats()
    context = {'seats': seats}
    return render(request, 'seating/seats.html', context)
