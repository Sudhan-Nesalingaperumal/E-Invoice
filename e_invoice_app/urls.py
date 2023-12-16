from django.contrib import admin
from django.urls import path

from e_invoice_app.views import E_invoice



urlpatterns = [ 
    path('post-e_invoice/',E_invoice.as_view(), name='post-e_invoice'),
]