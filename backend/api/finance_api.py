import io
import sqlite3
from datetime import datetime

import pandas as pd
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

from backend.services import transactions_service
from backend.services import budgets_service
from backend.model.category import Category
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

DATABASE = 'finances.db'

@app.route('/api/chart/monthly-summary', methods=['GET'])
def get_monthly_summary_chart():
    """Get account balance chart over last 30 days"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        previous_transactions = transactions_service.get_transactions_by_date(end_date=start_date)
        initial_balance = sum(t.amount for t in previous_transactions)

        transactions_last_30_days = transactions_service.get_transactions_by_date(start_date=start_date, end_date=end_date)

        df=pd.DataFrame([{
            'date': t.date,
            'amount': t.amount
        } for t in transactions_last_30_days])

        df['date'] = pd.to_datetime(df['date'],format='ISO8601').dt.normalize()
        df['balance'] = df['amount'].cumsum() + initial_balance
        daily_balance = df.groupby('date')['balance'].last()
        date_range = pd.date_range(start=start_date.date(), end=end_date.date(), freq='D')
        daily_balance = daily_balance.reindex(date_range, method='ffill')
        daily_balance.iloc[0] = initial_balance
        daily_balance = daily_balance.fillna(0)

        plt.figure(figsize=(12, 6))
        plt.plot(date_range, daily_balance,
                marker='o', linewidth=2.5, markersize=5,
                color='#2196F3', label='Balance')

        plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        plt.title('Account Balance - Last 30 Days',
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Balance (€)', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.xticks(rotation=45, ha='right')


        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plt.close()

        response = make_response(send_file(img, mimetype='image/png'))
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'

        return response

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
        raise

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

        return jsonify({'message': f'Budget set for {category_name}'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/budgets', methods=['GET'])
def get_all_budgets():
    """Get all budgets."""
    try:
        result = []

        for category, budget in budgets_service.budgets.items():
            result.append({
                'category_name': category.category_name,
                'limit': budget.limit,
                'spent': budget.spent,
                'remaining': budget.get_remaining()
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


