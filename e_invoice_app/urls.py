from django.contrib import admin
from django.urls import path

from e_invoice_app.views import E_invoice_bulk, E_invoice_cancel, E_invoice_get





urlpatterns = [ 
    path('post-e_invoice/',E_invoice_bulk.as_view(), name='post-e_invoice'),
    path('post-e_invoice_cancel/',E_invoice_cancel.as_view(), name='post-e_invoice_cancel'),
    path('post-e_invoice_get/',E_invoice_get.as_view(), name='post-e_invoice_get'),
]