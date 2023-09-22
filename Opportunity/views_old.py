from django.shortcuts import render, redirect  
from django.db.models import Max
from django.http import JsonResponse, HttpResponse
from .forms import *  
from .models import *
from Employee.models import Employee
import requests, json
import os
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Opportunity All API
@api_view(["GET"])
def all(request):
    
    opps_obj = Opportunity.objects.all().order_by("-id")
    opps_json = OpportunitySerializer(opps_obj, many=True)
    return Response({"message": "Success","status": 200,"data":opps_json.data})

#Opportunity All API
@api_view(["GET"])
def all_opp(request):
    opps_obj = Opportunity.objects.all().order_by("-id")
    opps_json = OppSerializer(opps_obj, many=True)
    return Response({"message": "Success","status": 200,"data":opps_json.data})


#Opportunity All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "SalesPerson" in json_data:
        print("yes")
        
        if json_data['SalesPerson']!="":
            SalesPersonID = json_data['SalesPerson']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
                
            elif emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
            else:
                SalesPersonID = json_data['SalesPerson']
            
            print(SalesPersonID)
            
            for ke in json_data.keys():
                if ke =='U_FAV' :
                    print("yes filter")
                    if json_data['U_FAV'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            opps_json = OpportunitySerializer(opps_obj, many=True)
                            return Response({"message": "Success","status": 200,"data":opps_json.data})
                elif ke =='U_TYPE' :
                    if json_data['U_TYPE'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, U_TYPE=json_data['U_TYPE']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            opps_json = OpportunitySerializer(opps_obj, many=True)
                            return Response({"message": "Success","status": 200,"data":opps_json.data})
                elif ke =='Status' :
                    if json_data['Status'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, Status=json_data['Status']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            opps_json = OpportunitySerializer(opps_obj, many=True)
                            return Response({"message": "Success","status": 200,"data":opps_json.data})
                
                else:
                    print("no filter")
                    opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID).order_by("-id")
                    opps_json = OpportunitySerializer(opps_obj, many=True)
                    return Response({"message": "Success","status": 200,"data":opps_json.data})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})

"""
{
 "U_FAV":"",
 "U_TYPE":"Existing Business", 
 "Status":""
}
"""            

#Opportunity One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    opp_obj = Opportunity.objects.get(pk=id)
    opp_json = OpportunitySerializer(opp_obj)
    return Response({"message": "Success","status": 200,"data":[opp_json.data]})

