from django.contrib import admin
from django.urls import path

from e_bill_app.views import E_way_bill_bulk, E_way_bill_cancel, E_way_bill_get



urlpatterns = [ 
    path('post-e-bill/',E_way_bill_bulk.as_view(), name='post-e-bill'),
    path('post-e-bill-get/',E_way_bill_get.as_view(), name='post-e-bill-get'),
    path('post-e-bill-cancel/',E_way_bill_cancel.as_view(), name='post-e-bill-cancel'),
]