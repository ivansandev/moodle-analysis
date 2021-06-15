from django.db import models
from django.contrib.auth.models import User
from .helpers.application_field_content import selectin_list_for_application_field as appl_field_sl
from .helpers.analysis import NpEncoder


class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    platform_name = models.CharField(max_length=255)
    platform_type = models.CharField(max_length=255)
    platform_url = models.URLField(max_length=512)
    course_name = models.CharField(max_length=255)
    application_field = models.CharField(max_length=255, choices=appl_field_sl, default=appl_field_sl[0][1][0][0][0])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course_name} @ {self.platform_name}'

class CorrelationAnalysis(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    correlation_data = models.JSONField(encoder=NpEncoder)
    freq_distrib = models.JSONField(encoder=NpEncoder)

    def __str__(self):
        return f'Корелация: {self.upload.platform_name}'


class StatisticalAnalysis(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    exercise = models.CharField(max_length=512)
    mean = models.DecimalField(max_digits=6, decimal_places=4)
    mode = models.CharField(max_length=512)
    median = models.DecimalField(max_digits=6, decimal_places=4)
    rel_freq = models.DecimalField(max_digits=6, decimal_places=4)
    abs_freq = models.IntegerField()
    spread = models.DecimalField(max_digits=6, decimal_places=4)
    variance = models.DecimalField(max_digits=6, decimal_places=4)
    stdev = models.DecimalField(max_digits=6, decimal_places=4)

    def __str__(self):
        return f'Статистика {self.upload.platform_name} > {self.exercise}'
