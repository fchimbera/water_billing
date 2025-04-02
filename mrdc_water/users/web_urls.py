from django.urls import path
from .views import register_web, login_web, logout_web

urlpatterns = [
    path('register/', register_web, name='register'),
    path('login/', login_web, name='login'),
    path('logout/', logout_web, name='logout'),
]
# This file contains the URL patterns for the web views of the users app.
# It includes paths for user registration, login, and logout.
