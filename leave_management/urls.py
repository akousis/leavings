"""
URL configuration for leave management app.
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',TemplateView.as_view(template_name='index.html'), name='landing_page'),
    path('apply/', views.apply_for_leave, name='apply_for_leave'),
    path('add-leave/', views.add_leave_application, name='add_leave_application'),
    path('history/', views.leave_history_view, name='leave_history'),
    
]