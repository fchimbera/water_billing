from django.urls import path
from .views import add_reading_web, my_bills_web, bill_detail_web

urlpatterns = [
    path('readings/add/', add_reading_web, name='add-reading'),
    path('bills/', my_bills_web, name='my-bills'),
    path('bills/<int:pk>/', bill_detail_web, name='bill-detail'),
]
# This file contains the URL patterns for the web views of the billing app.
# It includes paths for adding meter readings, viewing bills, and viewing bill details.