#Opportunity Create API
@api_view(['POST'])
def create(request):
    CardCode = request.data['CardCode']
    SalesPerson = request.data['SalesPerson']
    SalesPersonName = request.data['SalesPersonName']
    ContactPerson = request.data['ContactPerson']
    ContactPersonName = request.data['ContactPersonName']
    Source = request.data['Source']
    StartDate = request.data['StartDate']
    PredictedClosingDate = request.data['PredictedClosingDate']
    MaxLocalTotal = request.data['MaxLocalTotal']
    MaxSystemTotal = request.data['MaxSystemTotal']
    Remarks = request.data['Remarks']
    
    Status = request.data['Status']
    ReasonForClosing = request.data['ReasonForClosing']
    TotalAmountLocal = request.data['TotalAmountLocal']
    TotalAmounSystem = request.data['TotalAmounSystem']
    
    stg = StaticStage.objects.all().order_by("SequenceNo")[:1]
    
    cur = stg[0].SequenceNo
    cur_num = stg[0].Stageno
    cur_name = stg[0].Name

    CurrentStageNo = cur
    CurrentStageNumber = cur_num
    CurrentStageName = cur_name
    
    OpportunityName = request.data['OpportunityName']
    Industry = request.data['Industry']
    LinkedDocumentType = request.data['LinkedDocumentType']
    DataOwnershipfield = request.data['DataOwnershipfield']
    DataOwnershipName = request.data['DataOwnershipName']
    StatusRemarks = request.data['StatusRemarks']
    ProjectCode = request.data['ProjectCode']
    CustomerName = request.data['CustomerName']
    ClosingDate = request.data['ClosingDate']
    ClosingType = request.data['ClosingType']
    OpportunityType = request.data['OpportunityType']
    UpdateDate = request.data['UpdateDate']
    UpdateTime = request.data['UpdateTime']
    U_TYPE = request.data['U_TYPE']
    U_LSOURCE = request.data['U_LSOURCE']
    U_FAV = request.data['U_FAV']
    U_PROBLTY = request.data['U_PROBLTY']
    
    model = Opportunity(CardCode=CardCode, SalesPerson=SalesPerson, SalesPersonName=SalesPersonName, ContactPerson=ContactPerson, ContactPersonName=ContactPersonName, Source=Source, StartDate=StartDate, PredictedClosingDate=PredictedClosingDate, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Status=Status, ReasonForClosing=ReasonForClosing, TotalAmountLocal=TotalAmountLocal, TotalAmounSystem=TotalAmounSystem, CurrentStageNo=CurrentStageNo, CurrentStageNumber=CurrentStageNumber, CurrentStageName=CurrentStageName, OpportunityName=OpportunityName, Industry=Industry, LinkedDocumentType=LinkedDocumentType, DataOwnershipfield=DataOwnershipfield, DataOwnershipName=DataOwnershipName, StatusRemarks=StatusRemarks, ProjectCode=ProjectCode, CustomerName=CustomerName, ClosingDate=ClosingDate, ClosingType=ClosingType, OpportunityType=OpportunityType, UpdateDate=UpdateDate, UpdateTime=UpdateTime, U_TYPE=U_TYPE, U_LSOURCE=U_LSOURCE, U_FAV=U_FAV, U_PROBLTY=U_PROBLTY)

    model.save()
    
    Opp = Opportunity.objects.latest('id')
    print(Opp.id)
    
    LineNum = "0"
    SalesPerson = request.data['SalesOpportunitiesLines'][0]['SalesPerson']
    ContactPerson = request.data['ContactPerson']
    StartDate = request.data['StartDate']
    MaxLocalTotal = request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal']
    MaxSystemTotal = request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal']
    Remarks = request.data['Remarks']
    Contact="tNO"
    Status = "so_Open"
    StageKey = cur
    ClosingDate = request.data['ClosingDate']
    #SequenceNo = request.data['SequentialNo']
    Opp_Id = Opp.id
    
    model_line = Line(LineNum=LineNum, SalesPerson=SalesPerson, StartDate=StartDate, StageKey=StageKey, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Contact=Contact, Status=Status, ContactPerson=ContactPerson, ClosingDate=ClosingDate,Opp_Id=Opp_Id)    
    
    model_line.save()    
    
    # add all static stages with this Opp
    staticstage = StaticStage.objects.all().order_by("Stageno")
    for ststage in staticstage:
        SequenceNo = ststage.SequenceNo
        Name = ststage.Name
        Stageno = ststage.Stageno
        ClosingPercentage = ststage.ClosingPercentage
        Cancelled = ststage.Cancelled
        IsSales = ststage.IsSales
        IsPurchasing = ststage.IsPurchasing
        Opp_Id = Opp_Id
        CreateDate = StartDate
        UpdateDate = StartDate
        if(ststage.Stageno == 1):
            Status = 1
        else:
            Status = 0
        model = Stage(SequenceNo=SequenceNo, Name=Name, Stageno=Stageno, ClosingPercentage=ClosingPercentage, Cancelled=Cancelled, IsSales=IsSales, IsPurchasing=IsPurchasing, Opp_Id=Opp_Id, Status=Status, CreateDate=CreateDate, UpdateDate=UpdateDate)
        model.save()
        
    with open("../bridge/bridge/db.json") as f:
        db = f.read()
        print(db)
    data = json.loads(db)
    
    r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)
    
    opp_data = {
      "CardCode": request.data['CardCode'],
      "PredictedClosingDate": request.data['PredictedClosingDate'],
      "ContactPerson": request.data['ContactPerson'],
      "DataOwnershipfield": request.data['DataOwnershipfield'],
      "MaxLocalTotal": request.data['MaxLocalTotal'],
      "MaxSystemTotal": request.data['MaxSystemTotal'],
      "CurrentStageNumber":cur_num,
      "Remarks": request.data['Remarks'],
      "SalesOpportunitiesLines": [
        {
          "DocumentType": "bodt_MinusOne",
          "MaxLocalTotal": request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal'],
          "MaxSystemTotal": request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal'],
          "SalesPerson": request.data['SalesOpportunitiesLines'][0]['SalesPerson'],
          "StageKey": cur
        }
      ],
      "SalesPerson": request.data['SalesPerson'],
      "StartDate": request.data['StartDate'],
      "U_TYPE": request.data['U_TYPE'],
      "OpportunityName": request.data['OpportunityName']
    }
    #print(opp_data)
    
    res = requests.post('http://103.107.67.94:50001/b1s/v1/SalesOpportunities', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
    #print(res.text);
    live = json.loads(res.text)
    
    if "SequentialNo" in live:
        print(live['SequentialNo'])
        
        fetchid = Opp.id
        model = Opportunity.objects.get(pk = fetchid)
        model.SequentialNo = live['SequentialNo']
        model.save()
        
        model = Line.objects.get(LineNum = 0, Opp_Id=Opp.id)
        model.SequenceNo = live['SequentialNo']
        model.save()
        
        return Response({"message":"successful","status":200,"data":[{"Opp_Id":Opp.id, "SequentialNo":live['SequentialNo']}]})
    else:
        print(live['error']['message']['value'])
        SAP_MSG = live['error']['message']['value']
        return Response({"message":"Partely successful","SAP_error":SAP_MSG, "status":202,"data":[]})

#Opportunity Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Opportunity.objects.get(pk = fetchid)
        
        model.SequentialNo = request.data['SequentialNo']
        model.CardCode = request.data['CardCode']
        model.SalesPerson = request.data['SalesPerson']
        model.SalesPersonName = request.data['SalesPersonName']
        model.ContactPerson = request.data['ContactPerson']
        model.ContactPersonName = request.data['ContactPersonName']
        model.Source = request.data['Source']
        model.StartDate = request.data['StartDate']
        model.PredictedClosingDate = request.data['PredictedClosingDate']
        model.MaxLocalTotal = request.data['MaxLocalTotal']
        model.MaxSystemTotal = request.data['MaxSystemTotal']
        model.Remarks = request.data['Remarks']
        model.Status = request.data['Status']
        model.ReasonForClosing = request.data['ReasonForClosing']
        model.TotalAmountLocal = request.data['TotalAmountLocal']
        model.TotalAmounSystem = request.data['TotalAmounSystem']
        #model.CurrentStageNo = request.data['CurrentStageNo']
        model.CurrentStageNo = model.CurrentStageNo
        model.CurrentStageNumber = model.CurrentStageNumber
        model.CurrentStageName = model.CurrentStageName
        model.OpportunityName = request.data['OpportunityName']
        model.Industry = request.data['Industry']
        model.LinkedDocumentType = request.data['LinkedDocumentType']
        model.DataOwnershipfield = request.data['DataOwnershipfield']
        model.DataOwnershipName = request.data['DataOwnershipName']
        model.StatusRemarks = request.data['StatusRemarks']
        model.ProjectCode = request.data['ProjectCode']
        model.CustomerName = request.data['CustomerName']
        model.ClosingDate = request.data['ClosingDate']
        model.ClosingType = request.data['ClosingType']
        model.OpportunityType = request.data['OpportunityType']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        model.U_TYPE = request.data['U_TYPE']
        model.U_LSOURCE = request.data['U_LSOURCE']
        model.U_FAV = request.data['U_FAV']
        model.U_PROBLTY = request.data['U_PROBLTY']

        model.save()
        #print(model)
        #SELECT * FROM `opportunity_line` WHERE `SequenceNo`=5 and StageKey=2 order by LineNum desc limit 1;
        #SELECT * FROM `opportunity_line` WHERE `SequenceNo`=5 order by LineNum desc limit 1;
        
        # get object
        #line = Line.objects.filter(SequenceNo = request.data['SequentialNo']).order_by('-LineNum')[:1] 
        
        try:
            line = Line.objects.filter(SequenceNo = request.data['SequentialNo']).order_by('-LineNum')[:1]
            NewLine = int(line[0].LineNum) + 1
            print(NewLine)
        except:
            NewLine=0
            print(NewLine)
        
        LineNum = NewLine
        SalesPerson = request.data['SalesOpportunitiesLines'][0]['SalesPerson']
        ContactPerson = request.data['ContactPerson']
        StartDate = request.data['StartDate']
        MaxLocalTotal = request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal']
        MaxSystemTotal = request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal']
        Remarks = request.data['Remarks']
        Contact="tNO"
        Status = request.data['Status']
        #StageKey = request.data['SalesOpportunitiesLines'][0]['StageKey']
        StageKey = model.CurrentStageNo
        ClosingDate = request.data['ClosingDate']
        SequenceNo = request.data['SequentialNo']
        Opp_Id = fetchid
        
        model_line = Line(LineNum=LineNum, SalesPerson=SalesPerson, StartDate=StartDate, StageKey=StageKey, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Contact=Contact, Status=Status, ContactPerson=ContactPerson, ClosingDate=ClosingDate,Opp_Id=Opp_Id)    
        
        model_line.save()  
        
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
            print(db)
        data = json.loads(db)

        r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        opp_data = {
          "CardCode": request.data['CardCode'],
          "PredictedClosingDate": request.data['PredictedClosingDate'],
          "ContactPerson": request.data['ContactPerson'],
          "DataOwnershipfield": request.data['DataOwnershipfield'],
          "MaxLocalTotal": request.data['MaxLocalTotal'],
          "MaxSystemTotal": request.data['MaxSystemTotal'],
          "Remarks": request.data['Remarks'],
          "SalesOpportunitiesLines": [
            {
              "DocumentType": "bodt_MinusOne",
              "MaxLocalTotal": request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal'],
              "MaxSystemTotal": request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal'],
              "SalesPerson": request.data['SalesOpportunitiesLines'][0]['SalesPerson'],
              #"StageKey": request.data['SalesOpportunitiesLines'][0]['StageKey']
              "StageKey": model.CurrentStageNo
            }
          ],
          "SalesPerson": request.data['SalesPerson'],
          "StartDate": request.data['StartDate'],
          #"U_TYPE": request.data['U_TYPE'],
          "OpportunityName": request.data['OpportunityName']
        }
        
        print(json.dumps(opp_data))
    
        print('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+request.data['SequentialNo']+')');
        
        res = requests.patch('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+request.data['SequentialNo']+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)


        context = {
            'id':request.data['id'],
            'SequentialNo':request.data['SequentialNo'],
            'CardCode':request.data['CardCode'],
            'SalesPerson':request.data['SalesPerson'],
            'SalesPersonName':request.data['SalesPersonName'],
            'ContactPerson':request.data['ContactPerson'],
            'ContactPersonName':request.data['ContactPersonName'],
            "DataOwnershipfield": request.data['DataOwnershipfield'],
            "DataOwnershipName": request.data['DataOwnershipName'],
            'Source':request.data['Source'],
            'StartDate':request.data['StartDate'],
            'PredictedClosingDate':request.data['PredictedClosingDate'],
            'MaxLocalTotal':request.data['MaxLocalTotal'],
            'MaxSystemTotal':request.data['MaxSystemTotal'],
            'Remarks':request.data['Remarks'],
            'Status':request.data['Status'],
            'ReasonForClosing':request.data['ReasonForClosing'],
            'TotalAmountLocal':request.data['TotalAmountLocal'],
            'TotalAmounSystem':request.data['TotalAmounSystem'],
            'CurrentStageNo':model.CurrentStageNo,
            'CurrentStageNumber':model.CurrentStageNumber,
            'CurrentStageName':model.CurrentStageName,
            'OpportunityName':request.data['OpportunityName'],
            'Industry':request.data['Industry'],
            'LinkedDocumentType':request.data['LinkedDocumentType'],
            'StatusRemarks':request.data['StatusRemarks'],
            'ProjectCode':request.data['ProjectCode'],
            'CustomerName':request.data['CustomerName'],
            'ClosingDate':request.data['ClosingDate'],
            'ClosingType':request.data['ClosingType'],
            'OpportunityType':request.data['OpportunityType'],
            'UpdateDate':request.data['UpdateDate'],
            'UpdateTime':request.data['UpdateTime'],
            'U_TYPE':request.data['U_TYPE'],
            'U_LSOURCE':request.data['U_LSOURCE'],
            'U_FAV':request.data['U_FAV'],
            'U_PROBLTY':request.data['U_PROBLTY']
        }

        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
        else:
            return Response({"message":"successful","status":200, "data":[context]})
    except Exception as e:
        #print(e)
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Stage Create API
@api_view(['POST'])
def create_stage(request):

    chk = Stage.objects.filter(Opp_Id = request.data['Opp_Id'], Stageno = request.data['Stageno'])
    if chk[0].Status==2:
        return Response({"message":"Can not create due to CurrentStage already completed","status":201,"data":[]})

    SequenceNo = request.data['SequenceNo']
    Name = request.data['Name']
    Stageno = round(float(request.data['Stageno']) + float(.1),1)
    ClosingPercentage = request.data['ClosingPercentage']
    Cancelled = request.data['Cancelled']
    IsSales = request.data['IsSales']
    IsPurchasing = request.data['IsPurchasing']
    Opp_Id = request.data['Opp_Id']
    CreateDate = request.data['CreateDate']
    UpdateDate = request.data['UpdateDate']

    print(Stageno)
    model = Stage(SequenceNo=SequenceNo, Name=Name, Stageno=Stageno, ClosingPercentage=ClosingPercentage, Cancelled=Cancelled, IsSales=IsSales, IsPurchasing=IsPurchasing, Opp_Id=Opp_Id, CreateDate=CreateDate, UpdateDate=UpdateDate)
    model.save()
    return Response({"message":"successful","status":200,"data":[]})



#Stage All API
@api_view(["POST"])
def all_stage(request):
    Opp_Id=request.data['Opp_Id']    
    stages_obj = Stage.objects.filter(Opp_Id=Opp_Id).order_by("Stageno")        
    stages_json = StageSerializer(stages_obj, many=True)
    return Response({"message": "Success","status": 200,"data":stages_json.data})

#Stage One API
@api_view(["POST"])
def one_stage(request):
    SequenceNo=request.data['SequenceNo']    
    stage_obj = Stage.objects.get(SequenceNo=SequenceNo)
    stage_json = StageSerializer(stage_obj)
    return Response({"message": "Success","status": 200,"data":[stage_json.data]})

#Stage_detail One API
@api_view(["POST"])
def stage_detail(request):
    Opp_Id=request.data['Opp_Id']
    Stageno=request.data['Stageno']
    stage_obj = Stage.objects.filter(Opp_Id=Opp_Id,Stageno=Stageno)
    print(stage_obj);
    stage_json = StageSerializer(stage_obj, many=True)
    return Response({"message": "Success","status": 200,"data":stage_json.data})


#Line All API
@api_view(["POST"])
def all_line(request):
    SequenceNo=request.data['SequenceNo']    
    line_obj = Line.objects.filter(SequenceNo=SequenceNo)
    line_json = LineSerializer(line_obj, many=True)
    return Response({"message": "Success","status": 200,"data":line_json.data})

#Line One API
@api_view(["POST"])
def one_line(request):
    SequenceNo=request.data['SequenceNo']    
    LineNum=request.data['LineNum']    
    line_obj = Line.objects.filter(SequenceNo=SequenceNo, LineNum=LineNum)
    line_json = LineSerializer(line_obj, many=True)
    return Response({"message": "Success","status": 200,"data":line_json.data})

#Opp Stage Update API
@api_view(['POST'])
def change_stage(request):
    fetchid = request.data['Opp_Id']
    print("come 0")
    chk = Stage.objects.filter(Opp_Id = fetchid, Stageno = request.data['Stageno'])
    if chk[0].Status==2:
        return Response({"message":"CurrentStage already completed","status":201,"data":[]})
    
    st_max = Stage.objects.filter(Opp_Id = fetchid).order_by('-Stageno')[:1]
    
    print(st_max[0].Stageno)
    
    if float(request.data['Stageno']) > 1:
        if st_max == float(request.data['Stageno']) :
            cur_stg = float(request.data['Stageno'])
        else:
            next_stg = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            #SELECT * FROM `Opportunity_stage` WHERE Opp_Id=8 and Stageno > 1 order by Stageno limit 1
            cur_stg = next_stg[0].Stageno
            cur_name = next_stg[0].Name
    
        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()
        print(cur_stg)
        
        stg_obj = Stage.objects.filter(Opp_Id = fetchid, Stageno__lte = float(request.data['Stageno'])).order_by('Stageno')
    
        for stg in stg_obj:
            print(stg)
            if(int(stg.Status) != 2):
                print("come")
                stg.Status= 2
                stg.UpdateDate=request.data['UpdateDate']
                
                stg.Comment=request.data['Comment']
                
                stg.save()
                
                try:
                    upload = request.FILES['File']
                    target = 'bridge/static/image/'+fetchid+'/'
                    os.makedirs(target, exist_ok=True)
                    fss = FileSystemStorage()
                    file = fss.save(target+"/"+upload.name, upload)
                    #file_url = fss.url(file)
                    file_url = '/static/image/'+fetchid+'/'+upload.name
                    #file_url = file_url.replace('/bridge','')
                    print(file_url)                
                    stg.File=file_url
                    stg.save()
                except:
                    stg.save()
        
        if float(request.data['Stageno']) != st_max[0].Stageno:
            current = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            obj = Stage.objects.get(pk=current[0].id)
            obj.Status = 1
            obj.UpdateDate=request.data['UpdateDate']
            obj.save()
            
        stg_objs = Stage.objects.filter(Opp_Id = fetchid).order_by('Stageno')
        stg_json = StageSerializer(stg_objs, many=True)
        
        print(request.data['Stageno'])
        print(type(request.data['Stageno']))
        
        if type(request.data['Stageno']) == int:
            print("int num")
            
            model = Opportunity.objects.get(pk = request.data['Opp_Id'])        
            
            with open("../bridge/bridge/db.json") as f:
                db = f.read()
                print(db)
            data = json.loads(db)

            r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
              "CardCode": model.CardCode,
              "PredictedClosingDate": model.PredictedClosingDate,
              "ContactPerson": int(model.ContactPerson),
              "DataOwnershipfield": int(model.DataOwnershipfield),
              "MaxLocalTotal": float(model.MaxLocalTotal),
              "MaxSystemTotal": float(model.MaxSystemTotal),
              "Remarks": model.Remarks,
              "SalesOpportunitiesLines": [
                {
                  "DocumentType": "bodt_MinusOne",
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "SalesPerson": int(model.SalesPerson),
                  "StageKey": float(request.data['Stageno'])
                }
              ],
              "SalesPerson": int(model.SalesPerson),
              "StartDate": model.StartDate,
              #"U_TYPE": request.data['U_TYPE'],
              "OpportunityName": model.OpportunityName
            }
            
            print(opp_data)
            print(json.dumps(opp_data))

            print('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')');
        
            res = requests.patch('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":stg_json.data})
            else:
                return Response({"message":"successful","status":200, "data":stg_json.data})
        else:
            return Response({"message":"successful","status":200, "data":stg_json.data})

        #return Response({"message": "Success","status": 200,"data":stg_json.data})
    
    else:
    
        if st_max == float(request.data['Stageno']) :
            cur_stg = float(request.data['Stageno'])
        else:
            next_stg = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            #SELECT * FROM `Opportunity_stage` WHERE Opp_Id=8 and Stageno > 1 order by Stageno limit 1
            cur_stg = next_stg[0].Stageno
            cur_name = next_stg[0].Name
    
        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()
        print(cur_stg)
    
        stg_obj = Stage.objects.get(Opp_Id = fetchid, Stageno = float(request.data['Stageno']))
        print("come 1")
        stg_obj.Status=2
        stg_obj.UpdateDate=request.data['UpdateDate']
        stg_obj.Comment=request.data['Comment']

        try:
            upload = request.FILES['File']
            target = 'bridge/static/image/'+fetchid+'/'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+upload.name, upload)
            #file_url = fss.url(file)
            file_url = '/static/image/'+fetchid+'/'+upload.name
            #file_url = file_url.replace('/bridge','')
            print(file_url)                
            stg_obj.File=file_url
            stg_obj.save()
        except:
            stg_obj.save()
        
        #SELECT * FROM `opportunity_stage` WHERE Opp_Id=85 and stageno > 2 order by stageno limit 1;
        current = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
        obj = Stage.objects.get(pk=current[0].id)
        obj.Status = 1
        obj.UpdateDate=request.data['UpdateDate']
        obj.save()
       
        # for obj in current:
            # obj.Status=1
            # obj.save()
        
        stg_objs = Stage.objects.filter(Opp_Id = fetchid).order_by('Stageno')
        stg_json = StageSerializer(stg_objs, many=True)
        
        
        print(request.data['Stageno'])
        print(type(request.data['Stageno']))
        
        if (type(request.data['Stageno']) == int)==True:
            print("int num")
            
            model = Opportunity.objects.get(pk = request.data['Opp_Id'])        
            
            data = {"CompanyDB":"TEST","Password":"Qwer1234","UserName":"manager"}

            r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
              "CardCode": model.CardCode,
              "PredictedClosingDate": model.PredictedClosingDate,
              "ContactPerson": int(model.ContactPerson),
              "DataOwnershipfield": int(model.DataOwnershipfield),
              "MaxLocalTotal": float(model.MaxLocalTotal),
              "MaxSystemTotal": float(model.MaxSystemTotal),
              "Remarks": model.Remarks,
              "SalesOpportunitiesLines": [
                {
                  "DocumentType": "bodt_MinusOne",
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "SalesPerson": int(model.SalesPerson),
                  "StageKey": float(request.data['Stageno'])
                }
              ],
              "SalesPerson": int(model.SalesPerson),
              "StartDate": model.StartDate,
              #"U_TYPE": request.data['U_TYPE'],
              "OpportunityName": model.OpportunityName
            }
            
            print(opp_data)
            print(json.dumps(opp_data))

            print('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')');
        
            res = requests.patch('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":stg_json.data})
            else:
                return Response({"message":"successful","status":200, "data":stg_json.data})
        else:
            return Response({"message":"successful","status":200, "data":stg_json.data})
        
        #return Response({"message": "Success","status": 200,"data":stg_json.data})
        
#Opp Fav Update API
@api_view(['POST'])
def fav(request):
    fetchid = request.data['id']
    model = Opportunity.objects.get(pk = fetchid)
    model.U_FAV  = request.data['U_FAV']
    model.save()
    return Response({"message":"successful","status":200, "data":[]})


#Opp Stage Update API
@api_view(['POST'])
def change_stage1(request):
    fetchid = request.data['Opp_Id']
    
    if type(request.data['CurrentStageNo']) == str:
        return Response({"message":"CurrentStageNo should be int or float","status":201,"data":[]})
    else:
        try:
            model = Opportunity.objects.get(pk = fetchid)        
            print(model)
            model.CurrentStageNo  = request.data['CurrentStageNo']
            model.UpdateDate  = request.data['UpdateDate']
            model.UpdateTime  = request.data['UpdateTime']

            model.save()
            
            stage = Stage.objects.get(Opp_Id = fetchid, Stageno=request.data['CurrentStageNo'])
            print(stage)
            
            stage.UpdateDate  = request.data['UpdateDate']
            stage.Status  = 1
            stage.save()

            context = {
                "CurrentStageNo":request.data['CurrentStageNo'],
                "UpdateDate ":request.data['UpdateDate'],
                "UpdateTime ":request.data['UpdateTime']            
            }
            
            if type(request.data['CurrentStageNo']) == int:
                print("int num")
                
                with open("../bridge/bridge/db.json") as f:
                    db = f.read()
                    print(db)
                data = json.loads(db)

                r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)
                
                opp_data = {
                  "CardCode1": model.CardCode,
                  "PredictedClosingDate": model.PredictedClosingDate,
                  "ContactPerson": int(model.ContactPerson),
                  "DataOwnershipfield": int(model.DataOwnershipfield),
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "Remarks": model.Remarks,
                  "SalesOpportunitiesLines": [
                    {
                      "DocumentType": "bodt_MinusOne",
                      "MaxLocalTotal": float(model.MaxLocalTotal),
                      "MaxSystemTotal": float(model.MaxSystemTotal),
                      "SalesPerson": int(model.SalesPerson),
                      "StageKey": request.data['CurrentStageNo']
                    }
                  ],
                  "SalesPerson": int(model.SalesPerson),
                  "StartDate": model.StartDate,
                  #"U_TYPE": request.data['U_TYPE'],
                  "OpportunityName": model.OpportunityName
                }
                
                print(opp_data)
                print(json.dumps(opp_data))
        
                print('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')');
            
                res = requests.patch('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
                
                if len(res.content) !=0 :
                    res1 = json.loads(res.content)
                    SAP_MSG = res1['error']['message']['value']
                    return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
                else:
                    return Response({"message":"successful","status":200, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[context]})
        except:
            return Response({"message":"ID Wrong","status":201,"data":[]})


#Opp Stage Update API
@api_view(['POST'])
def complete(request):
    fetchid = request.data['Opp_Id']
    try:
        model = Opportunity.objects.get(pk = fetchid)        
        print(model)
        model.Remarks  = request.data['Remarks']
        model.Status  = request.data['Status']
        model.UpdateDate  = request.data['UpdateDate']
        model.UpdateTime  = request.data['UpdateTime']
        
        model.save()
        
        stages = Stage.objects.filter(Opp_Id = fetchid)
        for stage in stages:
            stage.Status  = 2
            stage.save()

        st_max = Stage.objects.filter(Opp_Id = fetchid).order_by('-Stageno')[:1]
    
        cur_stg = st_max[0].Stageno
        cur_name = st_max[0].Name

        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()

        context = {
            #"CurrentStageNo":request.data['CurrentStageNo'],
            "UpdateDate ":request.data['UpdateDate'],
            "UpdateTime ":request.data['UpdateTime']            
        }
        
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
            print(db)
        data = json.loads(db)

        r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        opp_data = {
          "Remarks": request.data['Remarks'],
          "Status": request.data['Status']
        }
        
        print(opp_data)
        print(json.dumps(opp_data))

        print('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')');
    
        res = requests.patch('http://103.107.67.94:50001/b1s/v1/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
        else:
            return Response({"message":"successful","status":200, "data":[context]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})