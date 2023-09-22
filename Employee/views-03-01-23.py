from webbrowser import get
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Campaign.models import CampaignSet
from Campaign.views import showCamSet

from Item.models import Item
from Item.serializers import ItemSerializer
from Expense.models import Expense
from Payment.models import Payment
from Expense.serializers import ExpenseSerializer
from .forms import EmployeeForm  
from .models import *
from Activity.models import Activity
from Lead.models import Lead
from Invoice.models import Invoice
from Notification.models import Notification
import requests, json

from pytz import timezone
from datetime import date, datetime as dt, timedelta
from collections import Counter

from Order.models import Order, DocumentLines as OrderDocumentLines
from Invoice.models import Invoice, DocumentLines as InvoiceDocumentLines

from Mylib import *

tdate = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

from BusinessPartner.models import BusinessPartner
from Opportunity.models import Opportunity
from Order.models import Order, DocumentLines
from Quotation.models import Quotation

from django.contrib import messages

from django.db.models import Sum, F #added by millan on 05-September-2022

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import EmployeeSerializer, TargetSerializer, TargetqtySerializer, TargetyrSerializer #added by millan on 15-11-2022
from Opportunity.serializers import OpportunitySerializer
from rest_framework.parsers import JSONParser
from django.db.models import Q #added by millan on 14-10-2022

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
# Create your views here.  


#top 5 item based on sales person code and order
@api_view(["POST"])
def top5itembyamount(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        
        if emp_obj.role.lower() == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role.lower() == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesPersonCode))
        
        if Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode_arr).exists():
            top2bp = OrderDocumentLines.objects.values('ItemCode').annotate(Total = Sum(F('Quantity')*F('UnitPrice'))).order_by('-Total')[:5]
    
            top5=[]

            for od in top2bp:
                top5dt = OrderDocumentLines.objects.filter(ItemCode = od['ItemCode']).values('ItemDescription')
                for desc in top5dt:
                    print(desc)
                top5.append({"ItemCode":od['ItemCode'], "ItemName":desc['ItemDescription'], "Total":od['Total']})
            
            return Response({"message": "Success","status": 200,"data":top5}) #added by millan on 05-September-2022
        else:
            return Response({"message": "SalesPersonCode Not Found","status": 201,"data":[]})
        
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
@api_view(["GET"])
def top5itembyamount_old(request):
    try:
        top2bp = OrderDocumentLines.objects.values('ItemCode').annotate(Total = Sum(F('Quantity')*F('UnitPrice'))).order_by('-Total')[:5]
    
        top5=[]

        for od in top2bp:
            top5dt = OrderDocumentLines.objects.filter(ItemCode = od['ItemCode']).values('ItemDescription')
            for desc in top5dt:
                print(desc)
            top5.append({"ItemCode":od['ItemCode'], "ItemName":desc['ItemDescription'], "Total":od['Total']})
        
        return Response({"message": "Success","status": 200,"data":top5}) #added by millan on 05-September-2022
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

@api_view(["GET"])
def top5bp_old(request):
    try:
        #added by millan on 05-September-2022
        top2bp = Order.objects.values('CardCode').annotate(Total = Sum(F('DocTotal'))).order_by('-Total')[:5]
        print('milan',top2bp)
        top5=[]
        for od in top2bp:
            try:
                # cd = BusinessPartner.objects.get(CardCode=od.CardCode)
                # print(cd.CardCode)
                # print(cd.CardName)
                # print(od.Total)
                cd = BusinessPartner.objects.filter(CardCode = od['CardCode']).values('CardName')
                # print(cd.query)
                for cName in cd:
                    print(cName)
                top5.append({"CardCode":od['CardCode'], "CardName":cName['CardName'], 'Total':od['Total']})
            except Exception as e:
                # top5.append({"CardCode":od.CardCode, "CardName":od.CardCode, 'Total':od.Total})
                top5.append({"CardCode":od['CardCode'], "CardName":od['CardCode'], 'Total':od['Total']})
            
        return Response({"message": "Success","status": 200,"data":top5})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

@api_view(["POST"])
def analytics(request):

    json_data = request.data
    month = int(json_data['month'])
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
            print(SalesEmployeeCode)
            
            tgt_all = Target.objects.filter(SalesPersonCode__in=SalesEmployeeCode).exclude(monthYear=yearmonth).order_by("-monthYear")[:month]
            #{"month":"3", "SalesEmployeeCode":"3"}
            amount = sum(tgt_all.values_list('amount', flat=True))            
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)
            
            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)
            
            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)
            
            notification = Notification.objects.filter(Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)
            
            
            return Response({"message": "Success","status": 200,"data":[{"notification":notification, "amount":amount, "sale":sale, "sale_diff":sale_diff}]})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

#Target Create API
@api_view(['POST'])
def target(request):
    try:
        amount = request.data['amount']
        monthYear = request.data['monthYear']
        SalesPersonCode = request.data['SalesPersonCode']
        #sale = request.data['sale']
        #sale_diff = request.data['sale_diff']
        CreatedDate = request.data['CreatedDate']        
        model = Target(amount=amount, monthYear=monthYear, SalesPersonCode=SalesPersonCode, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        model.save()
        
        tgt = Target.objects.latest('id')
        print(tgt.id)
        return Response({"message":"Success","status":"200","data":[]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})

@api_view(["POST"])
def dashboard(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emp_ids = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}
            
            lead_all = Lead.objects.filter(assignedTo__in=emp_ids).count()
            print(lead_all)
            
            opp_all = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode).count()
            #print(opp_all)
            
            quot_all = Quotation.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            #print(quot_all)
            
            ord_all = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            #print(ord_all)
            
            expense_all = Expense.objects.filter(employeeId__in=SalesEmployeeCode).count()
            #print(expense_all)
            
            payment_all = Payment.objects.filter(createdBy__in=SalesEmployeeCode).count()
            #print(payment_all)
            
            #bp_all = BusinessPartner.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            bp_all = BusinessPartner.objects.all().count()
            #print(bp_all)
            
            tgt_all = Target.objects.filter(SalesPersonCode__in=SalesEmployeeCode, monthYear=yearmonth)
            
            amount = sum(tgt_all.values_list('amount', flat=True))            
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)
            
            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)
            
            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)
            
            notification = Notification.objects.filter(Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)

            ord_over = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=tdate).count()
            print(ord_over)
            print(date)
            
            ord_open = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=tdate).count()
            print(ord_open)

            ord_close = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close").count()
            print(ord_close)
            
            #added by millan on 25/08/2022 for Campset Count
            campset_count = CampaignSet.objects.all().count()
			
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":[{"notification":notification, "amount":amount, "sale":sale, "sale_diff":sale_diff, "Opportunity":opp_all, "Quotation":quot_all, "Order":ord_all, "Customer":bp_all, "Leads":lead_all, "Over":ord_over, "Open":ord_open, "Close":ord_close, "campset_count" : campset_count, "expense_all": expense_all, "payment_all": payment_all}]})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

