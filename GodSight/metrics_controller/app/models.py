from django.db import models
import uuid


class Blockchain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blockchain = models.CharField(max_length=255)
    sub_chain = models.CharField(max_length=255)
    original = models.BooleanField(default=False)
    start_date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('blockchain', 'sub_chain',)
        db_table = 'blockchain_table'

class Metric(models.Model):
    metric_name = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    grouping_type = models.CharField(max_length=255)
    formula = models.JSONField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'metric_table'

class ChainMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE, db_column='blockchain_id', related_name='metrics')
    metric_name = models.ForeignKey(Metric, on_delete=models.CASCADE, db_column='metric_name')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chain_metric'
        unique_together = (('blockchain', 'metric_name'),)




class MetricsData(models.Model):
    date = models.DateField()
    blockchain = models.CharField(max_length=255)
    subchain = models.CharField(max_length=255)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='metrics_data')
    value = models.FloatField()

    class Meta:
        unique_together = ('date', 'blockchain', 'subchain', 'metric',)
        db_table = 'metrics_data'


class GeneralModel(models.Model):
    field_name = models.CharField(max_length=64, primary_key=True)
    data_type = models.CharField(max_length=64)
    description = models.TextField()

    class Meta:
        db_table = 'general_model'  # Explicitly specifying the table name

    def __str__(self):
        return self.field_name
