from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Metric, BlockchainMetric
from .metric_validator import validate_json_structure, validate_columns_existence_and_type, validate_arithmetic_order
from django.core.exceptions import ValidationError
import json
import uuid


@require_http_methods(["POST"])
def create_metric(request):
    try:
        data = json.loads(request.body)

        # Assuming 'blockchain' and 'sub_chain' are provided in the request
        blockchain = data.get('blockchain')
        sub_chain = data.get('sub_chain', 'default')  # Default sub_chain if not provided

        # Preliminary validation for required fields
        if not all(key in data for key in ['metric_name', 'blockchain']):
            return JsonResponse({"error": "Missing required fields."}, status=400)

        # Create Metric object
        metric, created = Metric.objects.get_or_create(
            metric_name=data['metric_name'],
            defaults={
                'display_name': data.get('display_name', ''),
                'description': data.get('description', ''),
                'category': data.get('category', '') or 'Default Category',
                'type': data.get('type', '') or 'Default Type',
                'formula': data.get('formula', None)
            }
        )

        # Only proceed with further processing if the metric was newly created
        if created:
            try:
                formula_json = metric.formula
                formula_type = data.get('type', 'Default Type')  # Use type for formula_type if necessary
                formula = json.loads(formula_json) if formula_json else {}
            except ValueError:
                raise ValidationError('Invalid JSON format.')

            # Validate JSON structure based on the formats
            is_valid_structure, msg_structure = validate_json_structure(formula, formula_type)
            if not is_valid_structure:
                metric.delete()  # Rollback metric creation if validation fails
                return JsonResponse({"error": msg_structure}, status=400)

            # Additional validation to check column existence and types
            is_valid_columns, msg_columns = validate_columns_existence_and_type(formula, formula_type, blockchain,
                                                                                sub_chain)
            if not is_valid_columns:
                metric.delete()  # Rollback metric creation if validation fails
                return JsonResponse({"error": msg_columns}, status=400)

            # Create BlockchainMetric object
            BlockchainMetric.objects.create(
                blockchain_id=uuid.uuid4(),  # Generate a new UUID for each BlockchainMetric
                blockchain=blockchain,
                sub_chain=sub_chain,
                metric=metric
            )

        return JsonResponse({"message": "Metric created successfully", "metric": metric.metric_name}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)