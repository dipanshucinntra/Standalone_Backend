# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import LeadForm  
from .models import *
from Employee.models import Employee  


from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Lead Create API
@api_view(['POST'])
def create(request):
    leads = request.data
    log = []
    
    for lead in leads:
        date=lead['date']
        location=lead['location']
        companyName=lead['companyName']
        numOfEmployee = lead['numOfEmployee']
        turnover = lead['turnover']
        source=lead['source']
        contactPerson=lead['contactPerson']
        designation=lead['designation']
        phoneNumber=lead['phoneNumber']
        message=lead['message']
        email=lead['email']
        status=lead['status']
        leadType=lead['leadType']
        productInterest=lead['productInterest']
        assignedTo_id=lead['assignedTo']
        employeeId_id=lead['employeeId']
        timestamp=lead['timestamp']
        
        if Lead.objects.filter(phoneNumber=phoneNumber).exists():
            log.append(phoneNumber)
        else:
            model=Lead(date=date, location=location, companyName=companyName, numOfEmployee=numOfEmployee, turnover=turnover, source=source, status=status, leadType=leadType, contactPerson=contactPerson, designation=designation, phoneNumber=phoneNumber, message=message, email=email, productInterest=productInterest, assignedTo_id=assignedTo_id, employeeId_id=employeeId_id, timestamp=timestamp)
            model.save()
        print(log)
        if len(log) > 0:
            log_msg = "Mobile number is already exist: "+str(log)
        else:
            log_msg = 'successful'
    return Response({"message":log_msg,"status":"200","data":[]})


