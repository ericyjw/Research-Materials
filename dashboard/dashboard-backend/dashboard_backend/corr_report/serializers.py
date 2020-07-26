from rest_framework import serializers
from .models import CorrReport

# CorrReport Serializer
class CorrReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrReport
        fields = '__all__'