from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse


def landing_page(request):
    return render(request, 'leave_management/landing_page.html')

"""
@login_required
def logout_view(request):
    logout(request)
    return redirect('landing_page')
    

def test_view(request):
    return render(request, 'leave_management/test_page.html')


def test_http_response(request):
    return HttpResponse("This is a test HTTP response.")    
"""