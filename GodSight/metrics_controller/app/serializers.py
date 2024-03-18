from rest_framework import serializers
from .models import Metric, MetricsData, Blockchain, ChainMetric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class MetricsDataSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.metric_name', read_only=True)

    class Meta:
        model = MetricsData
        fields = ['date', 'blockchain', 'subchain', 'metric', 'metric_name', 'value']
        depth = 1  # Adjust depth as needed for nested relationships


class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = '__all__'


class ChainMetricSerializer(serializers.ModelSerializer):
    blockchain_name = serializers.CharField(source='blockchain.blockchain', read_only=True)

    class Meta:
        model = ChainMetric
        fields = ['blockchain', 'blockchain_name', 'metric_name']
        depth = 1
