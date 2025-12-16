"""
Transactions API Controller

Provides REST endpoints for managing financial transactions.
Delegates business logic to the TransactionsService.
"""
from flask import request, jsonify, Blueprint

from backend.app_context import transactions_service
transactions_api = Blueprint('transactions_api', __name__)

@transactions_api.route('/categories', methods=['GET'])
def get_categories():
    try:
        data = transactions_service.get_all_categories()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transactions_api.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get all transactions, optionally filtered by category or sub-category
    Query parameter: ?category=<category_name>
    Query parameter: ?sub_category=<sub_category_name>
    """
    category = request.args.get('category')
    sub_category = request.args.get('sub_category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        transactions = transactions_service.get_transactions(category, sub_category, start_date=start_date, end_date=end_date, as_dict=True)
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_api.route('/transactions', methods=['POST'])
def add_transaction():
    """Add a new transaction"""
    try:
        data = request.json
        transactions_service.add_transaction(data)
        return jsonify({'message': 'Transaction added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        print("UNCAUGHT ERROR:", e)
        return jsonify({'error': 'Internal server error'}), 500