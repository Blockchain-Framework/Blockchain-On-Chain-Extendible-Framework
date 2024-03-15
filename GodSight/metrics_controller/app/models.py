from django.db import models

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

class MetricsData(models.Model):
    date = models.DateField()
    blockchain = models.CharField(max_length=255)
    subchain = models.CharField(max_length=255)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='metrics_data')
    value = models.FloatField()

    class Meta:
        unique_together = ('date', 'blockchain', 'subchain', 'metric',)

class Blockchain(models.Model):
    blockchain = models.CharField(max_length=255, unique=True)
    sub_chain = models.CharField(max_length=255)
    original = models.BooleanField(default=False)
    start_date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class ChainMetric(models.Model):
    blockchain = models.ForeignKey(Blockchain, related_name='metrics', on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('blockchain', 'metric_name',)

class GeneralModel(models.Model):
    field_name = models.CharField(max_length=64, primary_key=True)
    data_type = models.CharField(max_length=64)
    description = models.TextField()

    class Meta:
        db_table = 'general_model'  # Explicitly specifying the table name

    def __str__(self):
        return self.field_name
