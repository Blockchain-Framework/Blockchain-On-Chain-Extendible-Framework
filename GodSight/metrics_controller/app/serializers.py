from rest_framework import serializers
from .models import Metric, MetricsData, Blockchain, ChainMetric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class MetricsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsData
        fields = ['date', 'value']


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
