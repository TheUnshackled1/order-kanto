from django.urls import path
from . import views

app_name = 'menu'  # add this line

urlpatterns = [
    path('', views.menu, name='menu'),
]