from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('one',one),
    path('update', update),
    path('delete', delete),
    path('assign', assign),
    
    path('chatter', chatter),
    path('chatter_all', chatter_all),
    
    path('type_create', type_create),
    path('type_all', type_all),
    path('type_delete', type_delete),
    
    path('source_all', source_all),
    path('source_create', source_create),
    path('source_update', source_update),
    path('source_delete', source_delete)


]
