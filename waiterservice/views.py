from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def home(request):
    return render(request, 'waiterservice/pages/home.html')
