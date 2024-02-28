from django.contrib import admin
from .models import Metric, BlockchainMetric

# Register your models here.
admin.site.register(Metric)
admin.site.register(BlockchainMetric)
