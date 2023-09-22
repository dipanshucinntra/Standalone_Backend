from django.db import models  

class BPAddresses(models.Model):
    BPID = models.CharField(max_length=50, blank=True)
    BPCode = models.CharField(max_length=50, blank=True)
    AddressName = models.CharField(max_length=100, blank=True)
    Street = models.CharField(max_length=100, blank=True)
    Block = models.CharField(max_length=100, blank=True)
    City = models.CharField(max_length=100, blank=True)
    State = models.CharField(max_length=100, blank=True)
    ZipCode = models.CharField(max_length=100, blank=True)
    Country = models.CharField(max_length=100, blank=True)
    AddressType = models.CharField(max_length=100, blank=True)
    RowNum = models.CharField(max_length=3, blank=True)
    U_SHPTYP = models.CharField(max_length=100, blank=True)
    U_COUNTRY = models.CharField(max_length=100, blank=True)
    U_STATE = models.CharField(max_length=100, blank=True)

class BusinessPartner(models.Model):
    CardCode = models.CharField(max_length=100, blank=True)
    CardName = models.CharField(max_length=100, blank=True)
    Industry = models.CharField(max_length=100, blank=True)
    CardType = models.CharField(max_length=100, blank=True)
    
    Website = models.CharField(max_length=100, blank=True)
    EmailAddress = models.CharField(max_length=100, blank=True)
    Phone1 = models.CharField(max_length=100, blank=True)
    
    DiscountPercent = models.CharField(max_length=100, blank=True)
    Currency = models.CharField(max_length=100, blank=True)
    IntrestRatePercent = models.CharField(max_length=100, blank=True)
    CommissionPercent = models.CharField(max_length=100, blank=True)
    Notes = models.CharField(max_length=100, blank=True)
    PayTermsGrpCode = models.CharField(max_length=100, blank=True)
    CreditLimit = models.CharField(max_length=100, blank=True)
    AttachmentEntry = models.CharField(max_length=100, blank=True)
    SalesPersonCode = models.CharField(max_length=5, blank=True)
    ContactPerson = models.CharField(max_length=100, blank=True)
    
    BPAddresses = models.CharField(max_length=100, blank=True)
    U_PARENTACC = models.CharField(max_length=100, blank=True)
    U_BPGRP = models.CharField(max_length=100, blank=True)
    U_CONTOWNR = models.CharField(max_length=100, blank=True)
    U_RATING = models.CharField(max_length=100, blank=True)
    U_TYPE = models.CharField(max_length=100, blank=True)
    U_ANLRVN = models.CharField(max_length=100, blank=True)
    U_CURBAL = models.CharField(max_length=100, blank=True)
    U_ACCNT = models.CharField(max_length=100, blank=True)
    U_INVNO = models.CharField(max_length=100, blank=True)
    
    U_LAT = models.CharField(max_length=100, blank=True)
    U_LONG = models.CharField(max_length=100, blank=True)
    
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)
    U_LEADID = models.CharField(max_length=10, blank=True, default='0')
    U_LEADNM = models.CharField(max_length=100, blank=True, default='')

class BPBranch(models.Model):
    BPID = models.CharField(max_length=4, blank=True)
    RowNum = models.CharField(max_length=4, blank=True)
    BPCode = models.CharField(max_length=100, blank=True)
    BranchName = models.CharField(max_length=100, blank=True)
    AddressName = models.CharField(max_length=100, blank=True)
    AddressName2 = models.CharField(max_length=100, blank=True)
    AddressName3 = models.CharField(max_length=100, blank=True)
    BuildingFloorRoom = models.CharField(max_length=100, blank=True)
    Street = models.CharField(max_length=100, blank=True)
    Block = models.CharField(max_length=100, blank=True)
    County = models.CharField(max_length=100, blank=True)
    City = models.CharField(max_length=100, blank=True)
    State = models.CharField(max_length=100, blank=True)
    ZipCode = models.CharField(max_length=100, blank=True)
    Country = models.CharField(max_length=100, blank=True)
    AddressType = models.CharField(max_length=100, blank=True)
    Phone = models.CharField(max_length=100, blank=True)
    Fax = models.CharField(max_length=100, blank=True)
    Email = models.CharField(max_length=100, blank=True)
    TaxOffice = models.CharField(max_length=100, blank=True)
    GSTIN = models.CharField(max_length=100, blank=True)
    GstType = models.CharField(max_length=100, blank=True)
    ShippingType = models.CharField(max_length=100, blank=True)
    PaymentTerm = models.CharField(max_length=100, blank=True)
    CurrentBalance = models.CharField(max_length=100, blank=True)
    CreditLimit = models.CharField(max_length=100, blank=True)    
    Lat = models.CharField(max_length=100, blank=True)
    Long = models.CharField(max_length=100, blank=True)
    Status = models.IntegerField(default=1)
    Default = models.IntegerField(default=0)
    
    U_SHPTYP = models.CharField(max_length=20, blank=True)
    U_COUNTRY = models.CharField(max_length=20, blank=True)
    U_STATE = models.CharField(max_length=20, blank=True)
    
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)

class BPEmployee(models.Model):
    Title = models.CharField(max_length=100, blank=True)
    FirstName = models.CharField(max_length=100, blank=True)
    MiddleName = models.CharField(max_length=100, blank=True)
    LastName = models.CharField(max_length=100, blank=True)
    Position = models.CharField(max_length=100, blank=True)
    Address = models.CharField(max_length=100, blank=True)
    MobilePhone = models.CharField(max_length=100, blank=True)
    Fax = models.CharField(max_length=100, blank=True)
    E_Mail = models.CharField(max_length=100, blank=True)
    Remarks1 = models.CharField(max_length=100, blank=True)
    InternalCode = models.CharField(max_length=100, blank=True)
    DateOfBirth = models.CharField(max_length=100, blank=True)
    Gender = models.CharField(max_length=100, blank=True)
    Profession = models.CharField(max_length=100, blank=True)
    CardCode = models.CharField(max_length=100, blank=True)

    U_BPID = models.IntegerField(default=0)
    U_BRANCHID = models.CharField(max_length=100, blank=True)
    U_NATIONALTY = models.CharField(max_length=100, blank=True)

    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)

class BPPosition(models.Model):
    PositionID = models.CharField(max_length=4, blank=True)
    Name = models.CharField(max_length=100, blank=True)
    Description = models.CharField(max_length=200, blank=True)

class BPDepartment(models.Model):
    Code = models.CharField(max_length=4, blank=True)
    Name = models.CharField(max_length=100, blank=True)
    Description = models.CharField(max_length=200, blank=True)

class BPType(models.Model):
    Type = models.CharField(max_length=255, blank=True)

#added by millan on 04-10-2022
class Attachment(models.Model):
    File = models.CharField(max_length=150, blank=True)
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)
    CustId = models.IntegerField(default=0)
    Size = models.CharField(max_length=100, blank=True)
