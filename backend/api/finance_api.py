from datetime import datetime

from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS

from backend.services import transactions_service, reports_service,budgets_service
from backend.model.category import Category

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/chart/monthly-income-share-chart', methods=['GET'])
def get_monthly_income_share_chart():
    """
    Returns a donut-chart with income shares by sub-categories for a specified month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))

        img = reports_service.get_monthly_income_share_chart_img(year, month)
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/monthly-spending-share-chart', methods=['GET'])
def get_monthly_spending_share_chart():
    """
    Returns a donut-chart with expense shares by categories for a specified month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))

        img = reports_service.get_monthly_spending_share_chart_img(year, month)
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/monthly-summary', methods=['GET'])
def get_monthly_summary_chart():
    """
    Returns the account balance history for the last 30 days as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        img = reports_service.get_monthly_summary_chart_img()
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chart/bar-chart', methods=['GET'])
def get_bar_chart():
    """
    Returns a bar chart that shows each set budget in relation to its spent amount in the current month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        img = reports_service.get_bar_chart_img()
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# Transaction Management
@app.route('/api/categories', methods=['GET'])
def get_categories():
    data = [
        {
            "category_name": cat.category_name,
            "sub_categories": cat.sub_categories,
            "is_income": cat.is_income
        }
        for cat in Category
    ]
    return jsonify(data)


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions, optionally filtered by category"""
    category = request.args.get('category')
    try:
        if category:
            transactions = transactions_service.get_transactions_by_category(category)
        else:
            transactions = transactions_service.get_all_transactions()

        return jsonify([{
            'amount': (t.amount if Category.from_category_as_string(t.category_name).is_income else -t.amount),
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
        category_name = data['category']
        sub_category = data['sub_category']

        transactions_service.add_transaction(amount, category_name, sub_category)
        return jsonify({'message': 'Transaction added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        print("UNCAUGHT ERROR:", e)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/transactions/by-date', methods=['GET'])
def get_transactions_by_date():
    """Get transactions filtered by date"""
    try:
        exact_date = request.args.get('exact_date')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        transactions = transactions_service.get_transactions_by_date(
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

        transactions = transactions_service.get_transactions_by_sub_category(sub_category)
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

        budgets_service.set_budget(category_name, limit)

        return jsonify({'message': f'Budget set for category: {category_name}'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/budgets', methods=['GET'])
def get_all_budgets():
    """Gets all budgets and calculates amount that is already spent in this month."""
    try:
        result = []

        for category, budget in budgets_service.budgets.items():
            category_name = category.category_name
            current_spent_amount = budgets_service.get_current_spent_amount(category_name)

            budget.spent = current_spent_amount

            result.append({
                'category_name': category_name,
                'limit': budget.limit,
                'spent': current_spent_amount,
                'remaining': budget.get_remaining()
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/budgets/<category_name>', methods=['DELETE'])
def delete_budget(category_name: str):
    """Deletes a budget for a category"""
    budgets_service.delete_budget(category_name)
    return jsonify({'message': f'Budget {category_name} was successfully deleted'}), 200