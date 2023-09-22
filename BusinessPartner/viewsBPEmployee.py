from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import BPEmployee  
from .models import BPEmployee  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPEmployeeSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#BPEmployee Create API
@api_view(['POST'])
def create(request):
    try:
        Title = request.data['Title']
        FirstName = request.data['FirstName']
        MiddleName = request.data['MiddleName']
        LastName = request.data['LastName']
        Position = request.data['Position']
        Address = request.data['Address']
        MobilePhone = request.data['MobilePhone']
        Fax = request.data['Fax']
        E_Mail = request.data['E_Mail']
        Remarks1 = request.data['Remarks1']
        DateOfBirth = request.data['DateOfBirth']
        Gender = request.data['Gender']
        Profession = request.data['Profession']
        CardCode = request.data['CardCode']
        
        U_BPID = request.data['U_BPID']
        U_BRANCHID = "1" #request.data['U_BRANCHID']
        U_NATIONALTY = request.data['U_NATIONALTY']
        
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        
        model = BPEmployee(U_BRANCHID=U_BRANCHID, U_BPID=U_BPID, CardCode=CardCode, Title=Title, FirstName=FirstName, MiddleName=MiddleName, LastName=LastName, Position=Position, Address=Address, MobilePhone=MobilePhone, Fax=Fax, E_Mail=E_Mail, Remarks1=Remarks1, U_NATIONALTY=U_NATIONALTY, DateOfBirth=DateOfBirth, Gender=Gender, Profession=Profession, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)

        model.save()    
        em = BPEmployee.objects.latest('id')
        model.InternalCode = em.id
        model.save()
        return Response({"message":"successful","status":200, "data":[{"id":em.id,"InternalCode":em.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#BPEmployee All API
@api_view(["POST"])
def all(request):    
    CardCode=request.data['CardCode']
    bpemployee_obj = BPEmployee.objects.filter(CardCode=CardCode) 
    bpemployee_json = BPEmployeeSerializer(bpemployee_obj, many=True)
    return Response({"message": "Success","status": 200,"data":bpemployee_json.data})


#BPEmployee One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    bpemployee_obj = BPEmployee.objects.get(id=id)
    bpemployee_json = BPEmployeeSerializer(bpemployee_obj)
    return Response({"message": "Success","status": 200,"data":[bpemployee_json.data]})

#BPEmployee Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = BPEmployee.objects.get(pk = fetchid)
        
        model.Title = request.data['Title']
        model.FirstName = request.data['FirstName']
        model.MiddleName = request.data['MiddleName']
        model.LastName = request.data['LastName']
        model.Position = request.data['Position']
        model.Address = request.data['Address']
        model.MobilePhone = request.data['MobilePhone']
        model.Fax = request.data['Fax']
        model.E_Mail = request.data['E_Mail']
        model.Remarks1 = request.data['Remarks1']
        model.DateOfBirth = request.data['DateOfBirth']
        model.Gender = request.data['Gender']
        model.Profession = request.data['Profession']
        model.CardCode = request.data['CardCode']
        model.U_BPID = request.data['U_BPID']
        model.U_BRANCHID = "1", #request.data['U_BRANCHID']
        model.U_NATIONALTY = request.data['U_NATIONALTY']
        model.CreateDate = request.data['CreateDate']
        model.CreateTime = request.data['CreateTime']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.save()
        return Response({"message":"successful","status":"200", "data":[request.data]})
    except Exception as e:
            return Response({"message":str(e),"status":"201","data":[]})

#BPEmployee delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=BPEmployee.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})
