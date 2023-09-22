from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes

# import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Order.models import Order
from Activity.serializers import ActivitySerializer
from .forms import *  
from .models import *  
from Activity.models import Activity
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

#added by millan on 03-10-2022
import os
from django.core.files.storage import FileSystemStorage

from datetime import date       #added by millan on 14-10-2022
#added by millan on 03-10-2022

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

        U_LEADID = request.data['U_LEADID']
        U_LEADNM = request.data['U_LEADNM']
        
        model = BusinessPartner(CardName = CardName, Industry = Industry, CardType = CardType, Website = Website, EmailAddress = EmailAddress, Phone1 = Phone1, DiscountPercent = DiscountPercent, Currency = Currency, IntrestRatePercent = IntrestRatePercent, CommissionPercent = CommissionPercent, Notes = Notes, PayTermsGrpCode = PayTermsGrpCode, CreditLimit = CreditLimit, AttachmentEntry = AttachmentEntry, SalesPersonCode = SalesPersonCode, ContactPerson = request.data['ContactEmployees'][0]['Name'], U_PARENTACC = U_PARENTACC, U_BPGRP = U_BPGRP, U_CONTOWNR = U_CONTOWNR, U_RATING = U_RATING, U_TYPE = U_TYPE, U_ANLRVN = U_ANLRVN, U_CURBAL = U_CURBAL, U_ACCNT = U_ACCNT, U_INVNO = U_INVNO, U_LAT = U_LAT, U_LONG = U_LONG, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, U_LEADID = U_LEADID, U_LEADNM = U_LEADNM)
        
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
    # allbp = [];
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    result = showBP(businesspartners_obj)
    return Response({"message": "Success","status": 200,"data":result})

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
    # onebp = [];
    try:
        CardCode=request.data['CardCode']
        if CardCode != "":
            businesspartners_obj = BusinessPartner.objects.filter(CardCode = CardCode)
            result = showBP(businesspartners_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Error","status": 201,"data":'Please Select CardCode'})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})

#BusinessPartner Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        # added by millan for check existing business partner name exclude(pk=self.instance.pk).get(username=username)
        if BusinessPartner.objects.exclude(pk=fetchid).filter(CardName=request.data['CardName']).exists():
            return Response({"message":"CardName Already Exists","status":"409","data":[]})
        # added by millan for check existing business partner name
        else:
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
            # model.ContactPerson = request.data['ContactEmployees'][0]['FirstName']
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
            # model.U_LEADID = request.data['U_LEADID']
            # model.U_LEADNM = request.data['U_LEADNM']

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
            # bpemp.FirstName = request.data['ContactEmployees'][0]['FirstName']
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

            # return Response({"message":"successful","status":200, "data":[request.data]})
            return Response({"message":"successful","status":200, "data":[]})
    
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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BP Type >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# create BP type
@api_view(['POST'])
def createtype(request):
    try:
        Type = request.data['Type']
        oppTypeObj = BPType(Type = Type).save()
        oppTypeId = BPType.objects.latest('id')

        return Response({"message":"successful","status":200, "data":[{"TypeId": oppTypeId.id}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error":str(e)}]})

# create BP type
@api_view(['GET'])
def alltype(request):
    try:
        oppTypeObj = BPType.objects.all().order_by('-Type')
        oppTypeJson = BPTypeSerializer(oppTypeObj, many=True)
        return Response({"message":"successful","status":200, "data":oppTypeJson.data})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error":str(e)}]})

# to get object of business_partner salesPersonCode, PaymentTerms and Business Type
def showBP(objs):
    allbp = [];
    for obj in objs:
        # print(obj.U_TYPE)
        bpType = obj.U_TYPE
        cardCodeType=obj.CardCode
        paymentType = obj.PayTermsGrpCode
        salesPersonType = obj.SalesPersonCode
        bpjson = BusinessPartnerSerializer(obj)
        finalBpData = json.loads(json.dumps(bpjson.data))
            
        if bpType != "":
            bpTypeObj = BPType.objects.filter(pk = bpType)
            bpTypejson = BPTypeSerializer(bpTypeObj, many = True)
            finalBpData['U_TYPE']=json.loads(json.dumps(bpTypejson.data))
        else:
            finalBpData['U_TYPE'] = []
            
        if paymentType != "":
            paymentTypeObj = PaymentTermsTypes.objects.filter(pk = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalBpData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalBpData['PayTermsGrpCode'] = []
            
        if salesPersonType != "":
            salesPersonObj = Employee.objects.filter(pk = salesPersonType).values("id","SalesEmployeeName", "SalesEmployeeCode")
            salesjson = EmployeeSerializer(salesPersonObj, many =True)
            finalBpData['SalesPersonCode'] = json.loads(json.dumps(salesjson.data))
        else:
            finalBpData['SalesPersonCode'] = []
            
        if cardCodeType != "":
            cardObj = BPEmployee.objects.filter(CardCode = cardCodeType).values("id","FirstName", "CardCode", "InternalCode", "MobilePhone", "E_Mail")
            cardjson = BPEmployeeSerializer(cardObj, many = True)
            finalBpData['ContactEmployees'] = json.loads(json.dumps(cardjson.data))
        else:
            finalBpData['ContactEmployees'] = []
            
        if cardCodeType != "":
            bpaddr = BPAddresses.objects.filter(BPCode=cardCodeType)
            bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
            jss0 = json.loads(json.dumps(bpaddr_json.data))
            
            bpbr = BPBranch.objects.filter(BPCode=cardCodeType)
            bpbr_json = BPBranchSerializer(bpbr, many=True)
            jss1 = json.loads(json.dumps(bpbr_json.data))
            finalBpData['BPAddresses'] = jss0 + jss1
        else:
            finalBpData['BPAddresses'] = []
        
        allbp.append(finalBpData)
    return allbp

#added by millan on 08-September-2022
#bp selected fields api
@api_view(["GET"])
def get_bp(request):
    try: 
        businesspartners_obj = BusinessPartner.objects.all().values("CardName", "EmailAddress", "Phone1", "id")
        bp_obj = BusinessPartnerSerializer(businesspartners_obj, many=True)
        finalBP = json.loads(json.dumps(bp_obj.data))
        return Response({"message": "Success","status": 200,"data":finalBP})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})
    
#added by millan on 03-October-2022 for adding attachment and description
@api_view(["POST"])
def bp_attachment_create(request):
    try:
        cust_id = request.data['cust_id']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        print(request.FILES)
        print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/BPAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, CustId=cust_id, CreateDate=CreateDate, CreateTime=CreateTime, Size=Size)
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#for updating attachment
@api_view(['POST'])
def bp_attachment_update(request):
    try:
        cust_id = request.data['cust_id']
        fetchid = request.data['id']
        
        File = request.data['Attach']
        
        model = Attachment.objects.get(pk = fetchid, CustId=cust_id)
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        attechmentsImage_url = ""
        if File:
            target ='./bridge/static/image/BPAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
            print(attechmentsImage_url)
            model.File = attechmentsImage_url
            model.Size = Size
        else:
            model.File= model.File
            print('no image')
        
        model.save()
        
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"status":"201","message":"error","data":[str(e)]})

