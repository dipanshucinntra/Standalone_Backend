from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('update', update),
    path('all', all),
	path('one', one),
    path('delete', delete),
    
    path('tax_all', tax_all),
    path('tax_create', tax_create),
    path('tax_update', tax_update),
	path('tax_one', tax_one),
    
    path('category_create', category_create),
    path('category_all', category_all),
    path('category_update', category_update),
	path('category_one', category_one)
    
]
