from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

#Item Create API
@api_view(['POST'])
def create(request):

    if request.data['CodeType']=='Manual':
        if Item.objects.filter(ItemCode=request.data['ItemCode']).exists():
            return Response({"message":"Already exist ItemCode","status":"409","data":[]})
        elif request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
            return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
        else:
            try:        
                CodeType = request.data['CodeType']
                ItemName = request.data['ItemName']
                ItemCode = request.data['ItemCode']
                CatID = request.data['CatID']
                Inventory = request.data['Inventory']
                Description = request.data['Description']
                UnitPrice = request.data['UnitPrice']
                UoS = request.data['UoS']
                Packing = request.data['Packing']
                Currency = request.data['Currency']
                HSN = request.data['HSN']
                TaxCode = request.data['TaxCode']
                Discount = request.data['Discount']
                Status = request.data['Status']
                CreatedDate = request.data['CreatedDate']
                CreatedTime = request.data['CreatedTime']
                UpdatedDate = request.data['UpdatedDate']
                UpdatedTime = request.data['UpdatedTime']
                
                CatID = Category.objects.get(pk=CatID)

                model = Item(CodeType = CodeType, ItemName = ItemName, ItemCode = ItemCode, CatID = CatID, Inventory=Inventory, Description = Description, UnitPrice = UnitPrice, UoS = UoS, Packing=Packing, Currency = Currency, HSN = HSN, TaxCode = TaxCode, Discount = Discount, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate = UpdatedDate, UpdatedTime = UpdatedTime)
                model.save()
                prod = Item.objects.latest('id')        
                return Response({"message":"successful","status":200,"data":[{"id":prod.id}]})
            except Exception as e:
                return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})
    
    elif request.data['CodeType']=='Series':
        if request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
            return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
        else:
            try:
                CodeType = request.data['CodeType']
                ItemName = request.data['ItemName']
                #ItemCode = request.data['ItemCode']
                CatID = request.data['CatID']
                Inventory = request.data['Inventory']
                Description = request.data['Description']
                UnitPrice = request.data['UnitPrice']
                UoS = request.data['UoS']
                Packing = request.data['Packing']
                Currency = request.data['Currency']
                HSN = request.data['HSN']
                TaxCode = request.data['TaxCode']
                Discount = request.data['Discount']
                Status = request.data['Status']
                CreatedDate = request.data['CreatedDate']
                CreatedTime = request.data['CreatedTime']
                UpdatedDate = request.data['UpdatedDate']
                UpdatedTime = request.data['UpdatedTime']
                
                CatID = Category.objects.get(pk=CatID)

                model = Item(CodeType = CodeType, ItemName = ItemName, CatID = CatID, Inventory=Inventory, Description = Description, UnitPrice = UnitPrice, UoS = UoS, Packing=Packing, Currency = Currency, HSN = HSN, TaxCode = TaxCode, Discount = Discount, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate = UpdatedDate, UpdatedTime = UpdatedTime)
                model.save()
                prod = Item.objects.latest('id')        
                pid = format(prod.id, '06')                
                model.ItemCode = "IT"+str(pid)
                model.save()
                
                return Response({"message":"successful","status":200,"data":[{"id":prod.id}]})
            except Exception as e:
                return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Item Create API R&D
@api_view(['POST'])
def create_test(request):
    try:
        model = makemodel(request)
        print("Item("+str(model)+")")
        ss = "Item("+str(model)+")"
        model = Item(ss)
        print(model)
        model.save()
        
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Item Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    if request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
        return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
    else:
        try:
            model = Item.objects.get(pk = fetchid)
            model.ItemName = request.data['ItemName']
            CatID = Category.objects.get(pk=request.data['CatID'])
            model.CatID = CatID
            model.Inventory = request.data['Inventory']
            model.Description = request.data['Description']
            model.UnitPrice = request.data['UnitPrice']
            model.UoS = request.data['UoS']
            model.Packing = request.data['Packing']
            model.Currency = request.data['Currency']
            model.HSN = request.data['HSN']
            model.TaxCode = request.data['TaxCode']
            model.Discount = request.data['Discount']
            model.Status = request.data['Status']
            model.UpdatedDate = request.data['UpdatedDate']
            model.UpdatedTime = request.data['UpdatedTime']            
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Item All API
@api_view(["POST"])
def all(request):
    if "CatID" in request.data:
        Items_obj = Item.objects.filter(CatID=request.data['CatID']).order_by("-id")
        prod_json = ItemSerializer(Items_obj, many=True)
        return Response({"message": "Success","status": 200,"data":prod_json.data})
    else:
        Items_obj = Item.objects.all().order_by("-id")
        prod_json = ItemSerializer(Items_obj, many=True)
        return Response({"message": "Success","status": 200,"data":prod_json.data})


