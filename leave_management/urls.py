"""
URL configuration for leave management app.
"""
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    
    # URL for logging out. Django's built-in logout view handles the logic.
    # The 'name' attribute is what the template tag {% url 'logout' %} will use.
    # path('logout/', auth_views.logout_view.as_view(next_page='landing_page'), name='logout'),

    # path('', views.test_http_response, name='test_page'),
]