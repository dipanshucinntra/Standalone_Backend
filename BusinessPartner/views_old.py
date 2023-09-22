from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import *  
from .models import *  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#BusinessPartner Create API
@api_view(['POST'])
def create(request):

    if BusinessPartner.objects.filter(CardName=request.data['CardName']).exists():
        return Response({"message":"Already exist Card Name","status":"409","data":[]})
    else:    
        CardName = request.data['CardName']
        Industry = request.data['Industry']
        CardType = request.data['CardType']
        Website = request.data['Website']
        EmailAddress = request.data['EmailAddress']
        Phone1 = request.data['Phone1']
        DiscountPercent = request.data['DiscountPercent']
        Currency = request.data['Currency']
        IntrestRatePercent = request.data['IntrestRatePercent']
        CommissionPercent = request.data['CommissionPercent']
        Notes = request.data['Notes']
        PayTermsGrpCode = request.data['PayTermsGrpCode']
        CreditLimit = request.data['CreditLimit']
        AttachmentEntry = request.data['AttachmentEntry']
        SalesPersonCode = request.data['SalesPersonCode']
        ContactPerson = request.data['ContactEmployees'][0]['Name']
        U_PARENTACC = request.data['U_PARENTACC']
        U_BPGRP = request.data['U_BPGRP']
        U_CONTOWNR = request.data['U_CONTOWNR']
        U_RATING = request.data['U_RATING']
        U_TYPE = request.data['U_TYPE']
        U_ANLRVN = request.data['U_ANLRVN']
        U_CURBAL = request.data['U_CURBAL']
        U_ACCNT = request.data['U_ACCNT']
        U_INVNO = request.data['U_INVNO']
        
        U_LAT = request.data['U_LAT']
        U_LONG = request.data['U_LONG']
        
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        
        model = BusinessPartner(CardName = CardName, Industry = Industry, CardType = CardType, Website = Website, EmailAddress = EmailAddress, Phone1 = Phone1, DiscountPercent = DiscountPercent, Currency = Currency, IntrestRatePercent = IntrestRatePercent, CommissionPercent = CommissionPercent, Notes = Notes, PayTermsGrpCode = PayTermsGrpCode, CreditLimit = CreditLimit, AttachmentEntry = AttachmentEntry, SalesPersonCode = SalesPersonCode, ContactPerson = request.data['ContactEmployees'][0]['Name'], U_PARENTACC = U_PARENTACC, U_BPGRP = U_BPGRP, U_CONTOWNR = U_CONTOWNR, U_RATING = U_RATING, U_TYPE = U_TYPE, U_ANLRVN = U_ANLRVN, U_CURBAL = U_CURBAL, U_ACCNT = U_ACCNT, U_INVNO = U_INVNO, U_LAT = U_LAT, U_LONG = U_LONG, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
        
        model.save()
        bp = BusinessPartner.objects.latest('id')
        CardCode = "C"+str(bp.id)
        bp.CardCode = CardCode
        bp.save()

        bpemp = BPEmployee(U_BPID=bp.id, CardCode=CardCode, U_BRANCHID=1, MobilePhone=request.data['ContactEmployees'][0]['MobilePhone'], FirstName=request.data['ContactEmployees'][0]['Name'], E_Mail=request.data['ContactEmployees'][0]['E_Mail'], CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        bpemp.save()
        em = BPEmployee.objects.latest('id')
        bpemp.InternalCode = em.id
        bpemp.save()

        
        if request.data['BPAddresses'][0]['AddressType']=='bo_BillTo' :
            bpadd = request.data['BPAddresses'][0]
            print(request.data['BPAddresses'][0]['AddressType'])
            model_add = BPAddresses(BPID=bp.id, AddressName = bpadd['AddressName'], Street = bpadd['Street'], Block = bpadd['Block'], ZipCode = bpadd['ZipCode'], City = bpadd['City'], Country = bpadd['Country'], AddressType = bpadd['AddressType'], RowNum=0, BPCode = CardCode, U_STATE = bpadd['U_STATE'], State = bpadd['State'], U_COUNTRY = bpadd['U_COUNTRY'], U_SHPTYP = bpadd['U_SHPTYP'])
            model_add.save()
        
        if request.data['BPAddresses'][1]['AddressType']=='bo_ShipTo' :
            bpadd1 = request.data['BPAddresses'][1]
            print(request.data['BPAddresses'][1]['AddressType'])
            model_br = BPBranch(BPID=bp.id, BranchName=CardName, AddressName = bpadd1['AddressName'], Street = bpadd1['Street'], Block = bpadd1['Block'], ZipCode = bpadd1['ZipCode'], City = bpadd1['City'], Country = bpadd1['Country'], AddressType = bpadd1['AddressType'], RowNum=1, BPCode = CardCode, U_STATE = bpadd1['U_STATE'], Default=1, State = bpadd1['State'], U_COUNTRY = bpadd1['U_COUNTRY'], U_SHPTYP = bpadd1['U_SHPTYP'], CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
            model_br.save()

    return Response({"message":"successful","status":"200","data":[]})

#BusinessPartner All API
@api_view(["GET"])
def all(request):
    allbp = [];
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        
        cont = BPEmployee.objects.filter(CardCode=bp.CardCode)
        cont_json = BPEmployeeSerializer(cont, many=True)
        cont_all = json.loads(json.dumps(cont_json.data))
        print(cont_all)        
        if len(cont) > 0:
           ContactPerson = cont[0].FirstName
           print(ContactPerson)
        else:
           ContactPerson = ""
           print(ContactPerson)
        
        bpaddr = BPAddresses.objects.filter(BPCode=bp.CardCode)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        
        jss0 = json.loads(json.dumps(bpaddr_json.data))
        
        bpbr = BPBranch.objects.filter(BPCode=bp.CardCode,Default=1)
        
        bpbr_json = BPBranchSerializer(bpbr, many=True)
        
        jss1 = json.loads(json.dumps(bpbr_json.data))
        
        context = {
            'id':bp.id,
            'CardCode':bp.CardCode,
            'CardName':bp.CardName,
            'Industry':bp.Industry,
            'CardType':bp.CardType,
            'Website':bp.Website,
            'EmailAddress':bp.EmailAddress,
            'Phone1':bp.Phone1,
            'DiscountPercent':bp.DiscountPercent,
            'Currency':bp.Currency,
            'IntrestRatePercent':bp.IntrestRatePercent,
            'CommissionPercent':bp.CommissionPercent,
            'Notes':bp.Notes,
            'PayTermsGrpCode':bp.PayTermsGrpCode,
            'CreditLimit':bp.CreditLimit,
            'AttachmentEntry':bp.AttachmentEntry,
            'SalesPersonCode':bp.SalesPersonCode,
            'ContactPerson':ContactPerson,
            'U_PARENTACC':bp.U_PARENTACC,
            'U_BPGRP':bp.U_BPGRP,
            'U_CONTOWNR':bp.U_CONTOWNR,
            'U_RATING':bp.U_RATING,
            'U_TYPE':bp.U_TYPE,
            'U_ANLRVN':bp.U_ANLRVN,
            'U_CURBAL':bp.U_CURBAL,
            'U_ACCNT':bp.U_ACCNT,
            'U_INVNO':bp.U_INVNO,
            'U_LAT':bp.U_LAT,
            'U_LONG':bp.U_LONG,
            'CreateDate':bp.CreateDate,
            'CreateTime':bp.CreateTime,
            'UpdateDate':bp.UpdateDate,
            'UpdateTime':bp.UpdateTime,
            'ContactEmployees': cont_all,
            'BPAddresses':jss0+jss1
            }
            
        allbp.append(context)
        
    return Response({"message": "Success","status": 200,"data":allbp})


#BusinessPartner All API
@api_view(["GET"])
def all_old(request):    
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        bpaddr = BPAddresses.objects.filter(BPID=bp.id)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        
        jss = json.loads(json.dumps(bpaddr_json.data))
        bp.U_BPADDRESS = jss
        
    businesspartner_json = BusinessPartnerSerializer(businesspartners_obj, many=True)
    return Response({"message": "Success","status": 200,"data":businesspartner_json.data})

#BusinessPartner All API
@api_view(["GET"])
def all_bp(request):    
    businesspartners_obj = BusinessPartner.objects.all()
    businesspartners_json = BPSerializer(businesspartners_obj, many=True)
    return Response({"message": "Success","status": 200,"data":businesspartners_json.data})

#BusinessPartner One API
@api_view(["POST"])
def one(request):

    CardCode=request.data['CardCode']
    bp = BusinessPartner.objects.get(CardCode=CardCode)
    
    cont = BPEmployee.objects.filter(CardCode=bp.CardCode)
    cont_json = BPEmployeeSerializer(cont, many=True)
    cont_all = json.loads(json.dumps(cont_json.data))
    print(cont_all)        
    if len(cont) > 0:
       ContactPerson = cont[0].FirstName
       print(ContactPerson)
    else:
       ContactPerson = ""
       print(ContactPerson)

    bpaddr = BPAddresses.objects.filter(BPID=bp.id)
    
    bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
    
    jss0 = json.loads(json.dumps(bpaddr_json.data))
    
    bpbr = BPBranch.objects.filter(BPCode=bp.CardCode,Default=1)
        
    bpbr_json = BPBranchSerializer(bpbr, many=True)
    
    jss1 = json.loads(json.dumps(bpbr_json.data))    
    
    context = {
        'id':bp.id,
        'CardCode':bp.CardCode,
        'CardName':bp.CardName,
        'Industry':bp.Industry,
        'CardType':bp.CardType,
        'Website':bp.Website,
        'EmailAddress':bp.EmailAddress,
        'Phone1':bp.Phone1,
        'DiscountPercent':bp.DiscountPercent,
        'Currency':bp.Currency,
        'IntrestRatePercent':bp.IntrestRatePercent,
        'CommissionPercent':bp.CommissionPercent,
        'Notes':bp.Notes,
        'PayTermsGrpCode':bp.PayTermsGrpCode,
        'CreditLimit':bp.CreditLimit,
        'AttachmentEntry':bp.AttachmentEntry,
        'SalesPersonCode':bp.SalesPersonCode,
        'ContactPerson':ContactPerson,
        'U_PARENTACC':bp.U_PARENTACC,
        'U_BPGRP':bp.U_BPGRP,
        'U_CONTOWNR':bp.U_CONTOWNR,
        'U_RATING':bp.U_RATING,
        'U_TYPE':bp.U_TYPE,
        'U_ANLRVN':bp.U_ANLRVN,
        'U_CURBAL':bp.U_CURBAL,
        'U_ACCNT':bp.U_ACCNT,
        'U_INVNO':bp.U_INVNO,
        'U_LAT':bp.U_LAT,
        'U_LONG':bp.U_LONG,
        'CreateDate':bp.CreateDate,
        'CreateTime':bp.CreateTime,
        'UpdateDate':bp.UpdateDate,
        'UpdateTime':bp.UpdateTime,
        'ContactEmployees': cont_all,
        'BPAddresses':jss0+jss1
        }
        
    return Response({"message": "Success","status": 200,"data":[context]})

#BusinessPartner Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = BusinessPartner.objects.get(pk = fetchid)

        model.CardName = request.data['CardName']
        model.Industry = request.data['Industry']
        model.CardType = request.data['CardType']
        model.Website = request.data['Website']
        model.EmailAddress = request.data['EmailAddress']
        model.Phone1 = request.data['Phone1']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Currency = request.data['Currency']
        model.IntrestRatePercent = request.data['IntrestRatePercent']
        model.CommissionPercent = request.data['CommissionPercent']
        model.Notes = request.data['Notes']
        model.PayTermsGrpCode = request.data['PayTermsGrpCode']
        model.CreditLimit = request.data['CreditLimit']
        model.AttachmentEntry = request.data['AttachmentEntry']
        model.SalesPersonCode = request.data['SalesPersonCode']
        model.ContactPerson = request.data['ContactEmployees'][0]['Name']
        model.U_PARENTACC = request.data['U_PARENTACC']
        model.U_BPGRP = request.data['U_BPGRP']
        model.U_CONTOWNR = request.data['U_CONTOWNR']
        model.U_RATING = request.data['U_RATING']
        model.U_TYPE = request.data['U_TYPE']
        model.U_ANLRVN = request.data['U_ANLRVN']
        model.U_CURBAL = request.data['U_CURBAL']
        model.U_ACCNT = request.data['U_ACCNT']
        model.U_INVNO = request.data['U_INVNO']
        
        model.U_LAT = request.data['U_LAT']
        model.U_LONG = request.data['U_LONG']
        
        model.CreateDate = request.data['CreateDate']
        model.CreateTime = request.data['CreateTime']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.save()
        
        model_add = BPAddresses.objects.get(BPID = model.id)
        
        model_add.AddressName = request.data['BPAddresses'][0]['AddressName']
        model_add.Street = request.data['BPAddresses'][0]['Street']
        model_add.Block = request.data['BPAddresses'][0]['Block']
        model_add.City = request.data['BPAddresses'][0]['City']
        model_add.State = request.data['BPAddresses'][0]['State']
        model_add.ZipCode = request.data['BPAddresses'][0]['ZipCode']
        model_add.Country = request.data['BPAddresses'][0]['Country']

        model_add.U_SHPTYP = request.data['BPAddresses'][0]['U_SHPTYP']
        model_add.U_COUNTRY = request.data['BPAddresses'][0]['U_COUNTRY']
        model_add.U_STATE = request.data['BPAddresses'][0]['U_STATE']
        model_add.save()
        
        bpemp = BPEmployee.objects.get(InternalCode = request.data['ContactEmployees'][0]['InternalCode'])
        print(bpemp)
        bpemp.MobilePhone = request.data['ContactEmployees'][0]['MobilePhone']
        bpemp.FirstName = request.data['ContactEmployees'][0]['Name']
        bpemp.E_Mail = request.data['ContactEmployees'][0]['E_Mail']
        bpemp.UpdateDate = request.data['UpdateDate']
        bpemp.UpdateTime = request.data['UpdateTime']
        
        bpemp.save()        
        
        print(bpemp)
        #return;        
        
        model_br = BPBranch.objects.get(BPCode = model.CardCode, Default=1)
        model_br.Default=0
        model_br.save()
        
        model_br = BPBranch.objects.get(pk = request.data['BPAddresses'][1]['id'])
        model_br.Default=1
        model_br.save()

        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        #print(e)
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})


#BusinessPartner delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        bp=BusinessPartner.objects.get(pk=fetchid)
        CardCode = bp.CardCode

        fetchdata=BusinessPartner.objects.filter(pk=fetchid).delete()
            
        addr=BPAddresses.objects.filter(BPID=fetchid).delete()

        bpem=BPEmployee.objects.filter(U_BPID=fetchid).delete()
        
        bpbr=BPBranch.objects.filter(BPID=fetchid).delete()

        return Response({"message":"successful","status":"200","data":[]})
        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

