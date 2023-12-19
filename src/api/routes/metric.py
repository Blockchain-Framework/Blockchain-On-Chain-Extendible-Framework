from flask import Blueprint, jsonify
from ..models.metric import db, DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount, TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring, CrossChainWhaleActivity

metrics_blueprint = Blueprint('metrics', __name__)

@metrics_blueprint.route('/daily_transaction_count')
def get_daily_transaction_count():
    data = DailyTransactionCount.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/average_transactions_per_block')
def get_average_transactions_per_block():
    data = AverageTransactionsPerBlock.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/total_staked_amount')
def get_total_staked_amount():
    data = TotalStakedAmount.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/total_burned_amount')
def get_total_burned_amount():
    data = TotalBurnedAmount.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/average_transaction_value')
def get_average_transaction_value():
    data = AverageTransactionValue.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/large_transaction_monitoring')
def get_large_transaction_monitoring():
    data = LargeTransactionMonitoring.query.all()
    return jsonify([item.serialize() for item in data])

@metrics_blueprint.route('/cross_chain_whale_activity')
def get_cross_chain_whale_activity():
    data = CrossChainWhaleActivity.query.all()
    return jsonify([item.serialize() for item in data])
