from flask import Blueprint, jsonify, request
from models.metric import (DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount, 
                           TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring, 
                           CrossChainWhaleActivity)
from datetime import datetime

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

@metrics_blueprint.route('/daily_transaction_count')
def get_daily_transaction_count():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = DailyTransactionCount.query
    query = filter_by_date(DailyTransactionCount, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/average_transactions_per_block')
def get_average_transactions_per_block():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = AverageTransactionsPerBlock.query
    query = filter_by_date(AverageTransactionsPerBlock, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/total_staked_amount')
def get_total_staked_amount():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = TotalStakedAmount.query
    query = filter_by_date(TotalStakedAmount, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/total_burned_amount')
def get_total_burned_amount():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = TotalBurnedAmount.query
    query = filter_by_date(TotalBurnedAmount, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/average_transaction_value')
def get_average_transaction_value():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = AverageTransactionValue.query
    query = filter_by_date(AverageTransactionValue, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/large_transaction_monitoring')
def get_large_transaction_monitoring():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = LargeTransactionMonitoring.query
    query = filter_by_date(LargeTransactionMonitoring, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/cross_chain_whale_activity')
def get_cross_chain_whale_activity():
    start_date = validate_date(request.args.get('start_date'))
    end_date = validate_date(request.args.get('end_date'))

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    query = CrossChainWhaleActivity.query
    query = filter_by_date(CrossChainWhaleActivity, query, start_date, end_date)
    data = query.all()
    return jsonify([item.serialize() for item in data])
