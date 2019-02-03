from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render

from .models import Person


def index(request):
    people_list = Person.objects.all()
    context = {'people_list': people_list}
    return render(request, 'seating/index.html', context)