@api_view(["POST"])
def invoice_counter(request):
    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[str(SalesEmployeeCode)]
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            else:
                SalesEmployeeCode=[str(SalesEmployeeCode)]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            #live=0
            inv_count = len(Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode))
     
            return Response({"message": "Success","status": 200,"data":[{"Invoice":inv_count}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

#Employee Create API
@api_view(['POST'])
def create(request):
    try:
        if Employee.objects.filter(userName = request.data['userName']).exists():
            return Response({"message": "UserName Already Exists","status": 201,"data":[]}) 
        elif Employee.objects.filter(Email = request.data['Email']).exists():
            return Response({"message": "Email Already Exists","status": 201,"data":[]}) 
        elif Employee.objects.filter(Mobile = request.data['Mobile']).exists():
            return Response({"message": "Mobile Number Already Exists","status": 201,"data":[]}) 
        else:
            companyID = request.data['companyID']
            SalesEmployeeCode = request.data['SalesEmployeeCode']
            SalesEmployeeName = request.data['SalesEmployeeName']
            EmployeeID = request.data['EmployeeID']
            userName = request.data['userName']
            password = request.data['password']
            firstName = request.data['firstName']
            middleName = request.data['middleName']
            lastName = request.data['lastName']
            Email = request.data['Email']
            Mobile = request.data['Mobile']
            role = request.data['role']
            position = request.data['position']
            branch = request.data['branch']
            Active = request.data['Active']
            #passwordUpdatedOn = request.data['passwordUpdatedOn']
            #lastLoginOn = request.data['lastLoginOn']
            #logedIn = request.data['logedIn']
            reportingTo = request.data['reportingTo']
            timestamp = request.data['timestamp']

            model=Employee(companyID = companyID, SalesEmployeeCode = SalesEmployeeCode, SalesEmployeeName = SalesEmployeeName, EmployeeID = EmployeeID, userName = userName, password = password, firstName = firstName, middleName = middleName, lastName = lastName, Email = Email, Mobile = Mobile, role = role, position = position, branch = branch, Active=Active, reportingTo = reportingTo, timestamp = timestamp)
            
            model.save()
            
            sp = Employee.objects.latest('id')        
            sp.SalesEmployeeCode = sp.id
            sp.save()
            
            return Response({"message":"successful","status":200,"data":[{"Sp_Id":sp.id, "SalesEmployeeCode":sp.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})

#Employee All API
@api_view(["GET"])
def all(request):
    
    employees_obj = Employee.objects.all().order_by('-id') 
    employee_json = EmployeeSerializer(employees_obj, many=True)
    return Response({"message": "Success","status": 200,"data":employee_json.data})

@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0, Active = "tYES")
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode, Active = "tYES")#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                print(emps)
                for emp in emps:
                    print(emp)
                    print(SalesEmployeeCode)
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emps_all = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode, Active = "tYES").order_by('-id')
            
            emps_json = EmployeeSerializer(emps_all, many=True)
            return Response({"message": "Success","status": 200,"data":emps_json.data})
            
            return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
               
#Employee All Filter API
@api_view(["POST"])
def all_filter_old(request):
    json_data = request.data
    
    if len(json_data) == 0:
        emps_obj = Employee.objects.all().order_by("-id")
        emps_json = EmployeeSerializer(emps_obj, many=True)
        return Response({"message": "Success","status": 200,"data":emps_json.data})
    else:
        #print(json_data.keys()[0])
        #if json_data['U_FAV']
        for ke in json_data.keys():
            if ke =='reportingTo' :
                if json_data['reportingTo'] !='':
                    emps_obj = Employee.objects.filter(reportingTo=json_data['reportingTo']).order_by("-id")
                    if len(emps_obj) ==0:
                        return Response({"message": "Not Available","status": 201,"data":[]})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":emps_json.data})
            elif ke =='role' :
                if json_data['role'] !='':
                    emps_obj = Employee.objects.filter(role=json_data['role']).order_by("-id")
                    if len(emps_obj) ==0:
                        return Response({"message": "Not Available","status": 201,"data":[]})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":emps_json.data})
            else:
                return Response({"message": "Not Available","status": 201,"data":[]})

#Employee One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        employee_obj = Employee.objects.get(id=id)
        employee_json = EmployeeSerializer(employee_obj)
        return Response({"message": "Success","status": 200,"data":[employee_json.data]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Employee Login API
@api_view(["POST"])
def login(request):
    try:
        #added by millan for showing active users only updated by millan on 17-10-2022 for login with email
        if Employee.objects.filter(Q(userName=request.data['userName']) | Q(Email=request.data['userName']), Active = "tYES").exists():
            userName=request.data['userName']
            password=request.data['password']
            FCM = request.data['FCM']
            msg=[]
            if Employee.objects.filter(Email=userName, password=password).exists():
                employee_obj = Employee.objects.get(Email=userName,password=password)
            elif Employee.objects.filter(userName=userName, password=password).exists():
                employee_obj = Employee.objects.get(userName=userName,password=password)
            else:
                return Response({"message": "Enter Valid UserName or Password","status": 201,"data":[]})
            if FCM !="":
                employee_obj.FCM = FCM
                employee_obj.save()
            employee_json = EmployeeSerializer(employee_obj)
            with open("../bridge/bridge/db.json") as f:
                db = f.read()
            data = json.loads(db)
            print(data)

            return Response({"message": "Success","status": 200,"data":employee_json.data, "SAP":data})
        else:
            return Response({"message": "InActive User Login Not Allowed", "status": 201,"data":[]})
    except:
        return Response({"message": "Username or Password is incorrect","status": 404,"data":[]})
		
#Employee Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Employee.objects.get(pk = fetchid)

        if Employee.objects.filter(userName = request.data['userName']).exclude(pk=fetchid):
            return Response({"message": "UserName Already Exists","status": 201,"data":[]}) 
        elif Employee.objects.filter(Email = request.data['Email']).exclude(pk=fetchid):
            return Response({"message": "Email Already Exists","status": 201,"data":[]}) 
        elif Employee.objects.filter(Mobile = request.data['Mobile']).exclude(pk=fetchid):
            return Response({"message": "Mobile Number Already Exists","status": 201,"data":[]}) 
        else:
            model.companyID = request.data['companyID']
            model.SalesEmployeeName = request.data['SalesEmployeeName']
            model.EmployeeID = request.data['EmployeeID']
            model.userName = request.data['userName']
            model.password = request.data['password']
            model.firstName = request.data['firstName']
            model.middleName = request.data['middleName']
            model.lastName = request.data['lastName']
            model.Email = request.data['Email']
            model.Mobile = request.data['Mobile']
            model.role = request.data['role']
            model.position = request.data['position']
            model.branch = request.data['branch']
            model.Active = request.data['Active']
            model.reportingTo = request.data['reportingTo']

            model.save()
        
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[request.data]})

#Employee delete
@api_view(['POST'])
def delete(request):
    try:
        fetchids=request.data['id']
        for empid in fetchids:
            if Employee.objects.filter(pk=empid).exists():
                Employee.objects.filter(pk=empid).delete()
        
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

# most order item in last 30 days
@api_view(['POST'])
def movingitems(request):
    try:
        json_data = request.data
        if "SalesEmployeeCode" in json_data:
            print("yes")
            
            if json_data['SalesEmployeeCode']!="":
                SalesEmployeeCode = json_data['SalesEmployeeCode']
                
                emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
                if emp_obj.role == 'admin':
                    emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                    SalesEmployeeCode=[]
                    for emp in emps:
                        SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
                elif emp_obj.role == 'manager':
                    emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                    SalesEmployeeCode=[SalesEmployeeCode]
                    for emp in emps:
                        SalesEmployeeCode.append(emp.SalesEmployeeCode)
                else:
                    SalesEmployeeCode=[SalesEmployeeCode]
                print(SalesEmployeeCode)
    
    
            fastMovingdate = date.today() - timedelta(days=15)
            slowMovingdate = date.today() - timedelta(days=30)

            print(fastMovingdate)
            print(slowMovingdate)

            itemCodeList = []
            fastMovingItemList = []
            # ----------------------------------------------------------------------------
            # ------------------------- Fast Moving Items --------------------------------
            # ----------------------------------------------------------------------------
            fastMovingOrder_obj = Order.objects.filter(SalesPersonCode__in = SalesEmployeeCode, CreateDate__gte = fastMovingdate)
            fastMovingItemCodeArr = []
            for order in fastMovingOrder_obj:
                order_id = order.id
                docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
                for docLine in docLineObj:
                    # print(docLine)
                    # docJason = DocumentLinesSerializer(docLine);
                    itemCode = docLine.ItemCode
                    itemObj = Item.objects.get(ItemCode = itemCode)
                    itemJson = ItemSerializer(itemObj)

                    if itemCode not in fastMovingItemCodeArr:
                        fastMovingItemList.append(itemJson.data)
                        fastMovingItemCodeArr.append(itemCode)
                        itemCodeList.append(itemCode)

            FastItemsCount = len(fastMovingItemCodeArr)
            
            # ----------------------------------------------------------------------------
            # ------------------------- Slow Moving Itmes --------------------------------
            # ----------------------------------------------------------------------------
            slowMovingdate_obj = Order.objects.filter(SalesPersonCode__in = SalesEmployeeCode, CreateDate__lte = fastMovingdate, CreateDate__gte = slowMovingdate)
            slowMovingItemCodeArr = []
            slowMovingItemList = []
            for order in slowMovingdate_obj:
                order_id = order.id
                docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
                for docLine in docLineObj:
                    # docJason = DocumentLinesSerializer(docLine);
                    itemCode = docLine.ItemCode
                    itemObj = Item.objects.get(ItemCode = itemCode)
                    itemJson = ItemSerializer(itemObj)
                    if itemCode not in fastMovingItemCodeArr:
                        slowMovingItemList.append(itemJson.data)
                        slowMovingItemCodeArr.append(itemCode)
                        itemCodeList.append(itemCode)
            
            SlowItemsCount = len(slowMovingItemCodeArr)

            dictItem = set(itemCodeList)
            # notMovingItemCount = Item.objects.all().exclude(ItemCode__in = dictItem).count()
            notMovingItemObj = Item.objects.all().exclude(ItemCode__in = dictItem)
            notMovingItemJson = ItemSerializer(notMovingItemObj, many=True)
            notMovingItemCount = len(notMovingItemObj)
            context = {
                "FastMovingItemsList": fastMovingItemList,
                "FastItemsCount": FastItemsCount,
                "SlowMovingItemsList": slowMovingItemList,
                "SlowItemsCount": SlowItemsCount,
                "NotMovingItemsList": notMovingItemJson.data,
                "NotMovingItemsCount": notMovingItemCount
            }

            print(FastItemsCount)
            print(SlowItemsCount)
            print(notMovingItemCount)

            return Response({"message":"successful","status":200,"data":[context]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[str(e)]})

# most order item in last 30 days
@api_view(['GET'])
def movingitems_count(request):
    try:
        fastMovingdate = date.today() - timedelta(days=15)
        slowMovingdate = date.today() - timedelta(days=30)
        itemCodeList = []
        # --------------------------------------------------------------------------
        # ------------------------- Fast Moving Items ------------------------------
        # --------------------------------------------------------------------------
        fastMovingOrder_obj = Order.objects.filter(CreateDate__gte = fastMovingdate)
        fastMovingItemCodeArr = []
        for order in fastMovingOrder_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    fastMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        FastItemsCount = len(fastMovingItemCodeArr)
        
        # ----------------------------------------------------------------------------
        # ------------------------- Slow Moving Itmes --------------------------------
        # ----------------------------------------------------------------------------
        slowMovingdate_obj = Order.objects.filter(CreateDate__lte = fastMovingdate, CreateDate__gte = slowMovingdate)
        slowMovingItemCodeArr = []
        for order in slowMovingdate_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    slowMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)
        
        SlowItemsCount = len(slowMovingItemCodeArr)

        # --------------------------------------------------------------------------
        # ------------------------- Not Moving Itmes -------------------------------
        # --------------------------------------------------------------------------
        dictItem = set(itemCodeList)
        notMovingItemCount = Item.objects.all().exclude(ItemCode__in = dictItem).count()

        context = {
            "FastItemsCount": FastItemsCount,
            "SlowItemsCount": SlowItemsCount,
            "NotMovingItemsCount": notMovingItemCount
        }

        return Response({"message":"successful","status":200,"data":[context]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[str(e)]})

@api_view(["POST"])
def opportunity_bystage(request):
    json_data = request.data
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
            print(SalesEmployeeCode)
            
            opp_Lead_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Lead").count()
            opp_Need_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Need Analysis").count()
            opp_Quotation_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Quotation").count()
            opp_Negotiation_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Negotiation").count()
            opp_Order_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Order").count()
            
            opportunity_context = {
                "Lead": opp_Lead_count,
                "NeedAnalysis": opp_Need_count,
                "Quotation": opp_Quotation_count,
                "Negotiation": opp_Negotiation_count,
                "Order": opp_Order_count
            }
            
            return Response({"message": "Success","status": 200,"data":[opportunity_context]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    
#added by millan on 10-11-2022 to get Employee Expense
@api_view(["POST"])
def empExpen(request):
    try:
        empId=request.data['empId']
        if Expense.objects.filter(employeeId=empId).exists():
            empExpn_obj = Expense.objects.filter(employeeId=empId)
            
            allexpn = [];
          
            for obj in empExpn_obj:
                empExpn_json = ExpenseSerializer(obj)
                empExpnFinal = json.loads(json.dumps(empExpn_json.data))
                if Attachment.objects.filter(LinkID = obj.id, LinkType="Expense").exists():
                    Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Expense")
                    Attach_json = AttachmentSerializer(Attach_dls, many=True)
                    print(Attach_json.data)
                    empExpnFinal['Attach'] = Attach_json.data
                else:
                    empExpnFinal['Attach'] = []
                    
                allexpn.append(empExpnFinal)
            
            return Response({"message": "Success","status": 200,"data":allexpn})
        else:
            return Response({"message": "Expense not found","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#added by millan on 11-11-2022 to get sales of each particular month based on sales employee code
@api_view(["POST"])
def monthlySalesEmp(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']        
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
        
        SalesEmployeeCode_list = ",".join(SalesEmployeeCode_arr)
        
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        CurrentYearComplete = str(todays_date.year) + '-' + str('04') + '-' + str('01')
        NextYearComplete = str(todays_date.year +1) + '-' + str('03') + '-' + str('31')
        monSales = [
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Jan") + "-" + str(NextYr),
                "MonthlyCount": 0,
                "Year": 2023
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Feb") + "-" + str(NextYr),
                "MonthlyCount": 0,
                "Year": 2023
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Mar") + "-" + str(NextYr),
                "MonthlyCount": 0,
                "Year": 2023
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Apr") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("May") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Jun") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Jul") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Aug") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Sep") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Oct") + "-" + str(CurrYr),
                "MonthlyCount": 2,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Nov") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            },
            {
                "MonthlySales": 0,
                "FinanYr": FinanYr,
                "Month": str("Dec") + "-" + str(CurrYr),
                "MonthlyCount": 0,
                "Year": 2022
            }        
        ]
        MonthlySales = MonthlyCount = 0
        if Order.objects.filter(SalesPersonCode__in = SalesEmployeeCode_arr).exists():
            sql_query = f"SELECT id, CreateDate, SUBSTR(CreateDate,1,7) monYr, Sum(DocTotal) as MonthlySales, Count(DocTotal) as MonthlyCount FROM `Order_order` where SalesPersonCode IN ({SalesEmployeeCode_list})  and ((CreateDate >='{CurrentYearComplete}') and (CreateDate <='{NextYearComplete}') ) group by monYr"
            monsl = Order.objects.raw(sql_query)
            for desc in monsl:
                monthYear = desc.monYr.split('-')
                month = int(monthYear[1])
                nextyear = int(monthYear[0])+1
                if month == 1:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jan") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 2:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Feb") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 3:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Mar") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 4:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Apr") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 5:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("May") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 6:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jun") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 7:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jul") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 8:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Aug") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 9:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Sep") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 10:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Oct") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 11:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Nov") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 12:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Dec") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                else:
                    print(month)
            
            monSales = ser(monSales)
            return Response({"message": "success","status": 200,"data":monSales})
        else:
            monSales = ser(monSales)
            return Response({"message": "Sales Employee Code Not Found","status": 201,"data":monSales})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})

