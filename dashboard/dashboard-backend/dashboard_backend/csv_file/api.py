from .models import CsvFile, CommonPeriod
from rest_framework import viewsets, permissions
from .serializers import CsvFileSerializer, CommonPeriodSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.cache import cache

from python_scripts.data_processor import DataProcessor
from python_scripts.data_analyser import DataAnalyser


# CsvFile Viewset


class CsvFileViewSet(viewsets.ModelViewSet):
    queryset = CsvFile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CsvFileSerializer

    # @action(detail=False, methods=['post'])
    # def get_common_period(self, request):
    #     try:
    #         data_processor = DataProcessor()
    #         res_obj = data_processor.find_common_period(
    #             request.data)

    #         return Response(data=res_obj)
    #     except:
    #         return Response(status=404)

# Common Period View


class CommonPeriodViewSet(viewsets.ModelViewSet):
    queryset = CommonPeriod.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CommonPeriodSerializer

    @action(detail=False, methods=['post'])
    def get_common_period(self, request):
        try:
            data_processor = DataProcessor()
            merged_df, res_obj = data_processor.find_common_period(
                request.data)

            cache.set("data_processor", data_processor)
            cache.set("merged_df", merged_df)

            return Response(data={"data": res_obj})
        except:
            return Response(status=404)

    # @action(detail=False, methods=['post'])
    # def generate_reports(self, request):
    #     print("===== GENERATE REPORT ==== ")
    #     try:
    #         data = request.data
    #         dataProcessor = cache.get("data_processor")
    #         merged_df = cache.get("merged_df")

    #         processed_data = dataProcessor.process_raw_data(merged_df, data["startDate"], data["endDate"])
            
    #         dataAnalyser = DataAnalyser(processed_data)
    #         dataAnalyser.get_reports("report name", data["windowSize"])

    #         return Response(data={"data": "generate data"})
    #     except:
    #         return Response(status=404)
