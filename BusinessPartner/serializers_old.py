from rest_framework import serializers
from .models import *

class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1

class BPSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['id',"CardCode", "CardName", "Industry", "CardType", "SalesPersonCode", "U_CONTOWNR"]
        
        #exclude = ['id']
        #fields = "__all__"
        #depth = 1


class BPAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPAddresses
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1
        
class BPBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPBranch
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class BPEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPEmployee
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class BPDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPDepartment
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class BPPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPPosition
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
                