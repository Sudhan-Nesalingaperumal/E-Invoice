from django.contrib import admin
from django.urls import path

from e_way_bill.views import E_way_bill



urlpatterns = [ 
    path('post-e-way-bill/',E_way_bill.as_view(), name='post-e-way-bill'),
]





























