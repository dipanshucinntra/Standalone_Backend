from django.urls import path,include
from .views import *
from BusinessPartner import views, viewsBPBranch, viewsBPEmployee, viewsBPDepartment, viewsBPPosition

urlpatterns = [
    path('businesspartner/create', create),
    path('businesspartner/all', all),
    path('businesspartner/all_bp', all_bp),
    path('businesspartner/one', one),
    path('businesspartner/update', update),
    path('businesspartner/delete', delete),
    
    path('businesspartner/branch/create', viewsBPBranch.create),
    path('businesspartner/branch/one', viewsBPBranch.one),
    path('businesspartner/branch/all', viewsBPBranch.all),
    path('businesspartner/branch/update', viewsBPBranch.update),
    path('businesspartner/branch/delete', viewsBPBranch.delete),
    
    path('businesspartner/employee/create', viewsBPEmployee.create),
    path('businesspartner/employee/one', viewsBPEmployee.one),
    path('businesspartner/employee/all', viewsBPEmployee.all),
    path('businesspartner/employee/update', viewsBPEmployee.update),
    path('businesspartner/employee/delete', viewsBPEmployee.delete),
    
    path('businesspartner/department/create', viewsBPDepartment.create),
    path('businesspartner/department/one', viewsBPDepartment.one),
    path('businesspartner/department/all', viewsBPDepartment.all),
    path('businesspartner/department/update', viewsBPDepartment.update),
    path('businesspartner/department/delete', viewsBPDepartment.delete),
    
    path('businesspartner/position/create', viewsBPPosition.create),
    path('businesspartner/position/one', viewsBPPosition.one),
    path('businesspartner/position/all', viewsBPPosition.all),
    path('businesspartner/position/update', viewsBPPosition.update),
    path('businesspartner/position/delete', viewsBPPosition.delete),

    # BP type
    path('businesspartner/createtype', createtype),
    path('businesspartner/alltype', alltype),
    
    # added by millan to get only 5 fields from Customer on 08-September-2022    
    path('businesspartner/get_bp', get_bp),
    
    #added by millan for business_partner attachments 
    path('businesspartner/bp_attachments', bp_attachments),
    path('businesspartner/bp_attachment_create', bp_attachment_create),
    path('businesspartner/bp_attachment_update', bp_attachment_update),
    path('businesspartner/bp_attachment_delete', bp_attachment_delete),
    
    path('businesspartner/monthlySales', monthlySales), #added by millan on 06-10-2022
    
    path('businesspartner/payment_summary', payment_summary)
    
]
