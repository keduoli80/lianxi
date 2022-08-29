from django.contrib import admin
from django.urls import path, include
from web.views import account,home
app_name='web'
urlpatterns = [
    path('register/', account.register,name='register'),
    path('send/sms/', account.send_sms,name='send_sms'),
    path('login/', account.login,name='login'),
    path('login/out/', account.login_out,name='login_out'),
    path('image/code/', account.image_code,name='image_code'),

    path('home/', home.home,name='home'),
]