def ser(arr):
    return arr[3:] + arr[:3]

#added by millan on 15-11-2022 for target create, update and list
def months_check(months, qt1, qt2, qt3, qt4):
    q1 = q2 = q3 = q4 = 0
    for mo in months:
        if mo['qtr'] == 1:
            q1 = q1 + int(mo['amount'])
        elif mo['qtr'] == 2:
            q2 = q2 + int(mo['amount'])
        elif mo['qtr'] == 3:
            q3 = q3 + int(mo['amount'])
        elif mo['qtr'] == 4:
            q4 = q4 + int(mo['amount'])

    if q1 != qt1:
        return {"message": "The months total of Qtr 1 should be equal to Q1 value", "data": q1}
    elif q2 != qt2:
        return {"message": "The months total of Qtr 2 should be equal to Q2 value", "data": q2}
    elif q3 != qt3:
        return {"message": "The months total of Qtr 3 should be equal to Q3 value", "data": q3}
    elif q4 != qt4:
        return {"message": "The months total of Qtr 4 should be equal to Q4 value", "data": q4}
    else:
        return "ok"

#Target Create API
@api_view(['POST'])
def target_create(request):
    try:
        TargetFor = request.data['TargetFor']
        amount = request.data['amount']
        monthYear = request.data['monthYear']
        qtr = request.data['qtr']
        department = request.data['department']

        SalesPersonCode = request.data['SalesPersonCode']
        reportingTo = request.data['reportingTo'].strip()
        CreatedDate = request.data['CreatedDate']
        if reportingTo == "":
            model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr, SalesPersonCode_id=SalesPersonCode, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        else:
            model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr, SalesPersonCode_id=SalesPersonCode, reportingTo_id=reportingTo, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

        model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr, SalesPersonCode_id=SalesPersonCode,reportingTo_id=reportingTo, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        model.save()

        tgt = Target.objects.latest('id')

        return Response({"message": "Success", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

@api_view(['POST'])
def targetqtm_create(request):

    try:
        if request.data['id'] != "":
            SalesPersonCode = request.data['SalesPersonCode']
            reportingTo = request.data['reportingTo'].strip()
            YearTarget = request.data['YearTarget']
            q1 = int(request.data['q1'])
            q2 = int(request.data['q2'])
            q3 = int(request.data['q3'])
            q4 = int(request.data['q4'])

            CreatedDate = request.data['CreatedDate']
            UpdatedDate = request.data['UpdatedDate']

            if Targetqty.objects.filter(pk=request.data['id']).exists():
                qtymodel = Targetqty.objects.get(pk=request.data['id'])
            else:
                return Response({"message": "Qtr info does not exists", "status": "201", "data": []})

            YearTargetAmount = Targetyr.objects.get(pk=YearTarget).YearTarget
            print(YearTargetAmount)
            print(q1+q2+q3+q4)

            if YearTargetAmount != (q1+q2+q3+q4):
                return Response({"message": "YearTarget should be equal to all quater", "status": "201", "data": []})
            elif (q1 < 1 or q2 < 1 or q3 < 1 or q4 < 1):
                return Response({"message": "All Qtr should be fill", "status": "201", "data": []})
            elif SalesPersonCode == reportingTo:
                return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
            else:

                if reportingTo == "" or reportingTo == "0":
                    qtymodel.SalesPersonCode_id = SalesPersonCode
                    qtymodel.YearTarget_id = YearTarget
                    qtymodel.q1 = q1
                    qtymodel.q2 = q2
                    qtymodel.q3 = q3
                    qtymodel.q4 = q4
                    qtymodel.CreatedDate = CreatedDate
                    qtymodel.UpdatedDate = CreatedDate
                else:
                    qtymodel.SalesPersonCode_id = SalesPersonCode
                    qtymodel.reportingTo_id = reportingTo
                    qtymodel.YearTarget_id = YearTarget
                    qtymodel.q1 = q1
                    qtymodel.q2 = q2
                    qtymodel.q3 = q3
                    qtymodel.q4 = q4
                    qtymodel.CreatedDate = CreatedDate
                    qtymodel.UpdatedDate = CreatedDate
                qtymodel.save()
                tgt = Targetqty.objects.latest('id')
                #print(tgt.id)
                if len(request.data['monthly']) == 12:
                    months = request.data['monthly']
                    if months[0]['amount'] < 1 or months[1]['amount'] < 1 or months[2]['amount'] < 1 or months[3]['amount'] < 1 or months[4]['amount'] < 1 or months[5]['amount'] < 1 or months[6]['amount'] < 1 or months[7]['amount'] < 1 or months[8]['amount'] < 1 or months[9]['amount'] < 1 or months[10]['amount'] < 1 or months[11]['amount'] < 1:
                        return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
                    else:

                        chk = months_check(
                            request.data['monthly'], request.data['q1'], request.data['q2'], request.data['q3'], request.data['q4'])

                        if chk == "ok":
                            if request.data['monthly'][0]["id"] != "":
                                for mo in months:
                                    mont = Target.objects.get(pk=mo['id'])
                                    print(mo['id'])
                                    print(mont)
                                    mont.YearTarget_id = YearTarget
                                    mont.amount = mo['amount']
                                    mont.monthYear = mo['monthYear']
                                    mont.SalesPersonCode_id = SalesPersonCode
                                    mont.qtr = mo['qtr']
                                    mont.CreatedDate = mo['CreatedDate']
                                    mont.UpdatedDate = mo['CreatedDate']
                                    mont.save()
                            else:
                                for mo in months:
                                    mont = Target(YearTarget_id=YearTarget, amount=mo['amount'], monthYear=mo['monthYear'],SalesPersonCode_id=SalesPersonCode, qtr=mo['qtr'], CreatedDate=mo['CreatedDate'], UpdatedDate=mo['CreatedDate'])
                                    mont.save()
                            return Response({"message": "Success", "status": "200", "data": []})
                        else:
                            print(chk)
                            return Response({"message": chk['message'], "status": "201", "data": chk['data']})

                else:
                    return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
        else:
            #StartYear = int(request.data['StartYear'])
            #EndYear = int(request.data['EndYear'])
            SalesPersonCode = request.data['SalesPersonCode']
            #Department = request.data['Department']
            reportingTo = request.data['reportingTo'].strip()
            YearTarget = request.data['YearTarget']
            q1 = int(request.data['q1'])
            q2 = int(request.data['q2'])
            q3 = int(request.data['q3'])
            q4 = int(request.data['q4'])

            CreatedDate = request.data['CreatedDate']
            UpdatedDate = request.data['UpdatedDate']

            if len(Targetqty.objects.filter(YearTarget=YearTarget, SalesPersonCode=SalesPersonCode)) > 0:
                return Response({"message": "Already exist with this Financial Year", "status": "201", "data": []})
            YearTargetAmount = Targetyr.objects.get(pk=YearTarget).YearTarget
            print(YearTargetAmount)
            print(q1+q2+q3+q4)

            if YearTargetAmount != (q1+q2+q3+q4):
                return Response({"message": "YearTarget should be equal to all quater", "status": "201", "data": []})
            elif (q1 < 1 or q2 < 1 or q3 < 1 or q4 < 1):
                return Response({"message": "All Qtr should be fill", "status": "201", "data": []})
            elif SalesPersonCode == reportingTo:
                return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
            else:

                if reportingTo == "" or reportingTo == "0":
                    model = Targetqty(SalesPersonCode_id=SalesPersonCode, YearTarget_id=YearTarget, q1=q1, q2=q2, q3=q3, q4=q4, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
                else:
                    model = Targetqty(SalesPersonCode_id=SalesPersonCode, reportingTo_id=reportingTo, YearTarget_id=YearTarget, q1=q1, q2=q2, q3=q3, q4=q4, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

                    #print("reportingTo_id="+str(reportingTo))

                model.save()
                tgt = Targetqty.objects.latest('id')
                #print(tgt.id)
                if len(request.data['monthly']) == 12:
                    months = request.data['monthly']
                    if months[0]['amount'] < 1 or months[1]['amount'] < 1 or months[2]['amount'] < 1 or months[3]['amount'] < 1 or months[4]['amount'] < 1 or months[5]['amount'] < 1 or months[6]['amount'] < 1 or months[7]['amount'] < 1 or months[8]['amount'] < 1 or months[9]['amount'] < 1 or months[10]['amount'] < 1 or months[11]['amount'] < 1:
                        return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
                    else:
                        chk = months_check(
                            request.data['monthly'], request.data['q1'], request.data['q2'], request.data['q3'], request.data['q4'])

                        if chk == "ok":
                            for mo in months:
                                mont = Target(YearTarget_id=YearTarget, amount=mo['amount'], monthYear=mo['monthYear'],
                                              SalesPersonCode_id=SalesPersonCode, qtr=mo['qtr'], CreatedDate=mo['CreatedDate'], UpdatedDate=mo['CreatedDate'])
                                mont.save()
                            return Response({"message": "Success", "status": "200", "data": []})
                        else:
                            print(chk)
                            return Response({"message": chk['message'], "status": "201", "data": chk['data']})
                else:
                    return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

def check_year(yeardata):
    StartYear = yeardata[0]['StartYear']
    EndYear = yeardata[0]['EndYear']
    Department = yeardata[0]['Department']
    reportingTo = yeardata[0]['reportingTo']

    if Targetyr.objects.filter(StartYear=StartYear, EndYear=EndYear, SalesPersonCode=reportingTo, Department=Department).exists():
        YearTarget = Targetyr.objects.get(
            StartYear=StartYear, EndYear=EndYear, SalesPersonCode=reportingTo, Department=Department).YearTarget
        ttl = 0
        for dt in yeardata:
            ttl = ttl+int(dt['YearTarget'])
        if YearTarget >= ttl:
            return "ok"
        else:
            return "Team distribution total should be equal to Target Goal"
    else:
        return "ok"
#Target yr Create API

@api_view(['POST'])
def targetyr_create(request):
    try:
        yrs = request.data
        chk = check_year(yrs)
        if chk == "ok":
            for yr in yrs:
                StartYear = int(yr['StartYear'])
                EndYear = int(yr['EndYear'])
                SalesPersonCode = yr['SalesPersonCode']
                Department = yr['Department']
                reportingTo = yr['reportingTo'].strip()
                YearTarget = int(yr['YearTarget'])

                CreatedDate = yr['CreatedDate']
                UpdatedDate = yr['UpdatedDate']

                if len(Targetyr.objects.filter(StartYear=StartYear, EndYear=EndYear, SalesPersonCode=SalesPersonCode, Department=Department)) > 0:
                    return Response({"message": "Already exist with this Financial Year", "status": "201", "data": []})
                print(YearTarget)
                if SalesPersonCode == reportingTo:
                    return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
                elif StartYear == EndYear:
                    return Response({"message": "StartYear and EndYear are same", "status": "201", "data": []})
                else:

                    if reportingTo == "":
                        model = Targetyr(StartYear=StartYear, EndYear=EndYear, SalesPersonCode_id=SalesPersonCode,Department=Department, YearTarget=YearTarget, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
                    else:
                        model = Targetyr(StartYear=StartYear, EndYear=EndYear, SalesPersonCode_id=SalesPersonCode, Department=Department,reportingTo_id=reportingTo, YearTarget=YearTarget, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

                    model.save()
                    tgt = Targetyr.objects.latest('id')
                    #print(tgt.id)
            return Response({"message": "Success", "status": "200", "data": []})
        else:
            return Response({"message": chk, "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

#targetqty all API
@api_view(["POST"])
def target_all(request):
    SalesPersonCode = request.data['SalesPersonCode']
    target_obj = Target.objects.filter(SalesPersonCode=SalesPersonCode)
    target_json = TargetSerializer(target_obj, many=True)
    return Response({"message": "Success", "status": 200, "data": target_json.data})

#targetqty all API
@api_view(["POST"])
def targetqtm_all(request):
    YearTarget = request.data['YearTarget']
    targetqty_obj = Targetqty.objects.filter(YearTarget=YearTarget)
    if len(targetqty_obj) > 0:
        targetqty_json = TargetqtySerializer(targetqty_obj, many=True)
        m_obj = Target.objects.filter(YearTarget=YearTarget)
        m_json = TargetSerializer(m_obj, many=True)

        targetqty_json.data[0]["monthly"] = m_json.data

        return Response({"message": "Success", "status": 200, "data": targetqty_json.data})
    else:
        return Response({"message": "Success", "status": 200, "data": []})

#targetqty all API
@api_view(["POST"])
def targetyr_all(request):
    SalesPersonCode = request.data['SalesPersonCode']
    targetyr_obj = Targetyr.objects.filter(SalesPersonCode=SalesPersonCode)
    targetyr_json = TargetyrSerializer(targetyr_obj, many=True)
    return Response({"message": "Success", "status": 200, "data": targetyr_json.data})

@api_view(["POST"])
def targetyr_all_filter(request):
    try:
        dt = request.data
        tgt_obj = Targetyr.objects.filter(
            StartYear=dt['StartYear'], EndYear=dt['EndYear'], Department=dt['Department'], reportingTo=dt['reportingTo'])
        tgt_json = TargetyrSerializer(tgt_obj, many=True)
        return Response({"message": "success", "status": 200, "data": tgt_json.data})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#targetqty close
@api_view(["POST"])
def targetqty_close(request):
    id = request.data["id"]
    try:
        model = Targetqty.objects.filter(pk=id).update(status=1)
        return Response({"message": "Success", "Status": 200, "data": []})
    except Exception as e:
        return Response({"message": str(e), "Status": 200, "data": []})

#targetyr close
@api_view(["POST"])
def targetyr_close(request):
    id = request.data["id"]
    try:
        model = Targetyr.objects.filter(pk=id).update(status=1)
        return Response({"message": "Success", "Status": 200, "data": []})
    except Exception as e:
        return Response({"message": str(e), "Status": 200, "data": []})

#added by millan on 15-11-20222 for top 5 products sold by an employee
@api_view(["POST"])
def proSoldEmp(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']        
        top5Item = []
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
        
        SalesEmployeeCode_list = ",".join(SalesEmployeeCode_arr)

        if Order.objects.filter(SalesPersonCode__in = SalesEmployeeCode_arr).exists():
            sql_query = f"SELECT oo.id, ordl.UnitPrice, Max(ordl.Quantity) MaxQuantity, COUNT(ordl.Quantity) ItemQuantity, ii.ItemName, ic.CategoryName, oo.SalesPersonCode FROM Order_documentlines ordl left join Order_order oo on oo.id = ordl.OrderID left join Item_item ii on ii.ItemCode = ordl.ItemCode left join Item_category ic on ic.id = ii.CatID_id where SalesPersonCode IN ({SalesEmployeeCode_list}) group by ordl.ItemCode order by MaxQuantity Desc limit 5"
            
            pro5sold = Order.objects.raw(sql_query)
            
            for item in pro5sold:
                top5Item.append({"ItemName":item.ItemName, "CategoryName":item.CategoryName, "ItemQuantity":item.ItemQuantity, "MaxQuantity":item.MaxQuantity, "UnitPrice":item.UnitPrice})
            
            return Response({"message": "success","status": 200,"data":top5Item})
        else:
            top5Item = []
            return Response({"message": "Sales Employee Code Not Found","status": 201,"data":top5Item})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})

#top 5 customers based on sales person code and order
@api_view(["POST"])
def top5bp(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        
        if emp_obj.role.lower() == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role.lower() == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesPersonCode))
        
        if Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode_arr).exists():
            top2bp = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode_arr).values('CardCode').annotate(Total = Sum(F('DocTotal'))).order_by('-Total')[:5]
            print(top2bp)
            top5=[]
            for od in top2bp:                
                try:            
                    cd = BusinessPartner.objects.filter(CardCode = od['CardCode']).values('CardName')
                    top5.append({"CardCode":od['CardCode'], "CardName":cd[0]['CardName'], 'Total':od['Total']})
                except Exception as e:
                    top5.append({"CardCode":od['CardCode'], "CardName":od['CardCode'], 'Total':od['Total']})

            return Response({"message": "Success","status": 200,"data":top5})
        else:
            return Response({"message": "SalesPersonCode Not Found","status": 201,"data":[]})
        
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#added by millan on 17-11-2022
@api_view(["POST"])
def all_filter_reportingto(request):
    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            emps_all1 = []
            # .values('id', 'SalesEmployeeCode')
            emps_all = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            print(len(emps_all))
            print(SalesEmployeeCode)

            if len(emps_all) == 0:
                print(SalesEmployeeCode)
                return Response({"message": "Success", "status": 200, "data": []})
            else:
                emps_json = EmployeeSerializer(emps_all, many=True)
            return Response({"message": "Success", "status": 200, "data": emps_json.data})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


#added by millan on 12-10-2022 to get target of each year based on Sales person and the decide target and achieved target in that financial year
@api_view(["POST"])
def employee_target(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']        
            
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        print(emp_obj.role)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode_arr=[]
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
        
        print("SalesPersonCode")
        print(SalesPersonCode_arr)
        SalesPersonCode_list = ",".join(SalesPersonCode_arr)
        print(SalesPersonCode_list)
        
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        
        fyTarget =[
                {
                    "MonthlyTargetSales": 0,
                    "Month":  str("Jan") + "-" + str(NextYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Feb") + "-" + str(NextYr) ,
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Mar") + "-" + str(NextYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },        
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Apr") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("May") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Jun") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Jul") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Aug") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Sep") + "-" + str(CurrYr) ,
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Oct") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Nov") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Dec") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                }
                
            ]
        
        if Target.objects.filter(SalesPersonCode_id = SalesPersonCode).exists():
            
            sql_query = f"SELECT id, amount, Concat(SUBSTR(monthYear,6,7), '-', SUBSTR(monthYear,1,4)) as monYr, monthYear FROM Employee_target where SalesPersonCode_id = {SalesPersonCode} and (SUBSTR(monthYear,1,4) IN ({CurrYr}, {NextYr}) ) "
            print(sql_query)
            
            fytgt = Target.objects.raw(sql_query)
            for fyt in fytgt:
                month = int(fyt.monthYear.split('-')[1])
                fyTarget[month-1]['MonthlyTargetSales'] = fyt.amount
                    
        if Order.objects.filter(SalesPersonCode__in = SalesPersonCode_arr).exists():
            
            #sql_query_ord = f"SELECT Distinct(id), SUM(DocTotal) as OrderAchieved, SUBSTR(CreateDate,1,7) as monYr FROM Order_order where SalesPersonCode = {SalesPersonCode} and (SUBSTR(CreateDate,1,4) IN ({CurrYr}, {NextYr})) and CancelStatus = 'csNo' "
            
            sql_query_ord = f"SELECT id, sum(DocTotal) as OrderAchieved, SUBSTR(CreateDate,1,7) as monYr, SUBSTR(CreateDate,6,2) as month FROM Order_order where SalesPersonCode IN ({SalesPersonCode_list}) and (SUBSTR(CreateDate,1,4) IN ({CurrYr}, {NextYr})) and CancelStatus = 'csNo' group by SUBSTR(CreateDate,6,2);"
            
            print(sql_query_ord)
            
            ord_sl = Order.objects.raw(sql_query_ord)            
            
            for ord in ord_sl:
                fyTarget[int(ord.month)-1]['MonthlyAchievedSales'] = ord.OrderAchieved
                
            fyTarget = ser(fyTarget)
            return Response({"message": "success","status": 200,"data":fyTarget})
        else:
            fyTarget = ser(fyTarget)
            return Response({"message": "SalesPersonCode Not Found","status": 201,"data":fyTarget})

    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 13-10-2022 to get annual target, achieved target and order placed in a finanical year 
@api_view(["POST"])
def target_anu_ach(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']        
            
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        print(emp_obj.role)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode_arr=[]
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
        
        print("SalesPersonCode")
        print(SalesPersonCode_arr)
        SalesPersonCode_list = ",".join(SalesPersonCode_arr)
        print(SalesPersonCode_list)
        
        #{"SalesPersonCode":105}
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        
        TargetFyYr = []
        if Targetyr.objects.filter(SalesPersonCode_id = SalesPersonCode).exists():
            sql_query = f"SELECT id, Sum(YearTarget) YearTarget FROM Employee_targetyr where SalesPersonCode_id = {SalesPersonCode} and StartYear={CurrYr} and EndYear={NextYr}"
            print(sql_query)
            fysl = Targetyr.objects.raw(sql_query)
            print(fysl)
            
            sql_query_ord = f"SELECT id, SUM(NetTotal) AchievedTarget,  Count(CancelStatus) ConfirmedOrder FROM Order_order where SalesPersonCode in ({SalesPersonCode_list}) and (SUBSTR(CreateDate,1,4) IN ({CurrYr})) and CancelStatus = 'csNo' "
            ord_sl = Order.objects.raw(sql_query_ord)
            
            #for fy in fysl:
                
            finalfy = {
                "AnnualTarget": fysl[0].YearTarget,
                "AchievedTarget": 0,
                "ConfirmedOrder": 0,
                "FinancialYear": FinanYr,
            }
                
            for ord in ord_sl:
                finalfy['AchievedTarget'] = ord.AchievedTarget
                finalfy['ConfirmedOrder'] = ord.ConfirmedOrder
                    
                TargetFyYr.append(finalfy)
            return Response({"message": "success","status": 200,"data":TargetFyYr})
        else:
            TargetFyYr = [ 
                {
                    "AnnualTarget": 0,
                    "AchievedTarget": 0,
                    "ConfirmedOrder": 0,
                    "FinancialYear": FinanYr
                }
            ]       
            return Response({"message": "SalesPersonCode Not Found","status": 200,"data":TargetFyYr})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

@api_view(["POST"])
def total_sale(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']        
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
        
        SalesEmployeeCode_list = ",".join(SalesEmployeeCode_arr)
        ttl = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode_arr, CancelStatus = 'csNo').values_list('DocTotal', flat=True)
        print(ttl)
        total_sale=0
        for tt in ttl:
            total_sale=float(total_sale)+float(tt)
        print(total_sale)
        
        return Response({"message": "Success","status": 200,"data":[{"TotalSale":total_sale}]})
        #return Response({"message": "Success","status": 200,"data":[]})
    except Exception as e:    
        return Response({"message": str(e),"status": 201,"data":[]})

#get total outstanding by sale person     
@api_view(["POST"])
def total_outstanding(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']        
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesEmployeeCode_arr=[]
            for emp in emps:
                SalesEmployeeCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesEmployeeCode_arr=[]
            SalesEmployeeCode_arr.append(str(SalesEmployeeCode))
        
        SalesEmployeeCode_list = ",".join(SalesEmployeeCode_arr)
        
        #total sale
        ttl = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode_arr, CancelStatus = 'csNo').values_list('DocTotal', flat=True)
        print(ttl)
        total_sale=0
        for tt in ttl:
            total_sale=float(total_sale)+float(tt)
        print(total_sale)
        
        
        #total payment received
        pmt = Payment.objects.filter(createdBy__in=SalesEmployeeCode_arr).values_list('ReceivedAmount', flat=True)
        print(pmt)
        total_pmt=0
        for pm in pmt:
            total_pmt=float(total_pmt)+float(pm)
        print(total_pmt)
        ttl_out = total_sale - total_pmt
        return Response({"message": "Success","status": 200,"data":[{"TotalOutstanding":ttl_out}]})
        #return Response({"message": "Success","status": 200,"data":[]})
    except Exception as e:    
        return Response({"message": str(e),"status": 201,"data":[]})
        
