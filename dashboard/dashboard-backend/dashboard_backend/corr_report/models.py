from django.db import models




# Create your models here.


def time_series_dir_path(instance, filename):
    return "{}".format(filename)


def gephi_report_dir_path(instance, filename):
    return "{}/gephi".format(filename)


def corr_csv_dir_path(instance, filename):
    return "{}/corr_csv".format(filename)


def metrics_csv_dir_path(instance, filename):
    return "{}/metrics".format(filename)


class CorrReport(models.Model):
    report_name: models.CharField(max_length=50, unique=True)
    time_series_graph: models.FileField(upload_to=time_series_dir_path)
    gephi_report: models.FileField(upload_to=gephi_report_dir_path)
    corr_csv: models.FileField(upload_to=corr_csv_dir_path)
    metrics_csv: models.FileField(upload_to=metrics_csv_dir_path)