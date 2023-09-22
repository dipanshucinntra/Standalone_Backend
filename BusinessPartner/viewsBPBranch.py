from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import BPBranch  
from .models import BPBranch  
import requests, json
from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPBranchSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  


#BPBranch Create API
@api_view(['POST'])
def create(request):
    try:
        BPID = request.data['BPID']
        BPCode = request.data['BPCode']
        BranchName = request.data['BranchName']
        AddressName = request.data['AddressName']
        AddressName2 = request.data['AddressName2']
        AddressName3 = request.data['AddressName3']
        BuildingFloorRoom = request.data['BuildingFloorRoom']
        Street = request.data['Street']
        Block = request.data['Block']
        County = request.data['County']
        City = request.data['City']
        State = request.data['State']
        ZipCode = request.data['ZipCode']
        Country = request.data['Country']
        #AddressType = request.data['AddressType']
        AddressType = 'bo_ShipTo'
        TaxOffice = request.data['TaxOffice']
        GSTIN = request.data['GSTIN']
        GstType = request.data['GstType']
        ShippingType = request.data['ShippingType']
        PaymentTerm = request.data['PaymentTerm']
        CurrentBalance = request.data['CurrentBalance']
        CreditLimit = request.data['CreditLimit']
        Phone = request.data['Phone']
        Fax = request.data['Fax']
        Email = request.data['Email']
        Lat = request.data['Lat']
        Long = request.data['Long']
        U_COUNTRY = request.data['U_COUNTRY']
        U_STATE = request.data['U_STATE']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        
        model = BPBranch(BPID=BPID, BPCode=BPCode, BranchName=BranchName, AddressName=AddressName, AddressName2=AddressName2, AddressName3=AddressName3, BuildingFloorRoom=BuildingFloorRoom, Street=Street, Block=Block, County=County, City=City, State=State, ZipCode=ZipCode, Country=Country, AddressType=AddressType, TaxOffice=TaxOffice, GSTIN=GSTIN, GstType=GstType, ShippingType=ShippingType, PaymentTerm=PaymentTerm, CurrentBalance=CurrentBalance, CreditLimit=CreditLimit, Phone=Phone, Fax=Fax, Email=Email, Lat=Lat, Long=Long, U_COUNTRY=U_COUNTRY, U_STATE=U_STATE, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        RN = BPBranch.objects.filter(BPCode=BPCode).count()
        model.RowNum = RN - 1
        model.save()

        return Response({"message":"successful","status":200, "data":[{"id":model.id,"RowNum":model.RowNum}]})
    except Exception as e:
        #print(e)
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

    
#BPBranch All API
@api_view(["POST"])
def all(request):    
    BPCode=request.data['BPCode']
    bpbranch_obj = BPBranch.objects.filter(BPCode=BPCode, Status=1) 
    bpbranch_json = BPBranchSerializer(bpbranch_obj, many=True)
    return Response({"message": "Success","status": 200,"data":bpbranch_json.data})


#BPBranch One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    
    try:
        bpbranch_obj = BPBranch.objects.get(id=id, Status=1) 
        bpbranch_json = BPBranchSerializer(bpbranch_obj)
        return Response({"message": "Success","status": 200,"data":[bpbranch_json.data]})
    except:
        return Response({"message": "Wrong ID","status": 201,"data":[]})

#BPBranch Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = BPBranch.objects.get(pk = fetchid)
        
        model.BPCode = request.data['BPCode']
        model.BranchName = request.data['BranchName']
        model.AddressName = request.data['AddressName']
        model.AddressName2 = request.data['AddressName2']
        model.AddressName3 = request.data['AddressName3']
        model.BuildingFloorRoom = request.data['BuildingFloorRoom']
        model.Street = request.data['Street']
        model.Block = request.data['Block']
        model.County = request.data['County']
        model.City = request.data['City']
        model.State = request.data['State']
        model.ZipCode = request.data['ZipCode']
        model.Country = request.data['Country']
        model.AddressType = request.data['AddressType']
        model.TaxOffice = request.data['TaxOffice']
        model.GSTIN = request.data['GSTIN']
        model.GstType = request.data['GstType']
        model.ShippingType = request.data['ShippingType']
        model.PaymentTerm = request.data['PaymentTerm']
        model.CurrentBalance = request.data['CurrentBalance']
        model.CreditLimit = request.data['CreditLimit']
        model.Phone = request.data['Phone']
        model.Fax = request.data['Fax']
        model.Email = request.data['Email']
        model.Lat = request.data['Lat']
        model.Long = request.data['Long']
        model.U_COUNTRY = request.data['U_COUNTRY']
        model.U_STATE = request.data['U_STATE']
        model.CreateDate = request.data['CreateDate']
        model.CreateTime = request.data['CreateTime']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.save()
        return Response({"message":"successful","status":200, "data":[request.data]})

    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#BPBranch delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:   
        br = BPBranch.objects.get(pk=fetchid)
        br.Status=0
        br.save()
        
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

