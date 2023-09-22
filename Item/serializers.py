from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        depth = 1
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

