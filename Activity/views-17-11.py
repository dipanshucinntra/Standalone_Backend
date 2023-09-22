from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import ActivityForm  
from .models import *
from Employee.models import Employee
from Lead.models import *

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

@api_view(['POST'])
def followup(request):
    try:
        SourceID = request.data['SourceID']
        Comment = request.data['Comment']
        Emp = request.data['Emp']
        From = request.data['From']
        To = request.data['From']
        Time = request.data['Time']
        Type = request.data['Type']
        SourceType = request.data['SourceType']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        
        model = Activity(SourceID=SourceID, Comment=Comment, Emp=Emp, From=From, To=To, Time=Time, Type=Type, SourceType=SourceType, CreateDate=CreateDate, CreateTime=CreateTime)        
        
        model.full_clean()
        
        model.save()
        act = Activity.objects.latest('id')
        print(act.id)
        
        SourceID = request.data['SourceID']
        Message = request.data['Comment']
        Emp = request.data['Emp']
        Mode = request.data['Mode']
        Emp_Name = request.data['Emp_Name']
        SourceType = request.data['SourceType']
        UpdateDate = request.data['CreateDate']
        UpdateTime = request.data['CreateTime']

        chat = Chatter(Message=Message, SourceID=SourceID, SourceType=SourceType, Emp=Emp, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime, Mode=Mode)
        
        chat.save()
        
        if SourceType=='Lead':
            led = Lead.objects.get(pk=SourceID)
            led.status = "Follow Up"
            led.save()
        
        return Response({"message":"Success","status":200,"data":[]})
    except Exception as e:
        return Response({"message":"Can not create","status":201,"data":[{"Error":str(e)}]})


#Opp Activity Create API
@api_view(['POST'])
def create(request):
    try:
        SourceID = request.data['SourceID']
        Subject = request.data['Subject']
        Comment = request.data['Comment']
        Name = request.data['Name']
        RelatedTo = request.data['RelatedTo']
        Emp = request.data['Emp']
        Title = request.data['Title']
        Description = request.data['Description']
        From = request.data['From']
        To = request.data['To']
        Time = request.data['Time']
        Allday = request.data['Allday']
        Location = request.data['Location']
        Host = request.data['Host']
        Participants = request.data['Participants']
        Document = request.data['Document']
        Repeated = request.data['Repeated']
        Priority = request.data['Priority']
        ProgressStatus = request.data['ProgressStatus']
        Type = request.data['Type']
        SourceType = request.data['SourceType']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        
        model = Activity(SourceID=SourceID, Subject=Subject, Comment=Comment, Name=Name, RelatedTo=RelatedTo, Emp=Emp, Title=Title, Description=Description, From=From, To=To, Time=Time, Allday=Allday, Location=Location, Host=Host, Participants=Participants, Document=Document, Repeated=Repeated, Priority=Priority, ProgressStatus=ProgressStatus, Type=Type, SourceType=SourceType, CreateDate=CreateDate, CreateTime=CreateTime)
        
        model.save()
        act = Activity.objects.latest('id')
        print(act.id)
        return Response({"message":"Success","status":"200","data":[]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})


