from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
	path('delivery', delivery),
	path('one',one),
    path('update',update),
    
    #added by millan on 10-11-2022 for order attachments 
    path('ord_attachment_create', ord_attachment_create),
    path('ord_attachment_delete', ord_attachment_delete),
]
