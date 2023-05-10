from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    template_name = 'customers/pages/home.html'
    return render(request, template_name)
