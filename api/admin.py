from django.contrib import admin
from .models import Upload, CorrelationAnalysis, StatisticalAnalysis


# Register your models here.
admin.site.register(Upload)
admin.site.register(CorrelationAnalysis)
admin.site.register(StatisticalAnalysis)
