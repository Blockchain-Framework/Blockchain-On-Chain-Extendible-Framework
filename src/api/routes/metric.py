from flask import Blueprint, jsonify, request
from models.metric import (DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount,
                           TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring,
                           CrossChainWhaleActivity)
from models.response import Response
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

# Create a blueprint for your metrics routes
metrics_blueprint = Blueprint('metrics', __name__)

def filter_by_date(model, query, start_date, end_date):
    """
    Filter a database query based on a date range.
    """
    if start_date:
        query = query.filter(model.date >= start_date)
    if end_date:
        query = query.filter(model.date <= end_date)
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
    Apply pagination to a database query.
    """
    # Retrieve pagination parameters from request
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    # Paginate the query
    paginated_query = query.paginate(page, page_size, False)
    return paginated_query.items

def handle_metric_route(model):
    """
    Handle the route logic, including validation, querying, and response formatting.
    """
    try:
        # Validate the date parameters
        start_date = validate_date(request.args.get('start_date'))
        end_date = validate_date(request.args.get('end_date'))

        # Raise an error if date validation fails
        if start_date is None or end_date is None:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        # Prepare and execute the query
        query = model.query
        query = filter_by_date(model, query, start_date, end_date)
        items = get_paginated_data(model, query)

        # Create a successful response
        response = Response(True, [item.serialize() for item in items], len(items))
        return jsonify(response.to_dict()), 200
    except ValueError as ve:
        # Return a 400 error for invalid date formats
        return jsonify(Response(False, error=str(ve)).to_dict()), 400
    except SQLAlchemyError:
        # Return a 500 error for database operation issues
        return jsonify(Response(False, error="Database error").to_dict()), 500

# Define individual routes for each metric
@metrics_blueprint.route('/daily_transaction_count')
def get_daily_transaction_count():
    return handle_metric_route(DailyTransactionCount)

@metrics_blueprint.route('/average_transactions_per_block')
def get_average_transactions_per_block():
    return handle_metric_route(AverageTransactionsPerBlock)

@metrics_blueprint.route('/total_staked_amount')
def get_total_staked_amount():
    return handle_metric_route(TotalStakedAmount)

@metrics_blueprint.route('/total_burned_amount')
def get_total_burned_amount():
    return handle_metric_route(TotalBurnedAmount)

@metrics_blueprint.route('/average_transaction_value')
def get_average_transaction_value():
    return handle_metric_route(AverageTransactionValue)

@metrics_blueprint.route('/large_transaction_monitoring')
def get_large_transaction_monitoring():
    return handle_metric_route(LargeTransactionMonitoring)

@metrics_blueprint.route('/cross_chain_whale_activity')
def get_cross_chain_whale_activity():
    return handle_metric_route(CrossChainWhaleActivity)

