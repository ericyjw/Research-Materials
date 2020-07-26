from django.db import models


from django_matplotlib import MatplotlibFigureField

# Create your models here.
class CsvFile(models.Model):
    fileName = models.CharField(max_length=50, unique=True)
    headers = models.TextField()
    data = models.TextField()

class CommonPeriod(models.Model):
    figure = MatplotlibFigureField(figure='my_figure')
    startDate = models.TextField
    endDate = models.TextField
    common = models.BigIntegerField