#Item One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    Items_obj = Item.objects.get(id=id)
    prod_json = ItemSerializer(Items_obj, many=False)
    return Response({"message": "Success","status": 200,"data":[prod_json.data]})

#Item delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Item.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

#Item Create API
@api_view(['POST'])
def tax_create(request):
    if request.data['TaxCode'] >= 1:
        return Response({"message":"TaxCode should be less than 1", "status":"201","data":[]})
    elif Tax.objects.filter(TaxCode=request.data['TaxCode']).exists():
        return Response({"message":"Already exist TaxCode","status":"409","data":[]})
    elif Tax.objects.filter(TaxName=request.data['TaxName']).exists():
        return Response({"message":"Already exist TaxName","status":"409","data":[]})
    else:
        try:        
            TaxName = request.data['TaxName']
            TaxCode = request.data['TaxCode']
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']

            model = Tax(TaxName = TaxName, TaxCode = TaxCode, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
            model.save()
            tax = Tax.objects.latest('id')        
            return Response({"message":"successful","status":200,"data":[{"id":tax.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Tax All API
@api_view(["GET"])
def tax_all(request):
    tax_obj = Tax.objects.all().order_by("-id")
    tax_json = TaxSerializer(tax_obj, many=True)
    return Response({"message": "Success","status": 200,"data":tax_json.data})

#Tax Update API
@api_view(['POST'])
def tax_update(request):
    fetchid = request.data['id']
    if request.data['TaxCode'] >= 1:
        return Response({"message":"TaxCode should be less than 1", "status":"201","data":[]})
    else:
        try:
            model = Tax.objects.get(pk = fetchid)
            model.TaxName = request.data['TaxName']
            model.TaxCode = request.data['TaxCode']
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Tax One API
@api_view(["POST"])
def tax_one(request):
    id=request.data['id']    
    tax_obj = Tax.objects.get(id=id)
    tax_json = TaxSerializer(tax_obj, many=False)
    return Response({"message": "Success","status": 200,"data":[tax_json.data]})


#Category Create API
@api_view(['POST'])
def category_create(request):
    if Category.objects.filter(CategoryName=request.data['CategoryName']).exists():
        return Response({"message":"Already exist CategoryName","status":"409","data":[]})
    else:
        try:        
            CategoryName = request.data['CategoryName']
            Status = request.data['Status']
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            UpdatedDate = request.data['UpdatedDate']
            UpdatedTime = request.data['UpdatedTime']

            model = Category(CategoryName = CategoryName, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate=CreatedDate, UpdatedTime=CreatedTime)
            model.save()
            category = Category.objects.latest('id')        
            return Response({"message":"successful","status":200,"data":[{"id":category.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Category All API
@api_view(["GET"])
def category_all(request):
    category_obj = Category.objects.all().order_by("-id")
    category_json = CategorySerializer(category_obj, many=True)
    return Response({"message": "Success","status": 200,"data":category_json.data})

#Category Update API
@api_view(['POST'])
def category_update(request):
    fetchid = request.data['id']
    if Category.objects.filter(CategoryName=request.data['CategoryName']).exists():
        return Response({"message":"Already exist CategoryName","status":"409","data":[]})
    else:
        try:
            model = Category.objects.get(pk = fetchid)
            model.CategoryName = request.data['CategoryName']
            model.Status = request.data['Status']
            model.UpdatedDate = request.data['UpdatedDate']
            model.UpdatedTime = request.data['UpdatedTime']
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Category One API
@api_view(["POST"])
def category_one(request):
    id=request.data['id']    
    category_obj = Category.objects.get(id=id)
    category_json = CategorySerializer(category_obj, many=False)
    return Response({"message": "Success","status": 200,"data":[category_json.data]})

