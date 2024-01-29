from flask import Blueprint, request, current_app
from models.metric import (DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount,
                           TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring,
                           CrossChainWhaleActivity, WhaleAddressActivity, AvgUtxoValue, MedianTransactionValue,
                           CumulativeNumberOfTransactions, ActiveAddresses, TransactionsPerSecond)
from models.response import Response # Import the custom Response
from utils.json_utils import jsonify  # Import the custom jsonify
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import logging
 
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

    # Correctly using keyword arguments for paginate
    return query.paginate(page=page, per_page=page_size, error_out=False)

@metrics_blueprint.route('/')
def handle_metric_route(model):
    """
    Handle the route logic, including validation, querying, and response formatting.
    """
    try:
        blockchain = request.args.get('blockchain')
        sub_chain = request.args.get('subChain')
        metric = request.args.get('metric')
        time_range = request.args.get('timeRange')
        token = request.args.get('token')

        if blockchain is None or sub_chain is None or metric is None or time_range is None or token is None:
            raise ValueError("Invalid parameters.")

        # Calculate start_date and end_date based on time_range
        end_date = datetime.now()
        print(end_date)
        if time_range == '7_days':
            start_date = end_date - timedelta(days=7)
        else:
            raise ValueError("Invalid time range.")

        query = model.query
        query = query.filter(model.date.between(start_date, end_date))
        # Add additional filters based on the new parameters
        query = query.filter_by(blockchain=blockchain, sub_chain=sub_chain, metric=metric, token=token)
        paginated_query = get_paginated_data(model, query)
        items = paginated_query.items

        response = Response(True, [item.serialize() for item in items], len(items))
        return jsonify(response.to_dict()), 200

    except ValueError as ve:
        return jsonify(Response(False, error=str(ve)).to_dict()), 400
    except SQLAlchemyError as e:
        # Log the detailed error message for debugging
        logging.error(f"Database error: {e}")
        return jsonify(Response(False, error="Database error").to_dict()), 500
    except Exception as e:
        # Generic catch for any other unexpected exceptions
        return jsonify(Response(False, error=f"An unexpected error occurred: {str(e)}").to_dict()), 500

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

@metrics_blueprint.route('/whale_address_activity')
def get_whale_address_activity():
    return handle_metric_route(WhaleAddressActivity)

@metrics_blueprint.route('/avg_utxo_value')
def get_avg_utxo_value():
    return handle_metric_route(AvgUtxoValue)

@metrics_blueprint.route('/median_trx_value')
def get_median_trx_value():
    return handle_metric_route(MedianTransactionValue)

@metrics_blueprint.route('/cumulative_number_of_trx')
def get_cumulative_number_of_trx():
    return handle_metric_route(CumulativeNumberOfTransactions)

@metrics_blueprint.route('/active_addresses')
def get_active_addresses():
    return handle_metric_route(ActiveAddresses)

@metrics_blueprint.route('/trx_per_second')
def get_trx_per_second():
    return handle_metric_route(TransactionsPerSecond)