#for deleting an attachment
@api_view(['POST'])
def bp_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        cust_id = request.data['cust_id']
        
        if Attachment.objects.filter(pk=fetchid, CustId=cust_id).exists():
            
            Attachment.objects.filter(pk=fetchid, CustId=cust_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#get all attachment based on customer_id
@api_view(["POST"])
def bp_attachments(request):
    try:
        cust_id=request.data['cust_id']
        if cust_id > 0:
            bpAttachObj = Attachment.objects.filter(CustId = cust_id)
            
            bpAttachjson = BPAttachmentSerilaizer(bpAttachObj, many = True)
            
            return Response({"message": "Success","status": 200,"data":bpAttachjson.data})
        else:
            return Response({"message": "Customer ID Not Found","status": 201,"data":[]})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 06-10-2022 to get sales of each particular month based on card code
@api_view(["POST"])
def monthlySales(request):
    try:
        CardCode = request.data['CardCode']
        monSales = []
        if Order.objects.filter(CardCode = CardCode).exists:
            sql_query = f"SELECT id, SUM(DocTotal) MonthlyTotal, CreateDate, SUBSTR(CreateDate,1,7) as mon FROM `order_order` where CardCode ='{CardCode}' GROUP BY mon"
            monsl = Order.objects.raw(sql_query)
            for desc in monsl:
                crDate = desc.mon.split('-')
                monSales.append({"MonthlySales":desc.MonthlyTotal, "Year":crDate[0], "Month":crDate[1]})
        
            return Response({"message": "success","status": 200,"data":monSales})
        else:
            return Response({"message": "Card Code Not Found","status": 201,"data":[]})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 14-10-2022 to get sales of each particular month based on card code
@api_view(["POST"])
def top5Activity(request):
    try:
        Emp = request.data['Emp']
        todays_date = date.today()
        cur_day = todays_date.day
        fif_day = cur_day + 5
        top5Act = []
        if Activity.objects.filter(Emp = Emp).exists():
            sql_query = f"SELECT * FROM `Activity_activity` where Emp = {Emp} and (SUBSTR(CreateDate,9,10)) BETWEEN {cur_day} AND {fif_day} LIMIT 5"
            top5sl = Activity.objects.raw(sql_query)
            top5Act = ActivitySerializer(top5sl,many=True)
                
        return Response({"message": "Success","status": 200,"data":top5Act.data})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})


