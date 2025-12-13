"""
Budgets API Controller

Provides REST endpoints for managing budgets per category.
Delegates business logic to the BudgetsService.
"""
from flask import jsonify, request, Blueprint

from backend.app_context import budgets_service
budgets_api = Blueprint('budgets_api', __name__)

@budgets_api.route('/budgets', methods=['POST'])
def set_budget():
    """Set a budget for a category"""
    try:
        data = request.json

        budgets_service.set_budget(data)

        category_name = data['category_name']

        return jsonify({'message': f'Budget set for category: {category_name}'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budgets_api.route('/api/budgets', methods=['GET'])
def get_all_budgets():
    """Gets all budgets from BudgetsService."""
    try:
        budgets = budgets_service.BudgetsService.get_all_budgets()

        return jsonify(budgets), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budgets_api.route('/api/budgets/<category_name>', methods=['DELETE'])
def delete_budget(category_name: str):
    """Deletes a budget for a category"""
    try:
        budgets_service.delete_budget(category_name)

        return jsonify({'message': f'Budget {category_name} was successfully deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500