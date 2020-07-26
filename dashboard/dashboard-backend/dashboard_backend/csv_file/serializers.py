from rest_framework import serializers
from .models import CsvFile, CommonPeriod

# CsvFile Serializer
class CsvFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields = '__all__'

# CommonPeriod Serializer
class CommonPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonPeriod
        fields = '__all__'