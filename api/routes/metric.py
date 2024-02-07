from flask import Blueprint, request, current_app
from utils.get_metric_model import metric_route_map
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

def handle_metric_route():
<<<<<<< HEAD
=======
    print("ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
>>>>>>> feature/dual-workflow
    """
    Handle the route logic, including validation, querying, and response formatting.
    """
    try:
        blockchain = request.args.get('blockchain')
        subchain = request.args.get('subChain')
        metric = request.args.get('metric')
        time_range = request.args.get('timeRange')
<<<<<<< HEAD
   
=======
        
        print(blockchain,subchain,metric,time_range)
        
>>>>>>> feature/dual-workflow
        model = metric_route_map[metric]
        
        if blockchain is None or subchain is None or metric is None or time_range is None:
            raise ValueError("Invalid parameters.")

        # Calculate start_date and end_date based on time_range
        end_date = datetime.now()
        if time_range == '7_days':
            start_date = end_date - timedelta(days=7)
        else:
            raise ValueError("Invalid time range.")
        
        query = model.query
<<<<<<< HEAD
        query = query.filter(model.date.between(start_date, end_date))
        # Add additional filters based on the new parameters
        query = query.filter_by(blockchain=blockchain, subchain=subchain)
        paginated_query = get_paginated_data(model, query)
        items = paginated_query.items

=======
        # query = query.filter(model.date.between(start_date, end_date))
        
        # Add additional filters based on the new parameters
        query = query.filter_by(blockchain=blockchain, subchain=subchain)
        print(query)
        paginated_query = get_paginated_data(model, query)
        items = paginated_query.items
        print(items)
>>>>>>> feature/dual-workflow
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
@metrics_blueprint.route('/chart_data')
def get_daily_transaction_count():
    return handle_metric_route()
