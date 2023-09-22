from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    # path('all_filter_assignto', all_filter_assignto),
    # path('all_filter_reportingto', all_filter_reportingto),
    path('dashboard', dashboard),
    path('opportunity_bystage', opportunity_bystage),
    path('movingitems', movingitems),
    path('movingitems_count', movingitems_count),
    path('invoice_counter', invoice_counter),   
    path('analytics', analytics),
    path('top5bp', top5bp),
    path('top5itembyamount', top5itembyamount),
    path('one',one),
    path('login',login),
    path('update', update),
    path('delete', delete)
]
