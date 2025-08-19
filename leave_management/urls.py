"""
URL configuration for leave management app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('apply/', views.apply_for_leave, name='apply_for_leave'),
    
]