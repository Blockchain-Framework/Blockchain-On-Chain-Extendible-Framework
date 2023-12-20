from flask import Blueprint, jsonify, request
from models.metric import (DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount,
                           TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring,
                           CrossChainWhaleActivity)
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

metrics_blueprint = Blueprint('metrics', __name__)

def filter_by_date(model, query, start_date, end_date):
    if start_date:
        query = query.filter(model.date >= start_date)
    if end_date:
        query = query.filter(model.date <= end_date)
    return query

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    except ValueError:
        return None

def get_paginated_data(model, query):
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)

        # Query with pagination
        paginated_query = query.paginate(page, page_size, False)
        items = paginated_query.items

        # Successful response
        return {
            "status": True,
            "data": [item.serialize() for item in items],
            "page_size": len(items)
        }
    except SQLAlchemyError:
        # Error in database operation
        return {"status": False, "error": "Database error"}

# Function to handle each metric route
def handle_metric_route(model):
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"status": False, "error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = model.query
    query = filter_by_date(model, query, start_date, end_date)
    response = get_paginated_data(model, query)
    return jsonify(response), response.get("status", 500)

# Define routes
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
