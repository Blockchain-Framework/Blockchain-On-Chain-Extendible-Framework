from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Avg
from django.core.exceptions import ValidationError
from .models import Metric, MetricsData, Blockchain, ChainMetric
from .serializers import MetricsDataSerializer, MetricSerializer, BlockchainSerializer
from .utils import APIResponse
from .validator import validate_json_structure, validate_columns_existence_and_type
from django.db.models import Prefetch


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class MetricsDataView(APIView, StandardResultsSetPagination):
    print("--------1")
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('blockchain', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='Blockchain to query metrics for'),
        openapi.Parameter('subChain', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='Subchain to query metrics for'),
        openapi.Parameter('metric', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='The specific metric to retrieve'),
        openapi.Parameter('timeRange', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                          description='The time range for the metric data, e.g., "7_days"'),
    ])
    def get(self, request, *args, **kwargs):
        print("--------2")
        blockchain = request.query_params.get('blockchain')
        subchain = request.query_params.get('subChain')
        metric_name = request.query_params.get('metric')
        time_range = request.query_params.get('timeRange')

        # Validate request parameters
        if not all([blockchain, subchain, metric_name, time_range]):
            return JsonResponse(APIResponse(False, error="Missing required parameters.").to_dict(),
                                status=status.HTTP_400_BAD_REQUEST)

        # Validate and process date range
        try:
            end_date = datetime.now().date()
            if time_range == '7_days':
                start_date = end_date - timedelta(days=7)
            else:
                raise ValueError("Invalid time range parameter.")
        except ValueError as e:
            print("--------2e")
            return JsonResponse(APIResponse(False, error=str(e)).to_dict(),
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            print("--------3")
            # Query database
            queryset = MetricsData.objects.filter(
                date__range=(start_date, end_date),
                blockchain=blockchain,
                metric__metric_name=metric_name
            )

            try:
                print("--------4")
                blockchain_obj = Blockchain.objects.get(blockchain=blockchain, sub_chain=subchain)
            except Blockchain.DoesNotExist:
                print("--------4e")
                raise Exception('Invalid Blockchain')

            if blockchain_obj and not blockchain_obj.original:
                print("--------5")
                try:
                    print("--------6")
                    metric_obj = Metric.objects.get(metric_name=metric_name)
                except Metric.DoesNotExist:
                    print("--------6e")
                    raise Exception('Metric Finding failed')

                aggregation_mapping = {
                    'sum': Sum('value'),
                    'avg': Avg('value'),
                }

                aggregation = aggregation_mapping.get(metric_obj.grouping_type, Sum('value'))

                # Apply aggregation and alias it as 'value'
                queryset = queryset.values('date').annotate(value=aggregation).order_by('date')
            else:
                print("--------7")
                if subchain != 'default':
                    queryset = queryset.filter(subchain=subchain)

            # At this point, queryset is ready for serialization
            serializer = MetricsDataSerializer(queryset, many=True)
            print("--------50")
            print(str(queryset.query))
            page = self.paginate_queryset(queryset, request, view=self)
            print("--------10")
            if page is not None:
                print("--------8")
                serializer = MetricsDataSerializer(page, many=True)
                return JsonResponse(APIResponse(
                    True,
                    serializer.data,
                    page_size=self.get_page_size(request),
                    total_pages=self.page.paginator.num_pages,
                    current_page=self.page.number,
                    total_items=self.page.paginator.count
                ).to_dict(), status=status.HTTP_200_OK)
            print("--------5")


            serializer = MetricsDataSerializer(queryset, many=True)
            return JsonResponse(APIResponse(True, serializer.data).to_dict(), status=status.HTTP_200_OK)
        except ValidationError as e:
            print("--------3e")
            return JsonResponse(APIResponse(False, error="Invalid query parameters.").to_dict(),
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("--------3e2")
            # Log the error for server-side debugging.
            print("Internal server error: ", e)  # Consider using logging instead of print in production
            return JsonResponse(APIResponse(False, error="Internal server error").to_dict(),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSelectionDataView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Selection Data",
        responses={
            200: openapi.Response('Successful response', examples={
                'application/json': {
                    "success": True,
                    "data": {
                        "Blockchain1": {
                            "Subchain1": ["Metric1", "Metric2"]
                        }
                    }
                }
            }),
            500: openapi.Response('Internal Server Error')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            blockchains = Blockchain.objects.all().prefetch_related('metrics')

            blockchain_data = {}

            for blockchain in blockchains:
                blockchain_key = blockchain.blockchain
                if blockchain_key not in blockchain_data:
                    blockchain_data[blockchain_key] = {}

                sub_chain_key = blockchain.sub_chain or 'default'
                if sub_chain_key not in blockchain_data[blockchain_key]:
                    blockchain_data[blockchain_key][sub_chain_key] = []

                # Assuming metrics is a related name for ChainMetric or direct metric relationship
                # And metric_name is a field on the Metric model
                metrics = [metric.metric_name.metric_name for metric in blockchain.metrics.all()]
                blockchain_data[blockchain_key][sub_chain_key].extend(metrics)

            final_data = []
            for blockchain, subchains in blockchain_data.items():
                for sub_chain, metrics in subchains.items():
                    final_data.append({
                        "blockchain": blockchain,
                        "sub_chain": sub_chain,
                        "metrics": metrics
                    })
            return Response({"data": final_data}, status=status.HTTP_200_OK)
        except Exception as e:
            # Here, consider using logging instead of print for production code
            return JsonResponse(APIResponse(False, error=f"An unexpected error occurred: {str(e)}").to_dict(),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateMetricView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['metric_name', 'blockchain'],
        properties={
            'metric_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the metric'),
            'blockchain': openapi.Schema(type=openapi.TYPE_STRING, description='Blockchain name'),
            'sub_chain': openapi.Schema(type=openapi.TYPE_STRING, description='Sub-chain', default='default'),
            'display_name': openapi.Schema(type=openapi.TYPE_STRING, description='Display name of the metric',
                                           default=''),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the metric',
                                          default=''),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Category of the metric',
                                       default='Default Category'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the metric', default='Default Type'),
            'formula': openapi.Schema(type=openapi.TYPE_OBJECT, description='Formula JSON object',
                                      additionalProperties=True),
        }
    ), responses={201: openapi.Response('Metric created successfully'), 400: 'Invalid JSON format or missing fields'})
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Preliminary validation for required fields
            required_fields = ['metric_name', 'blockchain', 'sub_chain', 'formula', 'type']
            if not all(field in data for field in required_fields):
                return JsonResponse(APIResponse(False, error="Missing required fields.").to_dict(),
                                    status=400)

            if data.get('type') not in ['Format 1', 'Format 2']:
                return JsonResponse(APIResponse(False, error="Invalid Formula Type.").to_dict(),
                                    status=400)

            blockchain_qs = Blockchain.objects.filter(blockchain=data.get('blockchain'),
                                                      sub_chain=data.get('sub_chain'))
            if not blockchain_qs.exists():
                return JsonResponse(
                    APIResponse(False, error="Blockchain and sub-chain combination does not exist.").to_dict(),
                    status=400)

            blockchain = blockchain_qs.first()

            metric_exists = ChainMetric.objects.filter(
                blockchain=blockchain,
                metric_name=data.get('metric_name')
            ).exists()

            if metric_exists:
                return JsonResponse(APIResponse(False,
                                                error="A metric with the given name, blockchain, and sub-chain already "
                                                      "exists.").to_dict(),
                                    status=400)

            formula = json.loads(data.get('formula')) if data.get('formula') else {}

            success_structure, error = validate_json_structure(formula, data.get('type'))

            if not success_structure:
                return JsonResponse(
                    APIResponse(False, error=error).to_dict(),
                    status=400)

            success_column_rules, error = validate_columns_existence_and_type(formula, data.get('type'),
                                                                              data.get('blockchain'),
                                                                              data.get('sub_chain'))

            if not success_column_rules:
                return JsonResponse(
                    APIResponse(False, error=error).to_dict(),
                    status=400)

            metric = Metric.objects.create(
                metric_name=data.get('metric_name'),
                display_name=data.get('display_name', ''),
                description=data.get('description', ''),
                category=data.get('category', 'Default Category'),
                type=data.get('type', 'Default Type'),
                formula=data.get('formula', None)  # Ensure your Metric model supports JSONField or similar
            )

            ChainMetric.objects.create(
                blockchain=blockchain,
                metric_name=metric.metric_name
            )

            serializer = MetricSerializer(metric)
            return JsonResponse(APIResponse(True, data=serializer.data).to_dict(), status=201)

        except Exception as e:  # General exception catch, consider more specific exception handling
            return JsonResponse(APIResponse(False, error=str(e)).to_dict(), status=500)
