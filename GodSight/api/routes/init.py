from flask import Blueprint, request, current_app
from ..models.response import Response # Import the custom Response
from ..utils.json_utils import jsonify  # Import the custom jsonify
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import logging
from ..models.chain_info import (Blockchain, ChainMetric)

init_blueprint = Blueprint('init', __name__)

@init_blueprint.route('/')
def get_selection_data():
    print("got request for init")
    try:
        blockchains = Blockchain.query.all()
        blockchain_data = {}

        for blockchain in blockchains:
            if blockchain.blockchain not in blockchain_data:
                blockchain_data[blockchain.blockchain] = {}

            if blockchain.sub_chain:
                if blockchain.sub_chain not in blockchain_data[blockchain.blockchain]:
                    blockchain_data[blockchain.blockchain][blockchain.sub_chain] = []

                # Add metrics for each subchain
                metrics = [metric.metric_name for metric in blockchain.metrics]
                blockchain_data[blockchain.blockchain][blockchain.sub_chain].extend(metrics)

        response = Response(True, blockchain_data)
        print(response)
        return jsonify(response.to_dict()), 200
    except Exception as e:
        # Handle any exceptions
        return jsonify(Response(False, error=f"An unexpected error occurred: {str(e)}").to_dict()), 500
