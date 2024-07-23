# signatures/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('verify/', views.verify_signature, name='verify_signature'),
    path('upload/', views.upload_signature, name='upload_signature'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