#Opp Map Create API
@api_view(['POST'])
def maps(request):
    try:
        Lat = request.data['Lat']
        Long = request.data['Long']
        Address = request.data['Address']
        Emp_Id = request.data['Emp_Id']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        
        model = Maps(Lat=Lat, Long=Long, Address=Address, Emp_Id=Emp_Id, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        mp = Maps.objects.latest('id')
        print(mp.id)
        return Response({"message":"Success","status":200,"data":[{"id":mp.id}]})
    except:
        return Response({"message":"Can not create","status":201,"data":[]})

#Opp Map Create API
@api_view(['POST'])
def chatter(request):
    try:
        Message = request.data['Message']
        SourceID = request.data['SourceID']
        SourceType = request.data['SourceType']
        Emp = request.data['Emp']
        Mode = request.data['Mode']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        model = Chatter(Message=Message, SourceID=SourceID, SourceType=SourceType, Emp=Emp, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime, Mode=Mode)
        
        model.save()
        chat = Chatter.objects.latest('id')
        print(chat.id)
        if SourceType=='Lead':
            led = Lead.objects.get(pk=SourceID)
            led.status = "Follow Up"
            led.save()
        return Response({"message":"Success","status":200,"data":[{"id":chat.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":201,"data":[str(e)]})


#Activity All API
@api_view(["POST"])
def all(request):
    Emp=request.data['Emp']
    act_obj = Activity.objects.filter(Emp=Emp).order_by("-id")
    act_json = ActivitySerializer(act_obj, many=True)
    return Response({"message": "Success","status": 200,"data":act_json.data})

#Activity All Filter API
@api_view(["POST"])
def all_filter(request):
    Emp=request.data['Emp']
    date=request.data['date']
    #"SELECT * FROM `Activity_activity` WHERE `From` <= '"+date+"' and `To` >= '"+date+"'"
    act_obj = Activity.objects.filter(Emp=Emp, From__lte=date, To__gte=date).order_by("-id")
    act_json = ActivitySerializer(act_obj, many=True)
    return Response({"message": "Success","status": 200,"data":act_json.data})



#Chatter All API
@api_view(["POST"])
def chatter_all(request):
    Emp=request.data['Emp']
    SourceID=request.data['SourceID']
    SourceType=request.data['SourceType']
    chat_obj = Chatter.objects.filter(Emp=Emp, SourceType=SourceType, SourceID=SourceID).order_by("id")
    chat_json = ChatterSerializer(chat_obj, many=True)
    return Response({"message": "Success","status": 200,"data":chat_json.data})


#Activity Delete API
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        Activity.objects.get(pk=fetchid).delete()
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
         return Response({"message":"Id wrong","status":201,"data":[str(e)]})


#Activity One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    act_obj = Activity.objects.get(id=id)
    act_json = ActivitySerializer(act_obj)
    return Response({"message": "Success","status": 200,"data":[act_json.data]})

#maps One API
@api_view(["POST"])
def map_one(request):
    Emp_Id=request.data['Emp_Id']    
    map_obj = Maps.objects.filter(Emp_Id=Emp_Id)
    map_json = MapsSerializer(map_obj, many=True)
    return Response({"message": "Success","status": 200,"data":[map_json.data]})

#Map Filter API
@api_view(["POST"])
def map_filter(request):
    Emp=request.data['Emp_Id']
    date=request.data['UpdateDate']
    act_obj = Maps.objects.filter(Emp_Id=Emp, UpdateDate=date).order_by("-id")
    act_json = MapsSerializer(act_obj, many=True)
    return Response({"message": "Success","status": 200,"data":act_json.data})


#Map all
@api_view(["POST"])
def map_all(request):

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
            mps = []
            print(SalesEmployeeCode)
            for scode in SalesEmployeeCode:
                emp = Employee.objects.get(SalesEmployeeCode=scode)
                mp_obj = Maps.objects.filter(Emp_Id=emp.id).order_by("-id")[:1]
                if len(mp_obj) !=0:
                    mp_json = MapsSerializer(mp_obj, many=True)
                    print(mp_json.data[0])
                    mps.append(mp_json.data[0])
            return Response({"message": "Success","status": 200,"data":mps})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

#Activity Status Update API
@api_view(['POST'])
def status(request):
    fetchid = request.data['id']
    try:
        model = Activity.objects.get(pk = fetchid)        
        if int(model.Status) == 0:
            model.Status = 1
            model.save()
            print("if")
        else:
            #model.Status = 0
            #model.save()
            print("else")
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message":"unsuccess","status":201,"data":[{"Error":str(e)}]})


#Activity Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Activity.objects.get(pk = fetchid)
        
        #model.SourceID = request.data['SourceID']
        #model.SourceType = request.data['SourceType']
        #model.Type = request.data['Type']
        model.Subject = request.data['Subject']
        model.Comment = request.data['Comment']
        model.Name = request.data['Name']
        model.RelatedTo = request.data['RelatedTo']
        model.Emp = request.data['Emp']
        model.Title = request.data['Title']
        model.Description = request.data['Description']
        model.From = request.data['From']
        model.To = request.data['To']
        model.Time = request.data['Time']
        model.Allday = request.data['Allday']
        model.Location = request.data['Location']
        model.Host = request.data['Host']
        model.Participants = request.data['Participants']
        model.Document = request.data['Document']
        model.Priority = request.data['Priority']
        model.ProgressStatus = request.data['ProgressStatus']
        model.Repeated = request.data['Repeated']


        model.save()
        context = {
            #'SourceID':request.data['SourceID'],
            #'SourceType':request.data['SourceType'],
            #'Type':request.data['Type'],
            'Subject':request.data['Subject'],
            'Comment':request.data['Comment'],
            'Name':request.data['Name'],
            'RelatedTo':request.data['RelatedTo'],
            'Emp':request.data['Emp'],
            'Title':request.data['Title'],
            'Description':request.data['Description'],
            'From':request.data['From'],
            'To':request.data['To'],
            'Time':request.data['Time'],
            'Allday':request.data['Allday'],
            'Location':request.data['Location'],
            'Host':request.data['Host'],
            'Participants':request.data['Participants'],
            'Document':request.data['Document'],
            'Priority':request.data['Priority'],
            'ProgressStatus':request.data['ProgressStatus'],
            'Repeated':request.data['Repeated']
            }

        return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[]})

#Activity All Filter by date API
@api_view(["POST"])
def all_filter_by_date(request):
    try:
        Emp=request.data['Emp']
        date=request.data['date']
        act_obj = Activity.objects.filter(Emp=Emp, To = date).order_by("-id")
        act_json = ActivitySerializer(act_obj, many=True)
        return Response({"message": "Success","status": 200,"data":act_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":""})
        