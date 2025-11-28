from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.finance_controller import FinanceController
from model.category import Category

app = Flask(__name__)
CORS(app)
controller = FinanceController()


# Transaction Management
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions, optionally filtered by category"""
    category = request.args.get('category')
    try:
        if category:
            transactions = controller.get_transactions_by_category(category)
        else:
            transactions = controller.get_all_transactions()

        return jsonify([{
            'amount': t.amount,
            'category_name': t.category_name,
            'sub_category': t.sub_category,
            'date': str(t.date)
        } for t in transactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    """Add a new transaction"""
    try:
        data = request.json
        amount = float(data['amount'])
        category_name = data['category_name']
        sub_category = data['sub_category']

        controller.add_transaction(amount, category_name, sub_category)
        return jsonify({'message': 'Transaction added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/transactions/by-date', methods=['GET'])
def get_transactions_by_date():
    """Get transactions filtered by date"""
    try:
        exact_date = request.args.get('exact_date')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        transactions = controller.get_transactions_by_date(
            exact_date=exact_date,
            start_date=start_date,
            end_date=end_date
        )

        return jsonify([{
            'amount': t.amount,
            'category_name': t.category_name,
            'sub_category': t.sub_category,
            'date': str(t.date)
        } for t in transactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/transactions/by-sub-category', methods=['GET'])
def get_transactions_by_sub_cat():
    """Get transactions by sub category"""
    try:
        sub_category = request.args.get('sub_category')
        if not sub_category:
            return jsonify({'error': 'sub_category parameter required'}), 400

        transactions = controller.get_transactions_by_sub_category(sub_category)
        return jsonify([{
            'amount': t.amount,
            'category_name': t.category_name,
            'sub_category': t.sub_category,
            'date': str(t.date)
        } for t in transactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Budget Management

@app.route('/api/budgets', methods=['POST'])
def set_budget():
    """Set a budget for a category"""
    try:
        data = request.json
        category_name = data['category_name']
        limit = float(data['limit'])

        controller.set_budget(category_name, limit)
        controller.storage.save_budget(category_name, limit)

        return jsonify({'message': f'Budget set for {category_name}'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/budgets/<category_name>', methods=['GET'])
def get_budget_status(category_name):
    """Get budget status for a category"""
    try:
        remaining = controller.check_budget(category_name)
        budget = controller.budgets.get(Category.from_category_as_string(category_name))

        if not budget:
            return jsonify({'error': f'No budget set for {category_name}'}), 404

        return jsonify({
            'category_name': category_name,
            'limit': budget.limit,
            'spent': budget.spent,
            'remaining': remaining,
            'percentage': round((budget.spent / budget.limit * 100) if budget.limit > 0 else 0, 2)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
