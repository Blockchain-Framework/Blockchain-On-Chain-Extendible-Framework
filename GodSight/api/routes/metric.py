from flask import Blueprint, request, current_app
from ..utils.get_metric_model import MetricsData, Metric
from ..models.response import Response # Import the custom Response
from ..utils.json_utils import jsonify  # Import the custom jsonify
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import logging
from flasgger import swag_from

metrics_blueprint = Blueprint('metrics', __name__)


def filter_by_date(model, query, start_date, end_date):
    """
    Filter a database query based on a date range.
    """
    if start_date:
        query = query.filter(model.date >= start_date)
    if end_date:
        query = query.filter(model.date <= end_date)
    # if chain:
    #     query = query.filter(model.chain_name == chain)
    return query


def validate_date(date_str):
    """
    Validate and convert a date string to a datetime object.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    except ValueError:
        return None


def get_paginated_data(model, query):
    """
    Apply pagination to a database query and return the paginated query.
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 30, type=int)

    return query.paginate(page=page, per_page=page_size, error_out=False)


def handle_metric_route():
    """
    Handle the route logic, including validation, querying, and response formatting.
    """
    try:
        blockchain = request.args.get('blockchain')
        subchain = request.args.get('subChain')
        metric_name = request.args.get('metric')
        time_range = request.args.get('timeRange')

        if blockchain is None or metric_name is None or time_range is None:
            raise ValueError("Invalid parameters.")

        # Calculate start_date and end_date based on time_range
        end_date = datetime.now().date()
        if time_range == '7_days':
            start_date = end_date - timedelta(days=7)
        else:
            raise ValueError("Invalid time range.")

        metric_details = Metric.query.filter_by(metric_name=metric_name).first()
        if metric_details is None:
            raise ValueError("Invalid metric.")

        util_data = metric_details.serialize()

        query = MetricsData.query.filter(
            MetricsData.date.between(start_date, end_date),
            MetricsData.blockchain == blockchain,
            MetricsData.metric == metric_name
        )

        if subchain == 'default':
            query = query.with_entities(MetricsData.date, func.sum(MetricsData.value).label('sum_value')) \
                .group_by(MetricsData.date)
            items = query.all()
            serialized_items = []
            for item in items:
                date, sum_value = item
                serialized_item = {
                    'date': date,
                    'blockchain': blockchain,
                    'subchain': 'default',
                    'metric': metric_name,
                    'value': float(sum_value)
                }
                serialized_items.append(serialized_item)
            chart_data = serialized_items
        else:
            query = query.filter(MetricsData.subchain == subchain)
            paginated_query = get_paginated_data(MetricsData, query)
            items = paginated_query.items
            chart_data = [item.serialize() for item in items]

        response = Response(True, {"chart_data": chart_data, "util_data": util_data}, len(chart_data))
        return jsonify(response.to_dict()), 200

    except ValueError as ve:
        logging.error(f"Invalid parameters: {ve}")
        return jsonify(Response(False, error=str(ve)).to_dict()), 400
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return jsonify(Response(False, error="Database error").to_dict()), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify(Response(False, error=f"An unexpected error occurred: {str(e)}").to_dict()), 500

# Define individual routes for each metric
@metrics_blueprint.route('/chart_data')
@swag_from({
    'parameters': [
        {
            'name': 'blockchain',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Blockchain to query metrics for',
        },
        {
            'name': 'subChain',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Subchain to query metrics for',
        },
        {
            'name': 'metric',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The specific metric to retrieve',
        },
        {
            'name': 'timeRange',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The time range for the metric data, e.g., "7_days"',
        },
    ],
    'responses': {
        200: {
            'description': 'Successful response with metric data',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {
                        'type': 'boolean',
                        'example': True,
                    },
                    'data': {
                        'type': 'object',  # Updated to 'object' type
                        'properties': {}  # Empty properties for dynamic population
                    },
                    'count': {
                        'type': 'integer',
                        'example': 1,
                    },
                },
            },
        },
        400: {
            'description': 'Invalid parameters',
        },
        500: {
            'description': 'Internal server error',
        },
    },
})
def get_daily_transaction_count():
    try:
        response, status_code = handle_metric_route()
        data_properties = {}
        if status_code == 200:
            data = response.get_json().get('data', [])
            if data and isinstance(data, list) and isinstance(data[0], dict):
                # Assume all items have a similar structure as the first item
                data_properties = {key: {'type': type(value).__name__.lower(), 'example': value} for key, value in data[0].items()}
                # Update the schema here, but consider this might not be the correct or possible way to dynamically update Swagger schema
        return response
    except Exception as e:
        return jsonify(Response(False, error=f"An unexpected error occurred: {str(e)}").to_dict()), 500
