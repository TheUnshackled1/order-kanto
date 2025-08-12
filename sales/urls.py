from django.urls import path
from . import views

urlpatterns = [
    path('sales-report/', views.sales_report, name='sales_report'),
]