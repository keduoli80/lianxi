from django.contrib import admin
from django.urls import path, include
from web.views import account
app_name='web'
urlpatterns = [
    path('register/', account.register,name='register'),
]