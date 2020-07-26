from .models import CorrReport
from rest_framework import viewsets, permissions
from .serializers import CorrReportSerializer

from rest_framework.response import Response
from rest_framework.decorators import action

from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from python_scripts.data_analyser import DataAnalyser

import os
from django.core.files import File
from django.conf import settings
# from PIL import Image
# CorrReport Viewset


class CorrReportViewSet(viewsets.ModelViewSet):
    queryset = CorrReport.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CorrReportSerializer

    @action(detail=False, methods=['post'])
    def generate_reports(self, request):

        print("===== GENERATE REPORT ==== ")
        try:
            data = request.data
            dataProcessor = cache.get("data_processor")
            merged_df = cache.get("merged_df")

            processed_data = dataProcessor.process_raw_data(
                merged_df, data["startDate"], data["endDate"])

            dataAnalyser = DataAnalyser(merged_df, processed_data)

            # tmp_dir: graph-chart saved to tmp/graph_chart/report_name
            time_series_plts, corr_df = dataAnalyser.get_reports(
                data["reportName"], int(data["windowSize"]))

            fs = FileSystemStorage()
            tmp_dir = 'temp'
            reportName = data["reportName"]

            print("===== Graph Chart Save =====")
            tmp_graph_chart_dir_path = os.path.join(
                tmp_dir, 'graph_chart', reportName)
            # if not os.path.exists(tmp_graph_chart_dir_path):
            #     os.makedirs(tmp_graph_chart_dir_path)
            for _, _, f in os.walk(tmp_graph_chart_dir_path):
                for file in f:
                    if '.png' in file:
                        print('file: {}'.format(file))
                        tmp_graph_chart_file_path = os.path.join(
                            tmp_graph_chart_dir_path, file)
                        file_ = File(open(tmp_graph_chart_file_path, 'rb'))
                        media_graph_chart_path = 'graph_chart/{}/{}'.format(
                            reportName, file)
                        # media_dir: graph-chart saved to media/graph_chart/report_name
                        fs.save(media_graph_chart_path, file_)

                        os.remove(tmp_graph_chart_file_path)

            print("===== Corr Matrix Save =====")
            tmp_corr_report_dir_path = os.path.join(
                tmp_dir, 'corr_report', reportName)
            if not os.path.exists(tmp_corr_report_dir_path):
                os.makedirs(tmp_corr_report_dir_path)

            for i in range(len(corr_df)):
                corr = corr_df[i]
                filename = "corr_report_{}.csv".format(i)
                tmp_corr_report_file_path = os.path.join(
                    tmp_corr_report_dir_path, filename)

                # tmp_dir: corr-report saved to tmp/corr_report/report_name
                corr.to_csv(tmp_corr_report_file_path)

                file_ = File(open(tmp_corr_report_file_path, 'rb'))
                media_corr_report_path = "corr_report/{}/{}".format(
                    reportName, filename)
                # media_dir: corr-report saved to media/corr_report/report_name
                fs.save(media_corr_report_path, file_)

                os.remove(tmp_corr_report_file_path)

            print("===== Gephi Analysis =====")
            curr_dir = os.getcwd()
            gephi_visualisation_path = os.path.join(
                curr_dir, 'python_scripts', 'gephi_visualisation')
            os.chdir(gephi_visualisation_path)
            os.system('mvn clean install')

            saved_corr_report_path = os.path.join(
                settings.MEDIA_ROOT, 'corr_report', reportName)
            temp_gephi_report_path = os.path.join(
                tmp_dir, 'gephi_report', reportName)
            for _, dir, f in os.walk(saved_corr_report_path):
                for file in f:
                    if '.csv' in file:
                        print('csv file: {}'.format(file))
                        filename = '{}/{}'.format(
                            saved_corr_report_path, file)

                        # tmp_dir: gephi-report saved to tmp/gephi_report/report_name
                        os.system(
                            'mvn exec:java -Dexec.mainClass=Main -Dexec.args="{} {}" -Dexec.cleanupDaemonThreads=false'.format(temp_gephi_report_path, filename))

            for root, _, f in os.walk(temp_gephi_report_path):
                for file in f:
                    tmp_gephi_report_file_path = os.path.join(root, file)

                    directories = root.split("/")
                    file_format = directories[len(directories) - 1]

                    file_ = File(open(tmp_gephi_report_file_path, 'rb'))
                    media_gephi_report_path = 'gephi_report/{}/{}/{}'.format(
                        reportName, file_format, file)

                    # media_dir: graph-chart saved to media/gephi_report/report_name/file_type
                    fs.save(media_gephi_report_path, file_)

                    os.remove(tmp_gephi_report_file_path)

            return Response(data={"data": "generated report"})
        except:
            return Response(status=404)
