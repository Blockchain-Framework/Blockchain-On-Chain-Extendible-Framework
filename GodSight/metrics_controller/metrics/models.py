from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid

class Metric(models.Model):
    metric_name = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    formula = models.JSONField(blank=True, null=True)  # Assuming formula is optional
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.metric_name

class BlockchainMetric(models.Model):
    blockchain_id = models.UUIDField(default=uuid.uuid4, editable=False)
    blockchain = models.CharField(max_length=255)
    sub_chain = models.CharField(max_length=255)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('blockchain_id', 'metric'),)

    def __str__(self):
        return f"{self.blockchain}/{self.sub_chain} - {self.metric.metric_name}"

class TransactionsFeatureMapping(models.Model):
    blockchain = models.CharField(max_length=255)
    sub_chain = models.CharField(max_length=255)
    sourceField = models.CharField(max_length=255)
    targetField = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # 'feature' or 'function'
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('blockchain', 'sub_chain', 'sourceField')

class EmittedUtxosFeatureMapping(models.Model):
    blockchain = models.CharField(max_length=255)
    sub_chain = models.CharField(max_length=255)
    sourceField = models.CharField(max_length=255)
    targetField = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # 'feature' or 'function'
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('blockchain', 'sub_chain', 'sourceField')

class ConsumedUtxosFeatureMapping(models.Model):
    blockchain = models.CharField(max_length=255)
    sub_chain = models.CharField(max_length=255)
    sourceField = models.CharField(max_length=255)
    targetField = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # 'feature' or 'function'
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('blockchain', 'sub_chain', 'sourceField')
