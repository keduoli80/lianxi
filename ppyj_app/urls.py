from django.contrib import admin
from django.urls import path, include
from ppyj_app import views
app_name='ppyj_app'
urlpatterns = [
    path('register/',views.register,name='register'),
]