#Lead Chat Create API
@api_view(['POST'])
def chatter(request):
    try:
        Message = request.data['Message']
        Lead_Id = request.data['Lead_Id']
        Emp_Id = request.data['Emp_Id']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        model = Chatter(Message=Message, Lead_Id=Lead_Id, Emp_Id=Emp_Id, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        chat = Chatter.objects.latest('id')
        print(chat.id)
        return Response({"message":"Success","status":200,"data":[{"id":chat.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":201,"data":[str(e)]})

#Chatter All API
@api_view(["POST"])
def chatter_all(request):
    Lead_Id=request.data['Lead_Id']
    print(Lead_Id)
    chat_obj = Chatter.objects.filter(Lead_Id=Lead_Id).order_by("id")
    chat_json = ChatterSerializer(chat_obj, many=True)
    return Response({"message": "Success","status": 200,"data":chat_json.data})

#Lead All API
@api_view(["GET"])
def all(request):
    leads_obj = Lead.objects.all()        
    lead_json = LeadSerializer(leads_obj, many=True)
    return Response({"message": "Success","status": 200,"data":lead_json.data})

#Lead All Filter API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data

    leadType = request.data['leadType']
        
    if json_data['assignedTo']!="":
        SalesPersonID = json_data['assignedTo']
        
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
    
    
    if len(json_data) == 0:
        leads_obj = Lead.objects.all().order_by("-id")
        leads_json = LeadSerializer(leads_obj, many=True)
        return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        #print(json_data.keys()[0])
        #if json_data['U_FAV']
        for ke in json_data.keys():
            if ke =='assignedTo' :
                if json_data['assignedTo'] !='':
                    if leadType !="All":
                        leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")
                    else:
                        leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID).order_by("-id")                        
                        
                    if len(leads_obj) ==0:
                        return Response({"message": "Success","status": 200,"data":[]})
                    else:
                        leads_json = LeadSerializer(leads_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":leads_json.data})
            elif ke =='employeeId' :
                if json_data['employeeId'] !='':
                    if leadType !="All":
                        leads_obj = Lead.objects.filter(employeeId=json_data['employeeId'], leadType=leadType).order_by("-id")
                    else:
                        leads_obj = Lead.objects.filter(employeeId=json_data['employeeId']).order_by("-id")
                        
                    if len(leads_obj) ==0:
                        return Response({"message": "Success","status": 200,"data":[]})
                    else:
                        leads_json = LeadSerializer(leads_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":leads_json.data})
            else:
                return Response({"message": "Success","status": 200,"data":[]})


#Lead All Filter API
@api_view(["POST"])
def all_filter_old(request):
    json_data = request.data
        
    if json_data['assignedTo']!="":
        SalesPersonID = json_data['assignedTo']
        
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
    
    
    if len(json_data) == 0:
        leads_obj = Lead.objects.all().order_by("-id")
        leads_json = LeadSerializer(leads_obj, many=True)
        return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        #print(json_data.keys()[0])
        #if json_data['U_FAV']
        for ke in json_data.keys():
            if ke =='assignedTo' :
                if json_data['assignedTo'] !='':
                    leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID).order_by("-id")
                    if len(leads_obj) ==0:
                        return Response({"message": "Success","status": 200,"data":[]})
                    else:
                        leads_json = LeadSerializer(leads_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":leads_json.data})
            elif ke =='employeeId' :
                if json_data['employeeId'] !='':
                    leads_obj = Lead.objects.filter(employeeId=json_data['employeeId']).order_by("-id")
                    if len(leads_obj) ==0:
                        return Response({"message": "Success","status": 200,"data":[]})
                    else:
                        leads_json = LeadSerializer(leads_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":leads_json.data})
            else:
                return Response({"message": "Success","status": 200,"data":[]})

#Lead One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    lead_obj = Lead.objects.get(id=id)
    lead_json = LeadSerializer(lead_obj)
    return Response({"message": "Success","status": 200,"data":[lead_json.data]})

#Lead Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Lead.objects.get(pk = fetchid)
        model.date  = request.data['date']
        model.location  = request.data['location']
        model.companyName  = request.data['companyName']
        model.numOfEmployee  = request.data['numOfEmployee']
        model.turnover  = request.data['turnover']
        model.source  = request.data['source']
        model.contactPerson  = request.data['contactPerson']
        model.designation  = request.data['designation']
        model.phoneNumber  = request.data['phoneNumber']
        model.message  = request.data['message']
        model.email  = request.data['email']
        model.status  = request.data['status']
        model.leadType  = request.data['leadType']
        model.productInterest  = request.data['productInterest']
        model.assignedTo_id  = request.data['assignedTo']
        model.employeeId_id  = request.data['employeeId']
        model.timestamp  = request.data['timestamp']

        model.save()
        context = {
            "id":request.data['id'],
            "date ":request.data['date'],
            "location ":request.data['location'],
            "companyName ":request.data['companyName'],
            "numOfEmployee ":request.data['numOfEmployee'],
            "turnover ":request.data['turnover'],
            "source ":request.data['source'],
            "contactPerson ":request.data['contactPerson'],
            "designation ":request.data['designation'],
            "phoneNumber ":request.data['phoneNumber'],
            "message ":request.data['message'],
            "email ":request.data['email'],
            "productInterest ":request.data['productInterest'],
            "assignedTo ":request.data['assignedTo'],
            "employeeId ":request.data['employeeId'],
            "timestamp ":request.data['timestamp']
        }

        return Response({"message":"successful","status":200,"data":[context]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})

#Lead delete

@api_view(['POST'])
def delete(request):
    fetchids=request.data['id']
    naid = []
    for fetchid in fetchids:
        if Lead.objects.filter(pk=fetchid).exists():
           fetchdata=Lead.objects.filter(pk=fetchid).delete()
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})
             #return Response({"message":"Id wrong","status":"201","data":[]})




# @api_view(['POST'])
# def delete(request):
    # fetchid=request.data['id']
    # try:
        # fetchdata=Lead.objects.filter(pk=fetchid).delete()
        # return Response({"message":"successful","status":"200","data":[]})
    # except:
         # return Response({"message":"Id wrong","status":"201","data":[]})

#Lead Assign
@api_view(['POST'])
def assign(request):
    fetchids=request.data['id']
    empid=request.data['employeeId']
    emp=Employee.objects.get(pk=empid)
    naid = []
    for fetchid in fetchids:
        if Lead.objects.filter(pk=fetchid).exists():
           model=Lead.objects.get(pk=fetchid)
           model.assignedTo = emp
           model.save()
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})
             #return Response({"message":"Id wrong","status":"201","data":[]})



#Type Create API
@api_view(['POST'])
def type_create(request):
    try:
        Name = request.data['Name']
        CreatedDate = request.data['CreatedDate']
        CreatedTime = request.data['CreatedTime']

        model=Type(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
        
        model.save()
        
        tp = Type.objects.latest('id')        
        
        return Response({"message":"successful","status":200,"data":[{"id":tp.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})

#LeadType All API
@api_view(["GET"])
def type_all(request):
    type_obj = Type.objects.all()        
    type_json = TypeSerializer(type_obj, many=True)
    return Response({"message": "Success","status": 200,"data":type_json.data})

#CaseType All API
@api_view(["GET"])
def casetype_all(request):
    casetype_obj = CaseType.objects.all()        
    casetype_json = CaseTypeSerializer(casetype_obj, many=True)
    return Response({"message": "Success","status": 200,"data":casetype_json.data})


#Type delete
@api_view(['POST'])
def type_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Type.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})


#Source Create API
@api_view(['POST'])
def source_create(request):
    Name = request.data['Name']    
    if Source.objects.filter(Name=Name).exists():        
        return Response({"message":"Already exist","status":409,"data":[]})
    else:        
        try:
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            model=Source(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)            
            model.save()            
            sc = Source.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":sc.id}]})
        except Exception as e:
            return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})        

#Type Update API
@api_view(['POST'])
def source_update(request):
    fetchid = request.data['id']
    try:
        model = Source.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})



#SourceType All API
@api_view(["GET"])
def source_all(request):
    source_obj = Source.objects.all()        
    source_json = SourceSerializer(source_obj, many=True)
    return Response({"message": "Success","status": 200,"data":source_json.data})

#Source delete
@api_view(['POST'])
def source_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Source.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

