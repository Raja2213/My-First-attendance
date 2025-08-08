from django.urls import path
from . import views

urlpatterns = [
    path('time-in/', views.time_in, name='time_in'),
    path('time-out/', views.time_out, name='time_out'),
]