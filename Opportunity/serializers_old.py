from rest_framework import serializers
from .models import *

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = "__all__"
        #exclude = ['id']
        #depth = 1
        
class OppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'OpportunityName']
        
class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = "__all__"
        #exclude = ['id']
        #depth = 1
class StaticStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticStage
        fields = "__all__"
        #exclude = ['id']
        #depth = 1

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = "__all__"
        #exclude = ['id']
        #depth = 1

		